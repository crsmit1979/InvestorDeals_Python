from flask import Blueprint, jsonify
from models.Deal import Deal
from models.DealPhoto import DealPhoto
from flask_login import login_required

profile_page = Blueprint('profile_page', __name__,
                        template_folder='templates')


