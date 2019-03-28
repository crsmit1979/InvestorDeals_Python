from components.formbuilder.validations import *
from components.formbuilder.uicomponents import *
from components.formbuilder.formbase import *
from components.formbuilder.formoutput import *
from flask_login import current_user

from models.Bedrooms import  Bedrooms
from models.DealType import DealType
from models.Deal import Deal
from models.DealPhoto import  DealPhoto

class AddDealForm(CustomFormBase):
    def __init__(self,request, endpoint_name,caption):
        CustomFormBase.__init__(self, request=request, endpoint_name=endpoint_name, caption=caption)
        bedroom_list = Bedrooms.select()
        deal_type_list = DealType.select()

        self.header1 = FormHeader(label='Property Details', order=0.2)
        self.title = FormCharField(id="title", label="Title", map_to_column="title", order=1, validations=[NotEmpty_Validation])
        self.description = FormCharField(id="description", label="Description", map_to_column="description", order=2, show_in_list=False, validations=[NotEmpty_Validation])
        self.deal_type = FormDropdownField(id="deal_type", label="Type of Deal", map_to_column="deal_type", order=2.3,  data=deal_type_list, id_field="uuid", value_field="deal_type", validations=[NotEmpty_Validation])
        self.seperator = FormSeperator(order=2.1)

        self.header1 = FormHeader(label='Address', order=2.2)
        self.address_line_1 = FormCharField(id="address_line_1", label="Address 1", map_to_column="address_line_1", order=3, show_in_list=False)
        self.address_line_2 = FormCharField(id="address_line_2", label="Address 2", map_to_column="address_line_2", order=4, show_in_list=False)
        self.county = FormCharField(id="county", label="County", map_to_column="county", order=5, show_in_list=False, validations=[NotEmpty_Validation])
        self.city = FormCharField(id="city", label="City", map_to_column="city", order=6, show_in_list=True, validations=[NotEmpty_Validation])
        self.postcode = FormCharField(id="postcode", label="Postcode", map_to_column="postcode", order=7, show_in_list=False)
        self.show_address = FormCheckboxField(id="show_address", label="Show Address", map_to_column="show_address", order=8, show_in_list=False)
        self.bedrooms = FormDropdownField(id="bedrooms", label="Number of Bedrooms", map_to_column="bedrooms", order=9, show_in_list=False, data=bedroom_list, id_field="uuid", value_field="description", validations=[NotEmpty_Validation])

        self.header2 = FormHeader(label='Investor Details', order=9.1)
        self.sourcing_fee = FormCharField(id="sourcing_fee", label="Sourcing Fee", map_to_column="sourcing_fee", order=10, show_in_list=False)
        self.roi = FormCharField(id="roi", label="ROI", map_to_column="roi", order=11, show_in_list=False, validations=[IsPercentage_Validation])
        self.document = FormUploadField(id="document", label="Document", map_to_column="document", request=self.request, order=12, show_in_list=False, save_to_directory="./files/document")
        self.photos = FormUploadField(id="photos", label="Photos", order=13, show_in_list=False, request=self.request, allow_multiple=True, save_to_directory="./files/dealphotos")

    def on_get_list(self):
        return Deal.select().where((Deal.deleted == False), (Deal.created_by_id == current_user.uuid))

    def on_edit(self, id):
        return Deal.get(Deal.uuid == str(id))

    def on_insert(self):
        self.get_field_values_from_request()
        saved_docs = self.document.save_file()
        dl = Deal.create(
            title = self.title.value,
            description = self.description.value,
            created_by = current_user.uuid,
            created = datetime.datetime.now(),
            sourcing_fee = self.sourcing_fee.value,
            roi = self.roi.value,
            deal_type_id = self.deal_type.value,
            document = saved_docs[0] if len(saved_docs)>0 else None,
            county = self.county.value,
            city = self.city.value,
            address_line_1 = self.address_line_1.value,
            address_line_2 = self.address_line_2.value,
            postcode = self.postcode.value,
            show_address = self.show_address.get_value(),
            bedrooms = self.bedrooms.value
        )
        saved_pics = self.photos.save_file()
        for pic in saved_pics:
            ph = DealPhoto.create(filename=pic, deal=dl.uuid)

    def on_save(self, id):
        dt = Deal.get(Deal.uuid == str(id))
        dt.title = self.title.value
        dt.description = self.description.value
        dt.sourcing_fee = self.sourcing_fee.value
        dt.roi = self.roi.value
        dt.address_line_1 = self.address_line_1.value
        dt.address_line_2 = self.address_line_2.value
        dt.county = self.county.value
        dt.city = self.city.value
        dt.postcode = self.postcode.value
        dt.show_address = self.show_address.value
        dt.bedrooms = self.bedrooms.value
        dt.save()
        return redirect("/" + self.endpoint_name + "/list")

    def on_delete(self, id):
        query = Deal.delete().where(Deal.uuid == str(id))
        query.execute()
        return redirect("/"+self.endpoint_name+"/list")

