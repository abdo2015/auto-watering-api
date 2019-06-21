import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import creat_app, db
from app.api import blueprint as api_bl

app = creat_app(os.getenv('WATERING_ENV') or 'dev')


manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

app.register_blueprint(api_bl)


@manager.command
@manager.option('-p', '--port', help='app port, default=5000')
def run(port=5000):
    app.run(port=port)


if __name__ == "__main__":

    manager.run()
