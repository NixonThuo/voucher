from flask import Blueprint, render_template, session, request
from application.main.main_model import CreditCashTr
from flask_login import login_required
from datetime import datetime
from application import db

admin = Blueprint('admin', __name__)


@login_required
def before_request():
    if session['isadmin'] is not True:
        return render_template("admin/401.html"), 401


@admin.route('/clientrqs',  methods=['GET', 'POST'])
def client_rqs():
    rows = CreditCashTr.query.all()
    return render_template("admin/list_requests.html", rows=rows)


@admin.route('/rejectreq',  methods=['GET', 'POST'])
def rejectreq():
    if request.method == "POST":
        rejectrequestserial = request.form.get('rejectrequestserial')
        rej = CreditCashTr.query.filter_by(
            cc_tr_serial=rejectrequestserial
        ).first()
        rej.rejected = True
        rej.admin_user_id = session['userid']
        rej.date_admin_action = datetime.now()
        db.session.commit()
        rows = CreditCashTr.query.all()
    return render_template("admin/list_requests.html", rows=rows)


@admin.route('/approvereq',  methods=['GET', 'POST'])
def approvereq():
    if request.method == "POST":
        approverequestserial = request.form.get('approverequestserial')
        rej = CreditCashTr.query.filter_by(
            cc_tr_serial=approverequestserial
        ).first()
        rej.approved = True
        rej.admin_user_id = session['userid']
        rej.date_admin_action = datetime.now()
        db.session.commit()
        rows = CreditCashTr.query.all()
    return render_template("admin/list_requests.html", rows=rows)
