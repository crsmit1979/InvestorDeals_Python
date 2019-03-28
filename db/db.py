import datetime
from models.DealPhoto import DealPhoto
from models.Favourites import Favourites
from models.Message import Message
from models.SignupUser import SignupUser
from models.Suggestions import Suggestions
from BatchCSV import BatchCSV, BatchCSVData
from models.Bedrooms import Bedrooms
from models.Deal import Deal
from models.DealBase import dbase
from models.DealQuestion import DealQuestion
from models.DealQuestionAnswer import DealQuestionAnswer
from models.DealType import DealType
from models.FAQ import FAQ
from models.User import User
from models.Reviews import Reviews
from models.Migration import Migrations


def initialize_db():
    #os.remove("deals.db")
    dbase.connect()
    dbase.drop_tables([Deal,User,DealType,DealQuestion,DealQuestionAnswer, SignupUser, Message, DealPhoto, Favourites,
                       BatchCSV, BatchCSVData, Suggestions, FAQ, Bedrooms, Reviews, Migrations],
                      safe=True)
    dbase.create_tables([Deal, User, DealType, DealQuestion, DealQuestionAnswer, SignupUser, Message,
                         DealPhoto, BatchCSV, BatchCSVData, Favourites, Suggestions, FAQ, Bedrooms, Reviews, Migrations],
                        safe=True)
    setup_test_data()

def setup_test_data():
    dt1 = DealType.create(deal_type="HMO")
    dt2 = DealType.create(deal_type="Land Development")
    dt3 = DealType.create(deal_type="R2R - HMO")
    dt4 = DealType.create(deal_type="R2R - SA")
    dt5 = DealType.create(deal_type="Buy to let")
    dt6 = DealType.create(deal_type="Commercial to Residentual")
    dt7 = DealType.create(deal_type="Lease Option")
    dt8 = DealType.create(deal_type="Other")
    dt9 = DealType.create(deal_type="Apartment Block")

    faq1 = FAQ.create(question="Question A", answer="Answer AA" )
    faq2 = FAQ.create(question="Question B", answer="Answer BB" )
    faq3 = FAQ.create(question="Question C", answer="Answer CC" )


    bedroom_not_applicable = Bedrooms.create(description="Not Applicable" )
    bedroomstudio = Bedrooms.create(description="Studio" )
    bedroom1 = Bedrooms.create(description="1 Bed" )
    bedroom2 = Bedrooms.create(description="2 Bed" )
    bedroom3 = Bedrooms.create(description="3 Bed" )
    bedroom4 = Bedrooms.create(description="4 Bed" )
    bedroom5 = Bedrooms.create(description="5 Bed" )
    bedroom6 = Bedrooms.create(description="6 Bed" )
    bedroom7 = Bedrooms.create(description="7 Bed" )
    bedroom8 = Bedrooms.create(description="8 Bed" )
    bedrooom_other = Bedrooms.create(description="More than 8" )

    desc = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean sed metus bibendum enim semper tempor vitae et neque. Integer lobortis lacus tortor. Fusce finibus hendrerit nunc sed vehicula. Sed dapibus lectus nec imperdiet faucibus. Mauris aliquet arcu nec quam aliquam, quis pharetra ipsum dapibus. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Etiam imperdiet ornare purus, vitae suscipit risus cursus ac. Etiam scelerisque imperdiet nibh, non condimentum nisl aliquam non. Donec quis nunc in diam convallis vulputate sed in purus. Aliquam venenatis ultrices imperdiet. Suspendisse consectetur leo id nisl consequat, in vestibulum tortor vehicula. Vestibulum eget elit condimentum, bibendum sem luctus, venenatis mi. Nam pellentesque molestie urna ut congue."

    inv1 = User.create(name="Richard", surname="Smit", telephone="07540388001", email="crsmit1979@gmail.com" ,
                       password="admin", activated=True, is_admin=True, disabled=False)
    inv2 = User.create(name="John", surname="Haagensen", telephone="07540388001", email="switzer.john@gmail.com" ,
                       password="admin", activated=True, disabled=True)

    dl1 = Deal.create(description=desc, title='Cheap SA', created=datetime.datetime(2018, 6, 13, 00, 00),
                      created_by=inv1, deal_type=dt1, sourcing_fee=2000, roi=10,
                      document="026d9108-6ec1-48b5-b7a4-ae02e2ff92e2.jpg" , county="Surrey", city="Shepperton",
                      address_line_1="304 Laleham Road", address_line_2="laleham road", postcode='tw17 0jq',
                      comparables = "xxxx",
                      key_features = "Feature 1, Feature 2, Feature 3",
                      show_address=True)
    dl2 = Deal.create(description=desc, title='2 Year D2V', created=datetime.datetime.now(),
                      created_by=inv1, deal_type=dt2 , county="Berkshire", city="Reading")
    dl3 = Deal.create(description=desc, title='HMO D2V', created=datetime.datetime.now(),
                      created_by=inv2, deal_type=dt2 , county="Berkshire", city="London")

    dq1 = DealQuestion.create(question="Is this D2V?", deal=dl1.uuid , asked_by=inv1.uuid)
    dqa1 = DealQuestionAnswer.create(answer="Yes it is", deal_question=dq1.uuid , answered_by=inv2.uuid)

    dq2 = DealQuestion.create(question="Can we view the property?", deal=dl1.uuid , asked_by=inv1.uuid)
    dqa2 = DealQuestionAnswer.create(answer="No", deal_question=dq2.uuid , answered_by=inv2.uuid)

    msg = Message.create(message_from=inv2, message_to=inv1, message="hello there" )

    df = DealPhoto.create(filename="026d9108-6ec1-48b5-b7a4-ae02e2ff92e2.jpg", deal=dl1.uuid )
    df2 = DealPhoto.create(filename="026d9108-6ec1-48b5-b7a4-ae02e2ff92e2.jpg", deal=dl1.uuid )
    df3 = DealPhoto.create(filename="026d9108-6ec1-48b5-b7a4-ae02e2ff92e2.jpg", deal=dl1.uuid )
    df4 = DealPhoto.create(filename="026d9108-6ec1-48b5-b7a4-ae02e2ff92e2.jpg", deal=dl1.uuid )

    fav = Favourites.create(deal=dl1.uuid , user=inv1.uuid)
    rev1 = Reviews.create(stars=3,
                          comment="test" ,
                          user=inv1.uuid)
    rev2 = Reviews.create(stars=5,
                          comment="test",
                          user=inv1.uuid)

    batch = BatchCSV.create(Filename="96249887-e751-4a1f-9b3d-05d5a24ecc46.csv" , Uploaded_By=inv1)