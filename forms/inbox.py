from components.formbuilder.validations import *
from components.formbuilder.uicomponents import *
from components.formbuilder.formbase import *
from components.formbuilder.formoutput import *

from models.Message import Message as ContactMessage

class InboxForm(CustomFormBase):
    def __init__(self,request, endpoint_name,caption):
        CustomFormBase.__init__(self, request=request, endpoint_name=endpoint_name, caption=caption)
        self.sender = FormCharField(id='sender', name='Sender', label='Sender', map_to_column="message_from", on_render=self.on_render_user, order=1)
        self.receiver = FormCharField(id='receiver', name='Receiver', label='Receiver', map_to_column="message_to", on_render=self.on_render_user, order=2)
        self.date_send = FormCharField(id='date_send', name='date_send', label='Date Send', map_to_column="created", order=3)
        self.message = FormCharField(id='message', name='message', label='Message', map_to_column="message", on_render=self.on_render_message, order=4)
        self.viewreply = CustomRenderField(label="View/Reply", on_render=self.on_render_view_reply, map_to_column="uuid", order=5)

        self.can_edit = False
        self.can_add = False

    def on_render_view_reply(self, val):
        url = "/reply_email/%s" % (val)
        return "<a href='%s'>View/Reply</a>" % (url)

    def on_render_message(self, data):
        return "<a href='%s'>%s</a>"  % ("/edit", data)

    def on_render_user(self, data):
        return "%s %s" % (data.name, data.surname)

    def on_get_list(self):
        data = ContactMessage.select()
        """\
            .where(
            (ContactMessage.message_from == current_user.uuid) | (ContactMessage.message_to == current_user.uuid) & (
            ContactMessage.deleted == False))"""
        return data
