import os
from dotenv import load_dotenv

class Config(object):
  DEBUG = False
  TESTING = False
  load_dotenv()
  SECRET_KEY = os.getenv("SECRET_KEY")


class DevelopmentConfig(Config):
  DEBUG = True
  TESTING = True
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  DB_NAME = "database.db"
  load_dotenv()
  SECRET_KEY = os.getenv("SECRET_KEY")


class ProductionConfig(Config):
  DEBUG = False
  TESTING = False
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="noeldolores",
    password="ST2TuTrbgmP8d",
    hostname="noeldolores.mysql.pythonanywhere-services.com",
    databasename="noeldolores$minmaxed_newworld"
  )
  load_dotenv()
  SECRET_KEY = os.getenv("SECRET_KEY")