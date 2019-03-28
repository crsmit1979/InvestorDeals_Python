from peewee import *
import datetime
import os

def get_db_file_path():
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))+"/../deals.db"
    #ROOT_DIR = "C:\Users\crsmit1979\PycharmProjects\DealFinder\deals.db"
    #ROOT_DIR = "../deals.db"
    print(ROOT_DIR)
    return ROOT_DIR

dbase = SqliteDatabase(get_db_file_path())

class DealBase(Model):
    uuid = BigAutoField(primary_key=True)
    #db.register_fields({'primary_key': 'BIGINT AUTOINCREMENT'})
    class Meta:
        database = dbase
