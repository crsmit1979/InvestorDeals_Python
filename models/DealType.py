from peewee import *

from models.DealBase import DealBase


class DealType(DealBase):
    deal_type = CharField()

    @staticmethod
    def get_all():
        return DealType.select()

    @staticmethod
    def get_by_id(id):
        return DealType.get(DealType.id == int(id))