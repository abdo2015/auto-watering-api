from app.dashboard.home import blueprint
from flask import render_template, redirect, url_for
from flask_login import login_required
import traceback
from app.api.model.user import User
from app.api.model.land import Land, Plant
from app import db


# @blueprint.route('')
# @login_required
# def index():
#     return render_template('home.html')

@blueprint.route('')
@blueprint.route('/<template>')
@login_required
def route_template(template='home'):
    num_of_users = User.query.filter_by(role='user').count()
    num_of_lands = Land.query.count()
    num_of_plants = Plant.query.count()
    num_of_admins = User.query.count() - num_of_users
    users_data = User.query.filter_by(role='user')
    admin_data = User.query.filter_by(role='admin')
    plants_data = Plant.query.all()
    kwargs = dict(users=num_of_users, lands=num_of_lands,
                  plants=num_of_plants, admins=num_of_admins, users_data=users_data,
                  admin_data=admin_data, plants_data=plants_data)
    template = template + '.'
    try:
        re = render_template(template + 'html', kwargs=kwargs)
        return re
    except Exception:
        # traceback.print_exc()
        return render_template('errors/page_404.html'), 404

    # return render_template('home.html', kwargs=kwargs)


@blueprint.route('/delUser/<user_id>')
def delUser(user_id):
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('home_blueprint.route_template'))


@blueprint.route('/delAdmin/<admin_id>')
def delAdmin(admin_id):
    admin = User.query.filter_by(id=admin_id).first()
    db.session.delete(admin)
    db.session.commit()
    return redirect(url_for('home_blueprint.route_template'))


@blueprint.route('/delPlant/<plant_id>')
def delPlant(plant_id):
    print(plant_id)
    plant = Plant.query.filter_by(id=plant_id).first()
    print(plant)
    db.session.delete(plant)
    db.session.commit()
    return redirect(url_for('home_blueprint.route_template'))


@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('errors/page_403.html'), 403


@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('errors/page_404.html'), 404


@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('errors/page_500.html'), 500
