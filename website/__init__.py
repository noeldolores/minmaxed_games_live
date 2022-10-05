from flask import Flask

def create_app():
  app = Flask(__name__)
  
  app.config.from_object("config.DevelopmentConfig")
  
  
  from .views.newworld import newworld
  from .views.index import index
  
  app.register_blueprint(newworld, url_prefix='/newworld')
  app.register_blueprint(index, url_prefix='/')

  return app