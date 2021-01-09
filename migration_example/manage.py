import config
from flask_migrate import Migrate, Manager, MigrateCommand
from app import app, db

from models import UserModel

migrate = Migrate(app, db)
app.config.from_object(config.StagingConfig)


migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()

