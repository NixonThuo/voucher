from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from application.main.login_form import LoginForm, RegistrationForm
from application.main.login_model import Users
from datetime import datetime
from application import app, db
from flask_login import login_user, logout_user
import hashlib


main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def home():
    today = datetime.now().date()
    return render_template("main.html")


@main.route('choose_service', methods=['GET', 'POST'])
def choose_service():
    today = datetime.now().date()
    return render_template("get_service.html")


@main.route('admin_home', methods=['GET', 'POST'])
def admin_home():
    today = datetime.now().date()
    return render_template("admin/layout.html")


@main.route('portal_login', methods=['GET', 'POST'])
def portal_login():
    today = datetime.now().date()
    form = LoginForm(request.form)
    """login controller"""
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        user = Users.query.filter_by(
            useremail=email
        ).first()
        print("user")
        print(user)
        if user is not None and user.password_check(password):
            if user.isenabled is True:
                login_user(user)
                session.permanent = True
                session['userid'] = str(user.userid)
                return redirect(url_for('dash.dash_tracking'))
    return render_template("portal/login.html", form=form)


@main.route('portal_enroll', methods=['GET', 'POST'])
def portal_enroll():
    today = datetime.now().date()
    form = RegistrationForm(request.form)
    if request.method == "POST":
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')

        if password != password2:
            flash("password did not match", category="danger")
            return render_template("portal/register.html")

        user = Users.query.filter_by(username=username).first()

        if user:
            flash("username already exists", category="danger")
            return render_template("portal/register.html")

        user = Users.query.filter_by(useremail=email).first()

        if user:
            flash("email already exists")
            return render_template("portal/register.html", category="danger")

        user = Users(
            username=username,
            useremail=email,
            password=hashlib.md5(password.encode()).hexdigest()
        )

        db.session.add(user)
        db.session.commit()
        return render_template("portal/register_success.html")
    return render_template("portal/register.html", form=form)


@main.route('/logout', methods=('GET', 'POST'))
def login_out():
    logout_user()
    return redirect(url_for('main.portal_login'))
