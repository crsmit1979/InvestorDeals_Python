from components.formbuilder.validations import *
from components.formbuilder.uicomponents import *
from components.formbuilder.formbase import *
from components.formbuilder.formoutput import *

from models.DealType import DealType

class DealTypeForm(CustomFormBase):
    def __init__(self,request, endpoint_name,caption):
        CustomFormBase.__init__(self, request=request, endpoint_name=endpoint_name, caption=caption)
        self.uuid = FormHiddenField(id="uuid", label="ID", map_to_column="uuid", show_in_list=False)
        self.deal_type = FormCharField(id="deal_type", label="Deal Type", map_to_column="deal_type", validations=[])

    def on_get_list(self):
        dt = DealType.select()
        return dt


    def on_save(self, id):
        dt = DealType.get(DealType.uuid == str(id))
        dt.deal_type = self.deal_type.value
        dt.save()


    def on_edit(self, id):
        dt = DealType.get(DealType.uuid == str(id))
        return dt

    def on_delete(self, id):
        query = DealType.delete().where(DealType.uuid == str(id))
        query.execute()

    def on_insert(self):
        self.get_field_values_from_request()
        DealType.create(deal_type=self.deal_type.value)


    def custom_validation(self):
        #if self.gender.value == "F":
        #    self.gender.errors.append("Don't allow girls")
        pass

