from flask import Blueprint, jsonify
from models.Deal import Deal
from models.DealPhoto import DealPhoto
from flask_login import login_required
from utils import requires_auth

def add_routes(app=None):
    api_page = Blueprint('api_page', __name__,
                            template_folder='templates')

    @api_page.route('/api/deals')
    #@requires_auth
    def deals():
        result = []
        d_deals = Deal.filter()
        for d in d_deals:
            photos = []
            d_photos = d.photos
            for p in d_photos:
                o_photo = {
                        "url": p.filename
                }
                photos.append(o_photo)
            o_deal = {
                "title":d.title,
                "description": d.description,
                "created_by": {
                    "id":str(d.created_by),
                    "name": d.created_by.name + " " + d.created_by.surname
                },
                "created": d.created,
                "sourcing_fee": d.sourcing_fee,
                "roi": d.roi,
                "deal_type_id": d.deal_type_id,
                "document": "",
                "county": d.county,
                "city": d.city,
                "address_line_1": d.address_line_1,
                "address_line_2": d.address_line_2,
                "postcode": d.postcode,
                "show_address": d.show_address,
                "bedrooms": d.bedrooms,
                "photos": photos
            }
            result.append(o_deal)

        return jsonify(result)

    app.register_blueprint(api_page)