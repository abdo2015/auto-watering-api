import flask
from flask import jsonify, render_template, redirect, request, url_for
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)

from app import db, login_manager
from app.dashboard.base import blueprint
from app.dashboard.base.forms import LoginForm, CreateAccountForm
from app.api.model.user import User


@blueprint.route('/')
def route_default():
    return redirect(url_for('base_blueprint.login'))


@blueprint.route('/<template>')
@login_required
def route_template(template):
    try:
        re = render_template(template + '.html')
        return re
    except Exception:
        return render_template('errors/page_404.html'), 404


@blueprint.route('/fixed_<template>')
@login_required
def route_fixed_template(template):
    return render_template('fixed/fixed_{}.html'.format(template))


@blueprint.route('/page_<error>')
def route_errors(error):
    return render_template('errors/page_{}.html'.format(error))

# Login & Registration


@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if 'login' in request.form:
        email = request.form['email']
        password = request.form['password']
        admin = User.query.filter_by(email=email).first()
        if admin and admin.isAdmin and admin.check_password(password):
            login_user(admin)
            flask.flash('Logged in successfully.')
            return redirect(url_for('base_blueprint.route_default'))
        return render_template('errors/page_403.html')
    if not current_user.is_authenticated:
        return render_template(
            'login/login.html',
            login_form=login_form,
        )
    return redirect(url_for('home_blueprint.route_template'))


# @blueprint.route('/create_user', methods=['POST'])
# def create_user():
#     user = User(**request.form)
#     db.session.add(user)
#     db.session.commit()
#     return jsonify('success')


@login_required
def logout():
    logout_user()
    return redirect(url_for('base_blueprint.login'))


@blueprint.route('/logout')
@blueprint.route('/shutdown')
def shutdown():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server shutting down...'

# Errors


# @blueprint.unauthorized_handler
# def unauthorized_handler():
#     return render_template('errors/page_403.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('errors/page_403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('errors/page_404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('errors/page_500.html'), 500
