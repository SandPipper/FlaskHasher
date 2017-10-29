from flask import render_template, request, url_for, session, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from ..models import User
from ..email import send_email
from .. import db, login_manager
from .forms import SignUpForm, SignInForm


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        if not current_user.confirmed \
                and request.endpoint \
                and request.endpoint[:5] != "auth." \
                and request.endpoint != 'static':
            return redirect(url_for("auth.unconfirmed"))


@auth.route("/unconfirmed")
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect("main.index")
    return render_template("unconfirmed.html")


@auth.route("/sign", methods=["GET", "POST"])
def signing():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    signUpForm = SignUpForm()
    if signUpForm.submitSignUp.data and signUpForm.validate():
        user = User(email=signUpForm.email.data,
                    username=signUpForm.username.data,
                    password=signUpForm.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, "Confirm Your Account", "mail/confirm",
                   user=user, token=token)
        flash("A confirmation email has been sent to you by email.")
        return redirect(url_for(".signing"))

    signInForm = SignInForm()
    if signInForm.submitSignIn.data and signInForm.validate():
        user = User.query.filter_by(email=signInForm.email.data).first()
        if user is not None and user.verify_password(signInForm.password.data):
            login_user(user, signInForm.remember_me.data)
            session.permanent = True
            flash("Welcome, {}!".format(user.username))
            return redirect(request.args.get("next") or url_for("main.index"))
        flash("Invalid username or password.")

    return render_template("sign.html", signUpForm=signUpForm,
                           signInForm=signInForm)


@auth.route("/confirm/<token>")
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for("main.index"))
    if current_user.confirm(token):
        flash("You have confirmed your account. Thanks!")
    else:
        flash("The confirmation link is invalid or has expired.")
    return redirect(url_for("main.index"))


@auth.route("/confirm")
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, "Confirm Your Account", "mail/confirm",
               user=current_user, token=token)
    flash("A new confirmation email has been sent to you by email.")
    return redirect(url_for("auth.signing"))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('auth.signing'))
