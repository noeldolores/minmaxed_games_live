import os
from dotenv import load_dotenv

class Config(object):
  DEBUG = False
  TESTING = False
  load_dotenv()
  SECRET_KEY = os.getenv("SECRET_KEY")
  
  
class DevelopmentConfig(Config):
  DEBUG = True
  load_dotenv()
  SECRET_KEY = os.getenv("SECRET_KEY")
  
  
class ProductionConfig(Config):
  DEBUG = False
  TESTING = False
  load_dotenv()
  SECRET_KEY = os.getenv("SECRET_KEY")
  
  