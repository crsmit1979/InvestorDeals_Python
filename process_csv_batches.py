import csv
import datetime
import os
import uuid

from BatchCSV import BatchCSV, BatchCSVData
from models.Deal import Deal
from models.DealBase import dbase
from models.DealType import DealType


def process_batches():
    rows = BatchCSV.select()
    for row in rows:
        csv_file = os.path.join("./files/csv", row.Filename)
        with open(csv_file, 'rb') as fl:
            next(fl)
            rd = csv.reader(fl, delimiter='|', quotechar=' ')
            for r in rd:
                title= r[0]
                description = r[1]
                sourcing_fee = r[2]
                roi = r[3]
                address_1 = r[4]
                address_2 = r[5]
                county = r[6]
                city = r[7]
                postcode=r[8]
                dealtype=r[9]
                show_address =r[10]

                dealtypes = DealType.select(DealType.deal_type)
                types= [c.deal_type for c in dealtypes]
                errors = []
                if (title == ""):
                    errors.append("Title cannot be empty")
                if (description == ""):
                    errors.append("Description cannot be empty")
                if show_address.lower() == "true" or show_address.lower()=="1":
                    show_address=True
                else:
                    show_address=False
                dtype = None
                if (dealtype not in types):
                    errors.append("Deal type not found ["+dealtype+"]")
                else:
                    dtype = DealType.select().where(DealType.deal_type==dealtype)[0]
                if (city == ""):
                    errors.append("City cannot be empty")
                if (county == ""):
                    errors.append("County cannot be empty")

                BatchCSVData.create(Title=title,
                                    Description = description,
                                    Sourcing_Fee = sourcing_fee,
                                    ROI = roi,
                                    Address_Line_1 = address_1,
                                    Address_Line_2 = address_2,
                                    County = county,
                                    City = city,
                                    PostCode = postcode,
                                    DealType = dealtype,
                                    DealTypeObj = dtype.uuid,
                                    Batch = row,
                                    Is_Error = False if len(errors) == 0 else True,
                                    Errors = ", ".join(errors),
                                    Show_Address = bool(show_address),
                                    uuid = uuid.uuid4())

def load_successfull_entries():
    rows = BatchCSVData.select().where(BatchCSVData.Is_Error==False, BatchCSVData.Processed == False)
    for row in rows:
        dt = DealType.get(DealType.uuid == row.DealTypeObj_id)
        dl1 = Deal.create(description=row.Description,
                          title=row.Title,
                          created=datetime.datetime.now(),
                          created_by=row.Batch.Uploaded_By,
                          deal_type=dt,
                          sourcing_fee=row.Sourcing_Fee,
                          roi=row.ROI,
                          document=None,
                          uuid=uuid.uuid4(),
                          county=row.County,
                          city=row.City,
                          address_line_1=row.Address_1,
                          address_line_2=row.Address_2,
                          postcode=row.Postcode,
                         show_address=row.Show_Address)
        row.Processed = True;
        row.Date_Processed = datetime.datetime.now()
        row.save()
dbase.execute_sql("delete  from batchcsvdata")
process_batches()
load_successfull_entries()