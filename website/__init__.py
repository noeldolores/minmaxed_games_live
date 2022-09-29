from flask import Flask

def create_app():
  app = Flask(__name__)
  
  app.config.from_object("config.DevelopmentConfig")
  
  
  from .views import views
  app.register_blueprint(views, url_prefix='/')
  
  return app