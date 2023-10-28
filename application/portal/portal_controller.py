from flask import Blueprint, render_template, request, session
from flask_login import login_required
from application.main.main_model import CreditServicesTr
from application import db


dash = Blueprint('dash', __name__)


@login_required
def before_request():
    pass


@dash.route('/tracking',  methods=['GET', 'POST'])
def dash_tracking():
    rows = CreditServicesTr.query.all()
    return render_template("portal/list_requests.html", rows=rows)


@dash.route('/postreq',  methods=['GET', 'POST'])
def post_req():
    if request.method == "POST":
        phonenumber = request.form.get('phonenumber')
        creditamount = request.form.get('creditamount')
        cashreq = CreditServicesTr(
            amount=creditamount,
            phone_no=phonenumber,
            user_id=session['userid']
        )
        db.session.add(cashreq)
        db.session.commit()
        return render_template("portal/request_sent.html")
    return render_template("portal/list_requests.html")
