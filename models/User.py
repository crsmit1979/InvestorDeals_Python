from flask_login import UserMixin
from peewee import *

from models.DealBase import DealBase

class User(UserMixin, DealBase):
    name = CharField()
    surname = CharField()
    telephone = CharField(null=True, default="")
    company_name = CharField(null=True, default="")
    company_registration_number = CharField(null=True, default="")
    company_address_line_1 = CharField(null=True, default="")
    company_address_line_2 = CharField(null=True, default="")
    company_address_postcode = CharField(null=True, default="")
    company_address_city = CharField(null=True, default="")
    email = CharField(null=True)
    password = CharField(null=True)
    last_login = DateTimeField(null=True)
    login_attempts = IntegerField(default=0)
    activated = BooleanField(default=False)
    is_admin = BooleanField(default=False)
    disabled = BooleanField(default=False)
    oauth_id = CharField(null=True)
    oauth_profile_image = CharField(null=True,default="")
    oauth_xml = CharField(null=True, default="")
    property_redress_number = CharField(null=True, default="")
    money_laundering_number = CharField(null=True, default="")
    ico_number = CharField(null=True, default="")

    def get_id(self):
        return str(self.uuid)

    @staticmethod
    def disabled_user(user_uuid):
        user = User.get(User.uuid == user_uuid)
        user.disabled = True
        user.save()

    @staticmethod
    def enabled_user(user_uuid):
        user = User.get(User.uuid == user_uuid)
        user.disabled = False
        user.save()

    @staticmethod
    def activate_user(user_uuid):
        usr = User.get(User.uuid == user_uuid)
        usr.activated = True
        usr.save()
        return usr

    @staticmethod
    def change_password(user_uuid, new_password):
        usr = User.get_by_uuid(user_uuid)
        usr.password = new_password
        usr.save()
        return usr

    @staticmethod
    def get_all():
        return User.select()

    @staticmethod
    def get_by_oauth(oauth_userid):
        return User.get(User.oauth_id == str(oauth_userid))


    @staticmethod
    def get_by_uuid(uuid):
        return User.get(User.uuid == uuid)

    @staticmethod
    def get_user_by_email(email):
        return User.get(User.email == email)