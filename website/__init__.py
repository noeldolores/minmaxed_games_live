from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = "noeldolores$minmaxed_newworld"

def create_app():
  app = Flask(__name__)
  app.config.from_object("config.ProductionConfig")

  db.init_app(app)
  with app.app_context():
    db.create_all()

  from .views.newworld import newworld
  from .views.index import index

  app.register_blueprint(newworld, url_prefix='/newworld')
  app.register_blueprint(index, url_prefix='/')

  return app


app = create_app()
