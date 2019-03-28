from flask import Blueprint, jsonify, request, render_template
from utils import get_json_value
from models.SignupUser import SignupUser

def add_routes(app=None):
    signup = Blueprint('signup',
                       __name__,
                       static_url_path="/signup/static",
                       static_folder="./static",
                       template_folder="./templates"
                       )


    @signup.route("/pre_signup/save", methods=['POST'])
    def pre_signup_save():
        json = request.get_json(silent=True)
        rec = SignupUser.create(
            name=get_json_value(json,'name'),
            surname=get_json_value(json,'surname'),
            email=get_json_value(json,'email'),
            typeofdeal=get_json_value(json,'typeofdeal'),
            otherdealtype=get_json_value(json,'otherdealtype'),
            investor=get_json_value(json,'investor'),
            sourcer=get_json_value(json,'sourcer'),
            location=get_json_value(json,'location'))
        return jsonify({'success': True})
        #return render_template("pre_signup_success.html")


    @signup.route("/pre_signup", methods=['GET'])
    def pre_signup():
        return render_template("signup/pre_signup.html")


    @signup.route("/pre_signup1", methods=['GET'])
    def test12():
        return render_template("signup.html")

    app.register_blueprint(signup)