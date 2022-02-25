from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')
DB_USER = config['DATABASE']['USER']
DB_PW = config['DATABASE']['PW']
DB_ADDRESS = config['DATABASE']['ADDRESS']
DB_PORT = config['DATABASE']['PORT']
DB_NAME = config['DATABASE']['NAME']

EMAIL_USER = config['EMAIL']['USER']
EMAIL_PW = config['EMAIL']['PW']
EMAIL_SERVER = config['EMAIL']['SERVER']
EMAIL_PORT = config['EMAIL']['PORT']

WEBSITE_URL = config['WEBSITE']['URL']
WEBSITE_PORT = config['WEBSITE']['PORT']
