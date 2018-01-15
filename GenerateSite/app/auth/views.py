from flask import render_template, redirect, request, url_for, flash
from . import auth
from flask_login import login_user, logout_user, login_required, current_user
from ..models import User
from .forms import \
    LoginForm, \
    RegistrationForm, \
    ChangeEmailForm, \
    ChangePasswordForm, \
    ResetPasswordEmailForm, \
    ChangeUsernameForm, \
    ResetPasswordForm
from .. import db
from ..email import send_email

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email,
                   'Confirm Your Account',
                   'auth/email/confirm',
                   user=user,
                   token=token)
        flash('A cofirmation email has been sent to you by email.')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired!')
    return redirect(url_for('main.index'))

@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email,
               'Confirm Your Account',
               'auth/email/confirm',
               user=current_user,
               token=token )
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))

@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
        and not current_user.confirmed \
        and request.endpoint[:5] != 'auth.':
        return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect('main.index')
    return render_template('auth/unconfirmed.html')

@auth.route('/account')
@login_required
def account():
    return render_template('auth/account.html')

@auth.route('/change_email', methods = ['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if current_user.is_authenticated and form.validate_on_submit():
        token = current_user.generate_email_reset_token(form.new_email.data)
        send_email(form.new_email.data,
                   'Change Your Email',
                   'auth/email/change_email',
                   user=current_user,
                   token=token,
                   next=request.args.get('next'))
        flash('We sent you a link to your new email. Go click the link we sent to finish changing the email!')
    return render_template('auth/change_email.html', form=form)

@auth.route('/change_email/<token>')
@login_required
def change_email(token):
    if current_user.is_authenticated:
        if current_user.change_email(token):
            db.session.commit()
            flash('Your email was successfully updated!')
        else:
            flash('Your email failed to update, make sure your reset link is fresh! It only lasts for an hour!')
    else:
        flash('You have to be logged in to change your email.')
        return redirect(url_for('main.index'))

    return redirect(url_for('auth.account'))


@auth.route('/change_username', methods=['GET', 'POST'])
@login_required
def change_username():
    form = ChangeUsernameForm()
    if form.validate_on_submit():
        if current_user.is_authenticated and current_user.change_username(form.new_username.data):
            db.session.commit()
            return render_template('auth/account.html')
        else:
            flash('That username is already in use!')
    return render_template('auth/change_username.html', form=form)

@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.is_authenticated and current_user.verify_password(form.old_password.data):
            current_user.password = form.new_password.data
            db.session.add(current_user)
            db.session.commit()
            return render_template('auth/account.html')
        else:
            flash('The old password you entered was incorrect!')
    return render_template('auth/change_password.html', form=form)

@auth.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    form = ResetPasswordEmailForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_password_reset_token()
            send_email(user.email,
                       'Reset Your Password',
                       'auth/email/reset',
                       user=user,
                       token=token,
                       next=request.args.get('next'))
            flash('We sent you a link to reset your password. Go check your email!')
        else:
            flash("Weird...We don't have any record of an account using that email address!")
    return render_template('auth/reset_password.html', form=form)

@auth.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password_confirm(token):
    form = ResetPasswordForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.new_password.data):
            db.session.commit()
            flash('Your password has been updated!')
            return redirect(url_for('auth.login'))
        else:
            flash('Your password reset has failed, try again!')
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)



