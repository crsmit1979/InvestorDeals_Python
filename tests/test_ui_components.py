import pytest
from components.formbuilder.uicomponents import *
from components.formbuilder.validations import  *

def create_form_object():
    #GIVEN
    id = 'id'
    label='lbl'
    validations = []
    map_to_column='test'
    show_in_list=False
    order=10,
    format_output = None
    on_render = None
    align="right"
    tooltip = "my tip"
    #WHEN
    return FormObject(id=id, label=label, validations=validations, map_to_column=map_to_column, show_in_list=show_in_list, order=order, format_output=format_output, on_render=on_render, align=align, tooltip=tooltip)


def test_formobject_constructors():
    #GIVEN
    id = 'id'
    label='lbl'
    validations = []
    map_to_column='test'
    show_in_list=False
    order=10,
    format_output = None
    on_render = None
    align="right"
    tooltip = "my tip"
    #WHEN
    obj = FormObject(id=id, label=label, validations=validations, map_to_column=map_to_column, show_in_list=show_in_list, order=order, format_output=format_output, on_render=on_render, align=align, tooltip=tooltip)

    #THEN
    assert obj.id == id
    assert obj.label == label
    assert obj.validations == validations
    assert obj.map_to_column == map_to_column
    assert obj.show_in_list == show_in_list
    assert obj.order == order
    assert obj.format_output == format_output
    assert obj.on_render == on_render
    assert obj.align == align
    assert obj.tooltip == tooltip


def test_formObject_clear_errors():
    #given
    obj = create_form_object()
    obj.errors = ["error 1", "error 2"]

    #when
    obj.clear_errors()

    #then
    assert len(obj.errors) == 0


def test_formobject_is_valid_returns_false_when_validation_fails():
    #given
    obj = create_form_object()
    obj.validations.append(NotEmpty_Validation)

    #when
    isvalid = obj.is_valid()

    #then
    assert isvalid== False
    assert len(obj.errors) == 1

def test_formobject_is_valid_returns_true_when_no_validation():
    #given
    obj = create_form_object()

    #when
    isvalid = obj.is_valid()

    #then
    assert isvalid== True
    assert len(obj.errors) == 0


def test_formHeader_render():
    #given
    order = 2
    label = 'my label'
    obj = FormHeader(label=label, order=order)

    #when
    txt = obj.render()

    #then
    assert txt == "<h3 class='form-header'>%s</h3>" % (label)

def test_formseperator_render():
    #given
    order = 2
    obj = FormSeperator( order=order)

    #when
    txt = obj.render()

    #then
    assert txt == "<hr class='form-seperator'/>"

def test_formuploadfield_single_file_render():
    #given
    label=3
    save_to_directory = "c:/"
    request= ""
    obj = FormUploadField(id=id, label=label, save_to_directory=save_to_directory, request=request, allow_multiple=False)

    #when
    txt= obj.render()

    #then
    assert obj.save_to_directory == save_to_directory
    assert obj.request == request
    assert txt == "<input type='file' name='%s' id='%s class='input_file' />" % (id, id)

def test_formuploadfield_multiple_file_render():
    #given
    label=3
    save_to_directory = "c:/"
    request= ""
    obj = FormUploadField(id=id, label=label, save_to_directory=save_to_directory, request=request, allow_multiple=True)

    #when
    txt= obj.render()

    #then
    assert obj.save_to_directory == save_to_directory
    assert obj.request == request
    assert txt == "<input type='file' name='%s' id='%s class='input_file' multiple/>" % (id, id)


def test_formcharfield():
    #given
    id="id"
    name='name'
    maxlength=20
    value=10
    label="label"
    obj = FormCharField(id=id, name=name, label=label, max_length=maxlength, value=value)

    #when
    txt = obj.render()
    #then
    assert txt == "<input type='text' name='%s' id='%s' value='%s' class='input_text' maxlength='%s'/>" % (name, id, value, maxlength)

def test_hidden_field_render():
    #given
    id="id"
    name='name'
    value=10
    label="label"
    obj = FormHiddenField(id=id, name=name, value=value, label=label)

    #when
    txt =obj.render()
    #then
    assert txt == "<input type='hidden' name='%s' id='%s' value='%s'/>" % (name, id, value)

def test_password_field_render():
    #given
    id="id"
    name='name'
    value=10
    label="label"
    obj = FormPasswordField(id=id, name=name, value=value, label=label)

    #when
    txt =obj.render()
    #then
    assert txt == "<input type='password' name='%s' id='%s' value='%s'/>" % (name, id, value)


def test_numeric_field_render():
    #given
    id="id"
    name='name'
    value=10
    label="label"
    obj = FormNumericField(id=id, name=name, value=value, label=label)

    #when
    txt =obj.render()
    #then
    assert txt == "<input type='text' name='%s' id='%s' value='%s' class='input_numeric'/>" % (name, id, value)

def test_dropdown_field_fixed_list_render():
    #given
    id="id"
    name='name'
    value=1
    label="label"
    obj = FormDropdownField(id=id, name=name, selected_value=value, label=label, ids=[1,2], values=["A","B"])

    #when
    txt =obj.render()
    #then
    expected =  "<select id='%s' name='%s'> <option value=''>Select</option> <option value='1' selected>A</option> <option value='2' >B</option> </select>" % (id, name)
    assert expected == txt


def test_dropdown_field_data_list_render():
    class items():
        def __init__(self, id, name):
            self.id = id
            self.name = name

    arr = [items(1,"A"), items(2,"B")]

    #given
    id="id"
    name='name'
    value=1
    label="label"
    obj = FormDropdownField(id=id, name=name, selected_value=value, label=label, data=arr, id_field="id", value_field="name")

    #when
    txt =obj.render()
    #then
    expected =  "<select id='%s' name='%s'> <option value=''>Select</option> <option value='1' selected>A</option> <option value='2' >B</option> </select>" % (id, name)
    assert expected == txt


def test_date_field_render():
    #given
    id="id"
    name='name'
    value=1
    label="label"
    obj = FormDateField(id=id, name=name, value=value, label=label)

    #when
    txt =obj.render()
    #then
    expected = "<input type='textbox' name='%s' id='%s' value='%s' placeholder='dd/mm/yyyy' class='input_date'/>" % (name, id, value)
    assert expected == txt


def test_date_field_render():
    #given
    id="id"
    name='name'
    value=1
    checked= True
    label="label"
    obj = FormCheckboxField(id=id, name=name, value=value, label=label)

    #when
    txt =obj.render()

    #then
    expected = "<input type='checkbox' name='%s' id='%s' value='1' class='input_checkbox' checked/>" % (name, id)
    assert expected == txt
