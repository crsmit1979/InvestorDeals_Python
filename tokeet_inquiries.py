import csv
import datetime
import urllib2
import uuid
from datetime import datetime

from peewee import *

from models.DealBase import DealBase, dbase


class Inquiry(DealBase):
    Name = TextField(null=True)
    Email = TextField(null=True)
    Rental = TextField(null=True)
    Arrive = DateField(null=True)
    Depart = DateField(null=True)
    Received = DateField(null=True)
    Checkin = TimeField(null=True)
    Checkout = TimeField(null=True)
    BookingID = TextField(null=True)
    InquiryID = TextField(null=False)
    Source = TextField(null=True)
    Booked = TextField(null=True)
    Adults = TextField(null=True)
    Children = TextField(null=True)
    Price = DoubleField(null=True)

def initialize_db():
    dbase.connect()
    dbase.drop_tables([Inquiry], safe=True)
    dbase.create_tables([Inquiry], safe=True)

initialize_db()

url = "https://datafeed.tokeet.com/v1/inquiry/1516269000.1485/aa93a986-21f4-4aaf-ae72-5aa84bc6b8df/5f2cc77d-5679-463d-a2cd-ab029f4c9bee/1527759580"

response = urllib2.urlopen(url)
cr = csv.reader(response)
next(cr)

def convert_string_to_date_time(dt, tm):
    return datetime.datetime.strptime(dt+" "+tm,'%Y-%m-%d %H:%M')

def convert_string_to_date(dt):
    return datetime.datetime.strptime(dt,'%Y-%m-%d')

def convert_string_to_time(dt):
    return datetime.datetime.strptime(dt,'%H:%M')

def load_tokeet_inquiries():
    for row in cr:
        rec = Inquiry.create(
            uuid = uuid.uuid4(),
            Name = row[0],
            Email = row[1],
            Rental = row[2],
            Arrive = convert_string_to_date(row[3]),
            Depart = convert_string_to_date(row[4]),
            Received = convert_string_to_date(row[5]),
            Checkin = convert_string_to_time(row[6]),
            Checkout = convert_string_to_time(row[7]),
            BookingID = row[8],
            InquiryID = row[9],
            Source = row[10], #airbnb, Booking.com, tokeet, Expedia.com
            Booked = row[11], #Yes/No
            Adults = row[12],
            Children = row[13],
            Price =float(row[14])
        )


load_tokeet_inquiries()
"""

stripe.api_key = "sk_test_rEvNUIpDfR7UFMNkZsJBYbhf"


def get_customer_id_from_stripe(email):
    customers =  stripe.Customer.list(limit=30)
    for d in customers.data:
        if (email == d['email']):
            return d["id"]
    return None

#print(get_customer_id_from_stripe("crsmit1979@gmail.com"))
#charges = stripe.Charge.list(limit=100)
#for charge in charges:
#    customer_id = 'cus_D8DRitKj0iOmnL'
#    if(charge['customer'] == customer_id):
#        print (charge['amount'])

class Stripe_Charge(object):
    def __init__(self):
        self.amount = 0
        self.paid = False

    def populate(self, obj, stripeData):
        self.amount=obj['amount']
        self.paid=obj['paid']

class Stripe_Customer(object):
    def __init__(self):
        self.customer_id = ""
        self.email = ""
        self.charges = []

    def populate(self, obj, stripeData):
        self.email = obj['email']
        self.customer_id = obj['id']

        for charge in stripeData.list_charges:
            if(charge['customer'] == self.customer_id):
                ch = Stripe_Charge()
                ch.populate(charge, stripeData)
                self.charges.append(ch)


class StripeData(object):
    def __init__(self):
        self.list_customers = ""
        self.list_charges = ""
        self.customers = []
    def load_data(self):
        self.list_customers = stripe.Customer.list(limit=100)
        self.list_charges = stripe.Charge.list(limit=100)
        self.set_data()

    def set_data(self):
        for r in self.list_customers.data:
            c = Stripe_Customer()
            c.populate(r, self)
            self.customers.append(c)



cls = StripeData()
cls.load_data()
print(cls.list_charges)
for c in cls.customers:
    print(c.customer_id+" = "+c.email)
    for ch in c.charges:
        print("   Amount: %s" % (ch.amount))

"""