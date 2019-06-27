import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import operator
from flask_cors import CORS

from app import creat_app, db
from app.api import blueprint as api_bl
from app.dashboard.base.routes import blueprint as base_bl
from app.dashboard.home.routes import blueprint as home_bl
from app.dashboard.forms.routes import blueprint as forms_bl

app = creat_app(os.getenv('WATERING_ENV') or 'dev')


manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
CORS(app)

app.register_blueprint(api_bl)
app.register_blueprint(base_bl)
app.register_blueprint(home_bl)
app.register_blueprint(forms_bl)


# @app.after_request
# def after_request(response):
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     return response


@manager.command
@manager.option('-p', '--port', help='app port, default=5000')
def run(port=5000):
    host = os.environ.get('IP', '192.168.1.3')
    app.run(host=host, port=port)


@manager.command
def test():
    pass
    # import datetime
    # from app.api.model.user import User
    # # plants = Plant.query.all()
    # # print(plants)
    # admin = User(email='admin2@admin.com', username='admin2',
    #              password='admin', registered_on=datetime.datetime.utcnow(), role='admin'
    # , phone='12345678')
    # db.session.add(admin)
    # db.session.commit()
    # admins = User.query.filter_by(role='admin').all()
    # print(admins)
    from app.api.model.land import Plant

    plant = Plant(name='mango', water_amount=100, fertilizer='7mada')
    db.session.add(plant)
    db.session.commit()
    plants = Plant.query.all()
    print(plants)


if __name__ == "__main__":

    manager.run()
