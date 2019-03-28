import datetime

from peewee import *

from models.DealBase import DealBase
from models.User import User


class BatchCSV(DealBase):
    Upload_Date = DateTimeField(default=datetime.datetime.now(), null=False)
    Uploaded_By = ForeignKeyField(User, null=False)
    Filename = TextField(null=False)

class BatchCSVData(DealBase):
    Batch = ForeignKeyField(BatchCSV)
    Title = TextField(null=False)
    Description = TextField(null=False)
    Sourcing_Fee = TextField(null=False)
    ROI = TextField(null=True)
    Address_1 = TextField(null=True)
    Address_2 = TextField(null=True)
    County = TextField(null=True)
    City = TextField(null=True)
    Postcode = TextField(null=True)
    DealType = TextField(null=True)
    Errors = TextField(null=True)
    Is_Error = BooleanField(default=False)
    Processed = BooleanField(default=False)
    Date_Processed = DateTimeField(null=True)
    DealTypeObj = ForeignKeyField(DealType, null=True)
    Show_Address = BooleanField(default=False)