from components.formbuilder.validations import *
from components.formbuilder.uicomponents import *
from components.formbuilder.formbase import *
from components.formbuilder.formoutput import *

from models.User import User

class ProfileForm(CustomFormBase):
    def __init__(self,request, endpoint_name,caption):
        CustomFormBase.__init__(self, request=request, endpoint_name=endpoint_name, caption=caption)
        self.uuid = FormHiddenField(id="uuid", label="Id", map_to_column="uuid", show_in_list=False, order=0)
        self.firstname = FormCharField(id="name", label="Name", map_to_column="name", order=1, format_output=YesNo_Output)
        self.surname = FormCharField(id="surname", label="Surname", map_to_column="surname", order=2)
        self.telephone = FormCharField(id="telehphone", label="Telephone", map_to_column="telephone", order=3)
        self.email = FormCharField(id="email", label="Email", map_to_column="email", order=4)

        self.company_name = FormCharField(id="company_name", label="Company name", map_to_column="company_name", order=5, show_in_list=False)
        self.company_registration_number = FormCharField(id="company_registration_number", label="Registration Number", map_to_column="company_registration_number", order=6, show_in_list=False, align="center")
        self.company_address_line_1 = FormCharField(id="company_address_line_1", label="Address Line 1", map_to_column="company_address_line_1", order=7, show_in_list=False)
        self.company_address_line_2 = FormCharField(id="company_address_line_2", label="Address Line 2", map_to_column="company_address_line_2", order=8, show_in_list=False)
        self.company_address_city = FormCharField(id="company_address_city", label="City", map_to_column="company_address_city", order=9, show_in_list=False)
        self.company_address_postcode = FormCharField(id="company_address_postcode", label="Postcode", map_to_column="company_address_postcode", order=9, show_in_list=False)

        self.property_redress_number = FormCharField(id="property_redress_number", label="Property Redress Scheme", map_to_column="property_redress_number", order=10, show_in_list=False, align="center", tooltip="Property Redress Scheme registration number")
        self.money_laundering_number = FormCharField(id="money_laundering_number", label="Money Laundering Number", map_to_column="money_laundering_number", order=11, show_in_list=False, align="center", tooltip="Registration number for Anti-Money Laundering")
        self.ico_number = FormCharField(id="ico_number", label="ICO Number", map_to_column="ico_number", order=12, show_in_list=False, align="right", tooltip="Registration number for data protection")

    def on_get_list(self):
        users = User.select()
        return users

    def on_edit(self, id):
        user = User.get(User.uuid == id)
        return user

    def on_save(self, id):
        user = User.get(User.uuid == id)
        user.name = self.firstname.value
        user.surname = self.surname.value
        user.telephone = self.telephone.value
        user.email = self.email.value
        user.company_registration_number = self.company_registration_number.value
        user.company_address_city = self.company_address_city.value
        user.company_address_line_1 = self.company_address_line_1.value
        user.company_address_line_2 = self.company_address_line_2.value
        user.money_laundering_number = self.money_laundering_number.value
        user.ico_number = self.ico_number.value
        user.property_redress_number = self.property_redress_number.value
        user.company_address_postcode = self.company_address_postcode.value
        user.save()
        return render_template("testform.html", type='form', form=self)

    def on_delete(self, id):
        query = User.delete().where(User.uuid == str(id))
        query.execute()

    def on_add(self):
        self.get_field_values_from_request()
        print("posting form")
        return redirect("/"+self.endpoint_name+"/list")

