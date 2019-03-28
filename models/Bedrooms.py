from peewee import *

from models.DealBase import DealBase


class Bedrooms(DealBase):
    description = CharField(null=False, default="")

    def get_id(self):
        return str(self.uuid)


