import datetime

from peewee import *

from models.DealBase import DealBase
from models.User import User
from models.DealQuestion import DealQuestion


class DealQuestionAnswer(DealBase):
    answer = TextField()
    answered_by = ForeignKeyField(User, related_name="answered_by")
    answered_date = DateTimeField(default=datetime.datetime.now())
    deal_question = ForeignKeyField(DealQuestion, related_name="deal_question_answer")
