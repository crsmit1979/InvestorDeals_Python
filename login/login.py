from flask import Blueprint, jsonify, session, url_for
from models.Deal import Deal
from models.DealPhoto import DealPhoto
from flask_login import login_required
from models.User import User
from config import config

login_page = Blueprint('login_page', __name__,
                        template_folder='templates')


