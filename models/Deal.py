from peewee import *
from models.DealBase import DealBase
from models.DealType import DealType
from models.User import User
from models.Bedrooms import Bedrooms

class Deal(DealBase):
    title = CharField()
    description = CharField()
    document = CharField(null=True)
    deal_type = ForeignKeyField(DealType, backref="deal_type_id",  null=True)
    sourcing_fee = DoubleField(default=0)
    key_features = CharField(null=True)
    comparables = CharField(null=True)
    created = DateTimeField()
    created_by = ForeignKeyField(User)
    roi = DoubleField(default=0)
    deleted = BooleanField(default=False)
    address_line_1 = TextField(null=True)
    address_line_2 = TextField(null=True)
    county = TextField(null=True)
    city = TextField(null=True)
    postcode = TextField(null=True)
    show_address = BooleanField(default=False)
    bedrooms = ForeignKeyField(Bedrooms, backref="bedroom_id", null=True)

    @staticmethod
    def get_deals_created_by_user(userid):
        return Deal.select() \
            .where(Deal.created_by_id == userid)

    @staticmethod
    def get_by_id(id):
        return Deal.get(Deal.id == int(id))

    @staticmethod
    def get_by_uuid(uuid):
        return Deal.get(Deal.uuid == uuid)

    @staticmethod
    def delete_by_id(id):
        query = Deal.delete().where(Deal.id == id)
        query.execute()

    @staticmethod
    def available_counties():
        return Deal.select().where(Deal.deleted == False).select(Deal.county).distinct()

    @staticmethod
    def available_cities():
        return Deal.select().where(Deal.deleted == False).select(Deal.city).distinct()

    @staticmethod
    def filter(deal_type_id=None, filter_city=None, filter_county=None):
        rows = Deal.select()
        if deal_type_id != "" and deal_type_id is not None:
            rows = rows.where(Deal.deal_type == str(deal_type_id), Deal.deleted == False)

        if filter_city is not None and filter_city != "":
            rows = rows.where(Deal.city == str(filter_city), Deal.deleted == False)
        if filter_county is not None and filter_county != "":
            rows = rows.where(Deal.county == str(filter_county), Deal.deleted == False)

        return rows