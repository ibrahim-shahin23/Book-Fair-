from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user
from app.models import User
from .forms import RegisterForm, LoginForm


auth_blueprint = Blueprint('auth', __name__,url_prefix='/auth')

@auth_blueprint.route('/register',methods=['GET','POST'],endpoint='register')
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data, password=form.password.data)
        user.save_to_db()
        return redirect(url_for('main.index'))
    return render_template("form.html",form=form , form_title = "Signup")

@auth_blueprint.route('/login',methods=['GET','POST'],endpoint='login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.verify_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('main.index'))
        flash("Invalid email or password")
    return render_template("form.html",form=form, form_title = "Login")

@auth_blueprint.route('/logout',endpoint='logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))