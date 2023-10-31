from flask import Blueprint, render_template, request, session
from flask_login import login_required
from application.main.main_model import CreditServicesTr, ServiceType, ServiceTypeOptions
from application import db


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
