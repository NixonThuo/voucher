from flask import Blueprint, render_template
from flask_login import login_required


dash = Blueprint('dash', __name__)

@login_required
def before_request():
    pass

@dash.route('/tracking',  methods=['GET', 'POST'])
def dash_tracking():
    return render_template("portal/list_requests.html")
