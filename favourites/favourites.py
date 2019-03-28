from flask import Blueprint, render_template, abort, jsonify, request
from jinja2 import TemplateNotFound

favourites_page = Blueprint('favourites_page', __name__,
                        template_folder='templates')


@favourites_page.route("/view_deal/<id>", methods=['GET'])
def view_favourites():
    return "ok"
