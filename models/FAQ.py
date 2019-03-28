from peewee import *

from models.DealBase import DealBase


class FAQ(DealBase):
    question = CharField(null=False, default="")
    answer = CharField(null=False, default="")

    def get_id(self):
        return str(self.uuid)


