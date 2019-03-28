import datetime

from peewee import *

from models.User import User
from models.DealBase import DealBase


class Message(DealBase):
    message_from = ForeignKeyField(User, related_name="message_from_id")
    message_to = ForeignKeyField(User, related_name="message_to_id")
    message = TextField(null=False)
    created = DateTimeField(default=datetime.datetime.now())
    date_read = DateTimeField(null=True)
    deleted = BooleanField(default=False)

    @staticmethod
    def delete(uuid):
        message = Message.get(Message.uuid == uuid)
        message.deleted = True
        message.save()

    @staticmethod
    def set_message_as_read(uuid):
        message = Message.get(Message.uuid == uuid)
        message.date_read = datetime.datetime.now()
        message.save()
        return message

    @staticmethod
    def get_user_messages(user_uuid):
        return Message.select() \
            .where(
            (Message.message_from == user_uuid) | (Message.message_to == user_uuid) & (
            Message.deleted == False))
