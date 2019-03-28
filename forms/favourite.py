
from components.formbuilder.validations import *
from components.formbuilder.uicomponents import *
from components.formbuilder.formbase import *
from components.formbuilder.formoutput import *

from models.Favourites import Favourites

class FavouritesForm(CustomFormBase):
    def __init__(self,request, endpoint_name,caption):
        CustomFormBase.__init__(self, request=request, endpoint_name=endpoint_name, caption=caption)
        self.deal = FormCharField(id="Deal", label="Deal", map_to_column="deal", on_render=self.render_deal, order=1)
        self.city = FormCharField(id="City", label="City", map_to_column="deal", on_render=self.render_city, order=2)
        self.can_add=False
        self.can_edit=False

    def render_city(self, data):
        return "%s" % (data.city)

    def render_deal(self, data):
        return "<a href='/view_deal/%s'>%s</a>" % (data.uuid, data.title)

    def on_get_list(self):
        dt = Favourites.select()
        return dt

    def on_delete(self, id):
        query = Favourites.delete().where(Favourites.uuid == str(id))
        query.execute()

