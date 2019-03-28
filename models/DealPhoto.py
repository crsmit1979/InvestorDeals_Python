from peewee import *

from models.Deal import Deal
from models.DealBase import DealBase


class DealPhoto(DealBase):
    filename = CharField(null=False)
    deal = ForeignKeyField(Deal, backref="photos")

    @staticmethod
    def get_photos_by_deal_id(id):
        return DealPhoto.select().where(DealPhoto.deal_id == id)
