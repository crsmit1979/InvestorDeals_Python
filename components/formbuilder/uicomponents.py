from werkzeug.utils import secure_filename
import pathlib
import uuid
import os

class FormObject(object):
    def __init__(self, id, label, validations=None, map_to_column=None, show_in_list=True, order=0, format_output=None, on_render=None, align="left", tooltip=None, name=None):
        self.id = id
        self.name = name
        if id is not None and name is None:
            self.name = id
        self.align = align
        self.tooltip = tooltip
        self.on_render = on_render
        self.label = label
        self.value = None
        self.format_output=format_output
        self.order = order
        self.validations = validations
        self.map_to_column = map_to_column
        self.show_in_list=show_in_list
        self.errors = []

    def clear_errors(self):
        self.errors = []


    def is_valid(self):
        result = True
        self.errors = []
        if self.validations is not None:
            for validation in self.validations:
                ob = validation(self.value)
                if ob.is_valid() == False:
                    self.errors.append(ob.message)
                    result = False
        return result

class NonFieldObject(object):
    def __init__(self):
        pass

class CustomRenderField(FormObject, NonFieldObject):
    def __init__(self, label, on_render, order, show_in_list=True, map_to_column=None, align="left", tooltip=None):
        FormObject.__init__(self, id=None, label=label, validations=None, map_to_column=map_to_column, show_in_list=show_in_list,
                            order=order, format_output=None, align=align, tooltip=tooltip)
        self.on_render = on_render

    def on_render(self, val):
        return "_Not Implemented_"


class FormHeader(FormObject, NonFieldObject):
    def __init__(self, order, label, on_render=None, align="left", tooltip=None):
        FormObject.__init__(self, id=None, label=label, validations=None, map_to_column=None, show_in_list=False,
                            order=order, format_output=None, align=align, tooltip=tooltip)
    def render(self):
        return "<h3 class='form-header'>%s</h3>" % (self.label)


class FormSeperator(FormObject, NonFieldObject):
    def __init__(self, order, align="left"):
        FormObject.__init__(self, id=None, label=None, validations=None, map_to_column=None, show_in_list=False, order=order, format_output=None, align=align, tooltip=None)

    def render(self):
        return "<hr class='form-seperator'/>"

class FormUploadField(FormObject):
    def __init__(self, id, label, save_to_directory, request, value=None, name=None, validations=None,map_to_column=None, show_in_list=True, order=None, format_output=None, allow_multiple=False, align="left", tooltip=None):
        FormObject.__init__(self, id=id, label=label, validations=validations, map_to_column=map_to_column, show_in_list=show_in_list, order=order, format_output=format_output, align=align, tooltip=tooltip, name=name)
        self.value = value
        self.request = request
        self.allow_multiple = allow_multiple
        self.save_to_directory = save_to_directory

    def save_file(self):
        new_filenames_array = []
        files = self.request.files.getlist(self.name)
        if len(files) > 0:
            for file in files:
                new_filename = None
                if (file):
                    filename = secure_filename(file.filename)
                    extension = pathlib.Path(filename).suffix
                    newfilename = str(uuid.uuid4()) + extension
                    file.save(os.path.join(self.save_to_directory, newfilename))
                    new_filenames_array.append(newfilename)
        return new_filenames_array

    def render(self):
        value = self.value
        multiple = ""
        if value is None:
            value = ""
        if (self.allow_multiple):
            multiple = "multiple"
        return "<input type='file' name='%s' id='%s class='input_file' %s/>" % (self.name, self.id, multiple)


class FormCharField(FormObject):
    def __init__(self, id, label, value=None, name=None, validations=None, map_to_column=None, max_length=255, show_in_list=True, order=None, format_output=None, on_render=None, align="left", tooltip=None):
        FormObject.__init__(self, id=id, label=label, validations=validations, map_to_column=map_to_column, show_in_list=show_in_list, order=order, format_output=format_output, on_render=on_render, align=align, tooltip=tooltip, name=name)
        self.value = value
        self.max_length = max_length

    def render(self):
        value = self.value
        if value is None:
            value = ""
        return "<input type='text' name='%s' id='%s' value='%s' class='input_text' maxlength='%s'/>" % (self.name, self.id, value, self.max_length)

class FormHiddenField(FormObject):
    def __init__(self, id, label, value=None, name=None, map_to_column=None, show_in_list=True, order=None, format_output=None, align="left", tooltip=None):
        FormObject.__init__(self, id=id, label=None, map_to_column=map_to_column,  show_in_list=show_in_list, order=order, format_output=format_output, align=align ,tooltip=tooltip, name=name)
        self.value = value

    def render(self):
        value = self.value
        if value is None:
            value = ""
        return "<input type='hidden' name='%s' id='%s' value='%s'/>" % (self.name, self.id, value)


class FormPasswordField(FormObject):
    def __init__(self, id, label, value=None, name=None, map_to_column=None, show_in_list=True, order=None, format_output=None, align="left", tooltip=None):
        FormObject.__init__(self, id=id, label=None, map_to_column=map_to_column,  show_in_list=show_in_list, order=order, format_output=format_output, align=align, tooltip=tooltip, name=name)
        self.value = value

    def render(self):
        value = self.value
        if value is None:
            value = ""
        return "<input type='password' name='%s' id='%s' value='%s'/>" % (self.name, self.id, value)


class FormNumericField(FormObject):
    def __init__(self, id, label, value=None, name=None, validations=None, map_to_column=None, show_in_list=True, order=None, format_output=None, align="right", tooltip=None):
        FormObject.__init__(self,id=id, label=label, validations=validations, map_to_column=map_to_column, show_in_list=show_in_list, order=order, format_output=format_output, align=align, tooltip=tooltip, name=name)
        self.value = value

    def render(self):
        value = self.value
        if value is None:
            value = ""
        return "<input type='text' name='%s' id='%s' value='%s' class='input_numeric'/>" % (self.name, self.id, value)


class FormDropdownField(FormObject):
    def __init__(self, id, label, name=None, ids=None, selected_value=None, values=None, validations=None, data=None, id_field=None, value_field=None, map_to_column=None, show_in_list=True, order=None, format_output=None, align="left", tooltip=None):
        FormObject.__init__(self,id=id, label=label, validations=validations, map_to_column=map_to_column,  show_in_list=show_in_list, order=order, format_output=format_output, align=align, tooltip=tooltip, name=name)
        self.values = values
        self.value = selected_value
        self.ids = ids
        self.data = data
        self.id_field = id_field
        self.value_field=value_field


    def render(self):
        value = self.value
        if value is None:
            value = ""
        txt = []
        txt.append("<select id='%s' name='%s'>" % (self.id, self.name))
        txt.append("<option value=''>Select</option>")
        if self.ids is not None and len(self.ids)>0:
            for x in range(len(self.ids)):
                selected = ""
                if (value == self.ids[x]):
                    selected = "selected"
                txt.append("<option value='%s' %s>%s</option>" % (self.ids[x], selected, self.values[x]))

        if self.data is not None and len(self.data) > 0:
            for row in self.data:
                selected = ""
                display_id = getattr(row,self.id_field)
                display_value = getattr(row, self.value_field)
                if display_id == self.value:
                    selected = "selected"
                txt.append("<option value='%s' %s>%s</option>" % (display_id, selected, display_value))

        txt.append("</select>")
        return " ".join(txt)


class FormDateField(FormObject):
    def __init__(self, id, label, value=None, name=None, validations=None, map_to_column=None, show_in_list=True, order=None, format_output=None, align="center", tooltip=None):
        super(self.__class__, self).__init__(id=id, label=label, validations=validations, map_to_column=map_to_column,  show_in_list=show_in_list, order=order, format_output=format_output, align=align, tooltip=tooltip, name=name)
        self.value = value

    def render(self):
        value = self.value
        if value is None:
            value = ""
        return "<input type='textbox' name='%s' id='%s' value='%s' placeholder='dd/mm/yyyy' class='input_date'/>" % (self.name, self.id, value)


class FormCheckboxField(FormObject):
    def __init__(self, id, label, value=None, name=None, validations=None, map_to_column=None, show_in_list=True, order=None, format_output=None, align="center", tooltip=None):
        super(self.__class__, self).__init__(id=id, label=label, validations=validations, map_to_column=map_to_column,  show_in_list=show_in_list, order=order, format_output=format_output, align=align, tooltip=tooltip, name=name)
        self.value = value

    def get_value(self):
        if self.value == '1':
            return True
        else:
            return False

    def render(self):
        value = self.value
        if self.value is None:
            value = ""

        checked = ""
        if value in ["1", 1]:
            checked = "checked"
        return "<input type='checkbox' name='%s' id='%s' value='1' class='input_checkbox' %s/>" % (self.name, self.id, checked)
