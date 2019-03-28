from peewee import *

from models.User import User
from models.Deal import Deal
from models.DealBase import DealBase


class Favourites(DealBase):
    deal = ForeignKeyField(Deal)
    user = ForeignKeyField(User)
    deleted = BooleanField(default=False)