from components.formbuilder.formbase import  CustomFormBase
from models.DealType import  DealType
from components.formbuilder.uicomponents import FormCharField

class mock_form():
    def get(self, fieldname):
        testdata = create_test_data()
        return getattr(testdata,fieldname)

class mock_request():
    form  = mock_form()


def test_constructor():
    #GIVEN
    sub_text = "sub text"
    method = "POST"
    action = "/test"
    caption = "caption"
    endpoint_name = "/endpoint"

    mock_req = mock_request()
    #WHEN
    itm = CustomFormBase(request=mock_request, endpoint_name=endpoint_name, caption=caption, method=method, action=action, sub_text=sub_text)

    #THEN
    assert itm.sub_text == sub_text
    assert itm.caption == caption
    assert itm.method == method
    assert itm.action == action
    assert itm.can_add == True
    assert itm.can_edit == True
    assert itm.can_delete == True

class TestForm(CustomFormBase):
    def __init__(self,request, endpoint_name,caption):
        CustomFormBase.__init__(self, request=request, endpoint_name=endpoint_name, caption=caption)
        self.deal_type = FormCharField(id="deal_type", label="Deal Type", map_to_column="deal_type", validations=[])

    def on_get_list(self):
        dt = DealType.select()
        return dt


    def on_save(self, id):
        pass

    def on_edit(self, id):
        dt = DealType.get(DealType.uuid == str(id))
        return dt

    def on_delete(self, id):
        pass
    def on_insert(self):
        pass

    def custom_validation(self):
        pass

def create_test_data():
    class myData():
        deal_type = "deal type"
    return myData()

def create_form():
    mock_req = mock_request()
    return TestForm(request=mock_req, caption="my caption", endpoint_name="/testme")

class DataObj(object):
    def __init__(self):
        self.deal_type == ""

def test_clear_errors():
    # GIVEN
    deal_type = "type1"

    frm = create_form()
    frm.deal_type.errors.append("error1")

    #WHEN
    frm.deal_type.clear_errors()

    #THEN
    assert len(frm.deal_type.errors) == 0

def test_get_fields():
    #GIVEN
    frm = create_form()

    #WHEN
    fields = frm.get_fields()

    #THEN
    assert len(fields) == 1

def test_set_form_data():
    #GIVEN
    frm = create_form()
    #WHEN
    data= create_test_data()
    frm.set_form_data(data)
    #THEN

    assert frm.deal_type.value == data.deal_type

def test_validate():
    #GIVEN
    frm = create_form()

    #WHEN
    frm.deal_type.value == ""
    valid = frm.validate()

    #THEN
    assert valid == False
    assert len(frm.deal_type.errors) == 1

def test_get_field_values_from_request():
    #GIVEN
    frm = create_form()
    data = create_test_data()

    #WHEN
    frm.get_field_values_from_request()

    #THEN
    assert frm.deal_type.value ==data.deal_type