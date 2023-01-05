from .database import Database
import os.path

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = 'main.db'

db = Database(BASE_DIR + '/' + DB_NAME)
