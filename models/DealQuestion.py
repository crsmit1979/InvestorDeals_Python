import datetime

from peewee import *

from models.DealBase import DealBase
from models.User import User
from models.Deal import Deal


class DealQuestion(DealBase):
    question = TextField()
    deal = ForeignKeyField(Deal, related_name="deal_question")
    asked_by = ForeignKeyField(User, related_name="asked_by")
    asked_date = DateTimeField(default=datetime.datetime.now())

    @staticmethod
    def get_by_uuid(uuid):
        return DealQuestion.get(DealQuestion.uuid == uuid)
