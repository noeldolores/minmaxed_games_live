import os
from dotenv import load_dotenv

class Config(object):
  DEBUG = False
  TESTING = False
  SECRET_KEY = "KYgnCVSJldpIKFvPV7p6JVQa2U5_AZiZ"
  
  
class DevelopmentConfig(Config):
  DEBUG = True