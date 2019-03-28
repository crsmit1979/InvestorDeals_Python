from peewee import *

from models.DealBase import DealBase


class SignupUser(DealBase):
    name = CharField(null=False)
    surname = CharField(null=False)
    email = CharField(null=False)
    typeofdeal = CharField(null=False)
    location=TextField(null=True)
    otherdealtype=CharField(null=True)
    investor=BooleanField(default=False)
    sourcer=BooleanField(default=False)

    @staticmethod
    def get_all():
        return SignupUser.select()