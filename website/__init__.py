from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy(session_options={"autoflush": False})
DB_NAME = "noeldolores$minmaxed_newworld"
#DB_NAME = "database.db" 
  
def create_app():
  app = Flask(__name__)
  app.config.from_object("config.ProductionConfig")
  
  db.init_app(app)
  
  from .views.newworld import newworld
  from .views.index import index
  
  app.register_blueprint(newworld, url_prefix='/newworld')
  app.register_blueprint(index, url_prefix='/')

  create_database(app)
  
  return app


# def create_database(app):
#   if not path.exists('website/' + DB_NAME):
#     db.create_all(app=app)
#     print('Created Database!')

def create_database(app):
  db.create_all(app=app)
  
app = create_app()
create_database(app)