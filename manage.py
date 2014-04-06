from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.assets import ManageAssets
from livereload import Server

from gather import create_app
from gather.extensions import db

app = create_app()
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command("db", MigrateCommand)
manager.add_command("assets", ManageAssets())


@manager.command
def create_all():
    db.create_all()


@manager.command
def clear_cache():
    from gather.extensions import cache
    with app.app_context():
        cache.clear()


@manager.command
def clean_junk_users():
    from gather.account.models import Account
    with app.app_context():
        Account.clean_junk_users()


@manager.command
def livereload():
    db.create_all()
    app.debug = True
    server = Server(app)
    server.watch("gather/*.py")
    server.watch("gather/templates/*.html")
    server.watch("gather/assets/stylesheets/*.sass")
    server.watch("gather/assets/stylesheets/*/*.sass")
    server.watch("gather/assets/javascripts/*.coffee")
    server.serve(port=8000)

if __name__ == "__main__":
    manager.run()
