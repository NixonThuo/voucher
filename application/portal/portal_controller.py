from flask import Blueprint, render_template, request, session, redirect
from flask_login import login_required
from application.main.main_model import CreditServicesTr, ServiceType, ServiceTypeOptions
from application import db
from application.portal.portal_services import send_payment_req


dash = Blueprint('dash', __name__)


@login_required
def before_request():
    pass


@dash.route('/tracking',  methods=['GET', 'POST'])
def dash_tracking():
    rows = CreditServicesTr.query.join(
        ServiceType,
        CreditServicesTr.service_id == ServiceType.id
    ).add_columns(
        CreditServicesTr.cc_tr_serial,
        CreditServicesTr.amount,
        CreditServicesTr.user_id,
        CreditServicesTr.approved,
        CreditServicesTr.rejected,
        CreditServicesTr.admin_user_id,
        CreditServicesTr.date_admin_action,
        CreditServicesTr.date_added,
        CreditServicesTr.phone_no,
        CreditServicesTr.service_id,
        CreditServicesTr.marked_paid,
        ServiceType.service_type
    ).all()
    services = ServiceType.query.all()
    soptions = ServiceTypeOptions.query.filter_by(enabled=True).all()
    return render_template("portal/list_requests.html", rows=rows, services=services, soptions=soptions)


@dash.route('/postreq',  methods=['GET', 'POST'])
def post_req():
    if request.method == "POST":
        phonenumber = request.form.get('phonenumber')
        creditamount = request.form.get('creditamount')
        servicetype = request.form.get('servicetype')
        print("service type "+str(servicetype))
        serviceserial = request.form.get('serviceserial')
        print("service serial"+str(serviceserial))
        cashreq = CreditServicesTr(
            amount=creditamount,
            phone_no=phonenumber,
            user_id=session['userid'],
            service_id=serviceserial
        )
        db.session.add(cashreq)
        db.session.commit()
        return render_template("portal/request_sent.html")
    return render_template("portal/list_requests.html")


@dash.route('/initiatepayment',  methods=['GET', 'POST'])
def initiate_payment():
    if request.method == "POST":
        payservicename = request.form.get('payservicename')
        paymentserial = request.form.get('paymentserial')
        payamount = request.form.get('payamount')
        paymentdata = send_payment_req(payamount, paymentserial, payservicename)
        if paymentdata["success"]:
            paymentid = paymentdata["yoco"]["id"]
            redirecturl  = paymentdata["yoco"]["redirectUrl"]
            trans  = CreditServicesTr.query.filter_by(
                cc_tr_serial=paymentserial
            ).first()
            trans.yoco_paymentid = paymentid
            trans.yoco_checkoutid = paymentdata["yoco"]["metadata"]["checkoutId"]
            trans.yoco_payment_facilitator = paymentdata["yoco"]["metadata"]["paymentFacilitator"]
            trans.yoco_payment_facilitator = paymentdata["yoco"]["merchantId"]
            db.session.commit()
            return redirect(redirecturl)
        return render_template("portal/payment_success.html", paymentdata=paymentdata)
    return render_template("portal/list_requests.html")


@dash.route('/succurl/<paymentserial>',  methods=['GET', 'POST'])
def succ_url(paymentserial):
    trans  = CreditServicesTr.query.filter_by(
                cc_tr_serial=paymentserial
            ).first()
    trans.success_url = True
    db.session.commit()
    return render_template("portal/payment_success.html", trans=trans)
