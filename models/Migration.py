from peewee import *

from models.DealBase import DealBase


class Migrations(DealBase):
    file = CharField(null=False)
    date_run = DateTimeField(null=False)

