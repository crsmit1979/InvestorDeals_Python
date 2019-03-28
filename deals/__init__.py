from flask import Blueprint, render_template,  request, send_from_directory, redirect
from flask_login import login_required
from models.Deal import Deal
from models.DealPhoto import DealPhoto
from models.DealType import DealType
from models.Bedrooms import Bedrooms
from models.DealQuestionAnswer import DealQuestionAnswer
from models.DealQuestion import DealQuestion
from models.User import User
from config import config
from utils import requires_auth

def add_routes(app=None):
    deal_page = Blueprint('deal_page', __name__,
                            template_folder='templates')


    @deal_page.route("/view_deal/<id>", methods=['GET'])
    def view_deal(id):
        data = Deal.get_by_uuid(id)
        photos = DealPhoto.get_photos_by_deal_id(id)
        return render_template("view_deal.html",
                               data=data,
                               photos=photos)


    @deal_page.route("/edit_deal/<id>", methods=['GET'])
    @requires_auth
    def edit_deal(id):
        return render_template("edit_deal.html",
                               data=Deal.get_by_uuid(id),
                               deal_types=DealType.get_all())

    @deal_page.route("/add_reply", methods=['POST'])
    @requires_auth
    def add_reply():
        deal_question_id = request.form['deal_question_id']
        rec = DealQuestion.get_by_uuid(deal_question_id)
        usr = User.select().first(1)
        res = DealQuestionAnswer.create(answer=request.form['answer'],
                                        deal_question=rec,
                                        answered_by=usr.uuid)
        return redirect("/view_deal/"+str(rec.deal.uuid))

    @deal_page.route("/find_deal", methods=['GET'])
    def find_deal():
        deal_type_id = request.args.get("deal_type_id")
        filter_city = request.args.get("city")
        filter_county = request.args.get("county")
        filter_bedrooms = request.args.get("bedrooms")

        pagenr =0 if request.args.get("page") is None else  int(request.args.get("page"))
        pagesize = 100 if request.args.get("pagesize") is None else int(request.args.get("pagesize"))
        rows = Deal.filter(deal_type_id=deal_type_id, filter_city=filter_city, filter_county=filter_county)
        data = rows.paginate(pagenr, pagesize)
        deal_types = DealType.select()
        return render_template("find_deal.html",
                               data=data,
                               deal_types=deal_types,
                               cities=Deal.available_cities(),
                               counties=Deal.available_counties(),
                               records=rows.count(),
                               pagesize=pagesize,
                               bedrooms=Bedrooms.select())


    @deal_page.route("/update_deal", methods=['POST'])
    @requires_auth
    def update_deal():
        deal = Deal.get_by_id(request.form["id"])
        deal.title = request.form['title']
        deal.description = request.form["description"]
        deal.sourcing_fee = float(request.form["sourcing_fee"])
        deal.roi = float(request.form["roi"])
        deal.county = request.form['county']
        deal.city = request.form['city']
        deal.address_line_1 = request.form['address_line_1']
        deal.address_line_2 = request.form['address_line_2']
        deal.postcode = request.form['postcode']
        deal.show_address_details = bool(request.form['show_address_details'])
        if request.form["deal_type"] is not None and request.form["deal_type"] != "":
            deal.deal_type = DealType.get_by_id(request.form["deal_type"])
        deal.save()
        return redirect("/find_deal")

    @deal_page.route("/delete_deal/<id>", methods=['GET'])
    @requires_auth
    def delete_deal(id):
        Deal.delete_by_id(id)
        return redirect("/find_deal")


    @deal_page.route("/document/<file>", methods=['GET'])
    def get_document(file):
        return send_from_directory(directory=config.get_config('UPLOAD_FOLDER_DOCUMENT'),
                                   filename=file)

    @deal_page.route("/deal_photo/<file>", methods=['GET'])
    def get_deal_photo(file):
        return send_from_directory(directory=config.get_config('UPLOAD_FOLDER_DEAL_PHOTOS'),
                                   filename=file)


    @deal_page.route("/deals_by_owner/<id>", methods=['GET'])
    @requires_auth
    def deals_by_owner(id):
        return render_template("deals_by_owner.html",
                               data=Deal.get_deals_created_by_user(id)
                               )

    app.register_blueprint(deal_page)