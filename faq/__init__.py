from flask import Blueprint, render_template, redirect, request
from models.FAQ import FAQ
from models.User import User
from models.DealQuestion import DealQuestion
from utils import requires_auth

def add_routes(app=None):
    faq_page = Blueprint('faq_page', __name__,
                            template_folder='templates')


    @faq_page.route("/faq", methods=['GET'])
    def faq():
        faqs = FAQ.select()
        return render_template("faq.html", data=faqs)



    @faq_page.route("/add_question", methods=['POST'])
    @requires_auth
    def add_question():
        q = DealQuestion.create(question=request.form['question'],
                                deal=request.form['deal_id'],
                                asked_by_id=User.select().first(1))

        return redirect("/view_deal/"+id)

    app.register_blueprint(faq_page)