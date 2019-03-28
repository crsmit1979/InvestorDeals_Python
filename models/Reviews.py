from peewee import *

from models.DealBase import DealBase
from models.User import  User

class Reviews(DealBase):
    stars = IntegerField()
    comment = CharField()
    user = ForeignKeyField(User, related_name="user")
