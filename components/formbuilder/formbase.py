from components.formbuilder.uicomponents import FormObject, FormSeperator, NonFieldObject, FormHeader
from flask import render_template, redirect

class CustomFormBase(object):
    def __init__(self, request, endpoint_name, caption, method=None, action=None, sub_text=None):
        self.errors = []
        self.method = method
        self.sub_text= sub_text
        self.endpoint_name = endpoint_name
        self.action = action
        self.submit_button_caption = "Add"
        self.request = request
        self.caption = caption
        self.can_add = True
        self.can_delete = True
        self.can_edit = True

    def on_render_edit_link(self,url, rowid):
        return "<a href='%s' title='Edit Record'><i class='icon edit'></i></a>" % (url)

    def clear_errors(self):
        fields = self.get_fields()
        for field in fields:
            field.clear_errors()

    def set_form_data(self, data):
        fields = self.get_fields()
        for field in fields:
            if field.map_to_column is not None:
                field.value = getattr(data, field.map_to_column)

    def validate(self):
        self.errors = []
        self.get_field_values_from_request()
        fields = self.get_fields()
        for field in fields:
            field.is_valid()
            if len(field.errors) > 0:
                for err in field.errors:
                    self.errors.append(err)
        self.custom_validation()
        if len(self.errors) > 0:
            return False
        else:
            return True

    def custom_validation(self):
        self.get_field_values_from_request()

    def is_submitted(self):
        if self.request.method in ['POST']:
            return True
        return False

    def __on_new(self):
        self.clear_errors()
        self.submit_button_caption = "Insert"
        self.method = 'POST'
        self.action = "/"+self.endpoint_name+"/new"
        self.clear_field_values()
        self.on_new()
        return render_template("testform.html", type="form", form=self)
    """
    def __on_add(self):
        self.method = "POST"
        self.action = "/"+self.endpoint_name

        return self.on_add()
    """

    def __on_delete(self, id):
        self.method = "GET"
        self.action = "/"+self.endpoint_name + "/"+str(id)+"/delete"
        self.on_delete(id)
        return redirect("/"+self.endpoint_name)

    def __on_get_list(self):
        data = self.on_get_list()
        return render_template("testform.html", type='list', form=self, rows=data)

    def __on_save(self, id):
        self.method = "POST"
        self.action = "/"+self.endpoint_name + "/"+str(id)
        self.get_field_values_from_request()
        if self.is_submitted() and not self.validate():
            return render_template("testform.html", type='form', form=self)
        self.on_save(id)
        return redirect("/"+self.endpoint_name)

    def __on_edit(self, id):
        self.method = "POST"
        self.action = "/"+self.endpoint_name + "/"+str(id)
        self.submit_button_caption = "Update"
        data = self.on_edit(id)
        self.set_form_data(data)
        return render_template("testform.html", type='form', form=self)

    def __on_insert(self):
        if self.is_submitted() and self.validate():
            self.on_insert()
        else:
            return render_template("testform.html", type="form", form=self)
        return redirect("/"+self.endpoint_name)

    def on_new(self):
        return render_template("testform.html", type='form', form=self)

    def on_insert(self):
        pass

    def on_edit(self, id):
        pass
    def on_delete(self,id):
        pass
    def on_save(self, id):
        pass

    def set_app(self, app):
        self.app = app
        #ADD
        self.app.add_url_rule('/'+self.endpoint_name+"/new", "new_form_"+self.endpoint_name, self.__on_new, methods=['GET'])
        #GET
        self.app.add_url_rule('/'+self.endpoint_name+"/<id>", "edit_form_"+self.endpoint_name, self.__on_edit, methods=['GET'])
        #POST
        #DELETE
        #LIST
        self.app.add_url_rule('/'+self.endpoint_name, "get_list_form_"+self.endpoint_name, self.__on_get_list, methods=['GET'])

        self.app.add_url_rule('/'+self.endpoint_name+"/new", "post_form_"+self.endpoint_name, self.__on_insert, methods=['POST'])
        self.app.add_url_rule('/'+self.endpoint_name+"/<id>/delete", "delete_form_"+self.endpoint_name, self.__on_delete, methods=['POST','GET'])
        self.app.add_url_rule('/'+self.endpoint_name+"/<id>", "update_form_"+self.endpoint_name, self.__on_save, methods=['POST'])

    def __get_from_value_from_request(self, fieldname):
        return str(self.request.form.get(fieldname))

    def get_field_values_from_request(self):
        fields = self.get_fields()
        for f in fields:
            try:
                f.value = self.__get_from_value_from_request(f.name)
            except:
                pass

    def clear_field_values(self):
        fields = self.get_fields()
        for f in fields:
            f.value = ""

    def on_form_post(self):
        self.on_post(self)


    def on_form_update(self):
        self.on_update(self);

    def on_form_delete(self):
        self.on_delete(self);


    def get_fields(self):
        fields =[]
        for a in dir(self):
            prop = getattr(self, a)
            if isinstance(prop, FormObject):
                fields.append(prop)
        fields.sort(key=lambda x: x.order, reverse=False)
        return fields

    def render_list(self, rows):
        txt = []
        fields = self.get_fields()
        txt.append("<div class='form-header-bar'>")
        txt.append("<h2>%s</h2>" % (self.caption))
        txt.append("</div>")
        txt.append("<table class='datatable'>")
        txt.append("<thead>")
        txt.append("<tr>")
        txt.append("<th></th>")
        total_fields=0
        for field in fields:
            if field.show_in_list == True:
                txt.append("<th class='%s'>%s</th>" % (field.align, field.label))
                total_fields = total_fields + 1
        txt.append("</tr>")
        txt.append("</thead>")

        txt.append("<tbody>")
        if len(rows) == 0:
            txt.append("<tr>")
            txt.append("<td colspan='%s' class='no-data'>No data available</td>" % (total_fields+1))
            txt.append("</tr>")

        for row in rows:
            txt.append("<tr>")
            txt.append("<td class='center'>")
            if (self.can_delete):
                txt.append("<a href='/%s/%s/delete' title='Delete Record'><i class='icon trash alternate outline'></i></a>" % (self.endpoint_name, str(getattr(row,'uuid'))))
            if (self.can_edit):
                rowid =str(getattr(row,'uuid'))
                edit_link = "/%s/%s" % (self.endpoint_name,rowid)
                txt.append(self.on_render_edit_link(edit_link, rowid))
            txt.append("</td>")
            for field in fields:
                if field.show_in_list == True:
                    val = ""
                    if field.map_to_column:
                        val = getattr(row,field.map_to_column)
                    if field.format_output is not None:
                       val = field.format_output(val).output()
                    if field.on_render is not None:
                        val = field.on_render(val)
                    txt.append("<td class='%s'>%s &nbsp</td>" %(field.align, val))
            txt.append("</tr>")
        txt.append("</tbody>")
        txt.append("<tfoot>")
        txt.append("<tr>")
        txt.append("<td colspan='%s'>" % (total_fields+1))

        if self.can_add:
            txt.append("<a href='/%s/new' class='form-button' title='Add new record'>Add New Record</i></a>"  % (self.endpoint_name))
        txt.append("<span class='float-right'>Total Records: %s</span>"  % (len(rows)))
        txt.append("</td>")
        txt.append("</tr>")
        txt.append("</tfoot>")
        txt.append("</table>")
        return " ".join(txt)

    def render(self):
        txt = []
        txt.append("<form method='%s' class='panel panel-default' action='%s' enctype='multipart/form-data'>" % (self.method, self.action))
        txt.append("<div class='form-header-bar'>")
        txt.append("<h2>%s</h2>" % (self.caption))
        if self.sub_text is not None:
            txt.append("<h3>%s</h3>" % (self.sub_text))
        txt.append("</div>")
        txt.append("<div class='form-body-bar'>")
        fields = self.get_fields()
        for a in fields:
                txt.append("<p>")
                if not isinstance(a, FormHeader) and not isinstance(a, FormSeperator) and not isinstance(a, NonFieldObject):
                    tooltip = ""
                    if (a.tooltip != None):
                        tooltip = "<i class='icon question circle outline' tooltip='%s'></i>" % (a.tooltip)
                    if a.label is not None and a.label != "":
                        txt.append("<label class='input_label'>%s %s</label>" % (a.label, tooltip))
                    txt.append("<span style='display:inline-block'>")
                txt.append(a.render())
                if len(a.errors)>0:
                    for error in a.errors:
                        txt.append("<span class='error-item''>%s</span>" % (error))
                txt.append("</p>")
        txt.append("</div>")
        txt.append("<div class='form-footer-bar'>")
        txt.append("   <input type='submit' value='%s' name='submit_button' class='form-button'/>" % (self.submit_button_caption))
        txt.append("   <a href='%s' value='Cancel' name='cancel_button' class='form-button'>Cancel</a>" % ("/"+self.endpoint_name+""))
        txt.append("</div>")
        txt.append("</form>")

        return " ".join(txt)

