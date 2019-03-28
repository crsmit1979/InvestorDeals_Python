from peewee import *

from models.DealBase import DealBase


class Suggestions(DealBase):
    name = CharField(null=False)
    email= CharField(null=False)
    comment = CharField(null=True)
    ip_address= CharField(null=False)
    date_posted = DateTimeField()

    def get_id(self):
        return str(self.uuid)