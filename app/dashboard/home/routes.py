from app.dashboard.home import blueprint
from flask import render_template
from flask_login import login_required

from app.api.model.user import User
from app.api.model.land import Land, Plant


@blueprint.route('/index')
@login_required
def index():
    return render_template('index.html')


@blueprint.route('/<template>')
@login_required
def route_template(template):
    num_of_users = User.query.filter_by(role='user').count()
    num_of_lands = Land.query.count()
    num_of_plants = Plant.query.count()
    kwargs = dict(users=num_of_users, lands=num_of_lands, plants=num_of_plants)
    return render_template(template + '.html', kwargs=kwargs)
