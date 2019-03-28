from components.formbuilder.validations import *
from components.formbuilder.uicomponents import *
from components.formbuilder.formbase import *
from components.formbuilder.formoutput import *

from models.FAQ import FAQ

class FAQForm(CustomFormBase):
    def __init__(self,request, endpoint_name,caption):
        CustomFormBase.__init__(self, request=request, endpoint_name=endpoint_name, caption=caption)
        self.uuid = FormHiddenField(id="uuid", label="ID", map_to_column="uuid", show_in_list=False)
        self.question = FormCharField(id="question", label="Question", map_to_column="question", validations=[])
        self.answer = FormCharField(id="answer", label="Answer", map_to_column="answer", validations=[])

    def on_get_list(self):
        dt = FAQ.select()
        return dt


    def on_save(self, id):
        dt = FAQ.get(FAQ.uuid == str(id))
        dt.question = self.question.value
        dt.answer = self.answer.value
        dt.save()


    def on_edit(self, id):
        dt = FAQ.get(FAQ.uuid == str(id))
        return dt

    def on_delete(self, id):
        query = FAQ.delete().where(FAQ.uuid == str(id))
        query.execute()

    def on_insert(self):
        self.get_field_values_from_request()
        FAQ.create(question=self.question.value, answer=self.answer.value)

    def on_post(self, form):
        print("add my own posting code here")
        dt = FAQ.get(FAQ.uuid == request.form.get("uuid"))
        dt.question = form.question.value
        dt.answer = form.answer.value
        dt.save()


    def custom_validation(self):
        #if self.gender.value == "F":
        #    self.gender.errors.append("Don't allow girls")
        pass
