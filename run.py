import json
import context_processors
from utils import requires_auth
import log
import error_handlers
from config import config
import requests
from models.Message import Message as ContactMessage
from models.SignupUser import SignupUser
from authlib.flask.client import OAuth
from logging import FileHandler
from flask import Flask, request, url_for, session, g
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from flask_mail import Mail, Message
from peewee import DoesNotExist
from six.moves.urllib.parse import urlencode
from forms.deal import AddDealForm
from forms.faq import FAQForm
from forms.profile import ProfileForm
from forms.dealtype import DealTypeForm
from forms.favourite import FavouritesForm
from forms.inbox import InboxForm
import signup
import faq
import messages
import upload
import deals
import api

from models.Suggestions import Suggestions
from models.User import User
import run_migration
from flask_caching import Cache
from components.formbuilder.validations import *
from components.formbuilder.uicomponents import *
from components.formbuilder.formbase import *
from waitress import serve


import logging
from logging.config import dictConfig


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})
file_handler = FileHandler("log.txt")
logger = logging.getLogger()
logger.addHandler(file_handler)


app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
cache.init_app(app)
oauth = OAuth(app)

#CREATE CONTEXT PROCESSORS
context_processors.apply(app)

#REGISTER ALL BLUEPRINTS
messages.add_routes(app)
deals.add_routes(app)
signup.add_routes(app)
upload.add_routes(app)
api.add_routes(app)
faq.add_routes(app)

#ADD ERROR HANLDING CAPABILITY
error_handlers.apply_error_handlers(app)

auth0 = oauth.register(
    'auth0',
    client_id=config.get_config("auth_client_id"),
    client_secret=config.get_config("auth_client_secret"),
    api_base_url=config.get_config("auth_api_base_url"),
    access_token_url=config.get_config("auth_access_token_url"),
    authorize_url=config.get_config("auth_authorize_url"),
    client_kwargs={
        'scope': 'openid profile',
    },
)
app.config.update(
    MAIL_SERVER=config.get_config("MAIL_SERVER"), #''smtp.gmail.com',
    MAIL_PORT=int(config.get_config("MAIL_PORT")), #465,
    MAIL_USE_SSL=bool(config.get_config("MAIL_USE_SSL")),
    MAIL_USERNAME = config.get_config("MAIL_USERNAME"), #''safunguy79@gmail.com',
    MAIL_PASSWORD = config.get_config("MAIL_PASSWORD"),
    TEMPLATES_AUTO_RELOAD = True,
    SECRET_KEY=config.get_config("SECRET_KEY")
)

mail = Mail(app)
mail.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"







def get_auth0_token():
    url = config.get_config("auth_access_token_url")
    payload = "{\"grant_type\":\"client_credentials\",\"client_id\": \"7P0uKEa32OVlfweiwEdPClAYDAhmanKm\",\"client_secret\": \"8SqyIA7Wx1uAOnTk7WbG0_N1z-rHAtD-2byCgu8hPp36ayhAPjDeWiX8TCa1ngk7\",\"audience\": \""+config.get_config("auth_api")+"\"}"
    headers = {'content-type': "application/json"}
    res = requests.post(url=url, data=payload, headers=headers)
    js  = res.json()
    return js

def get_auth0_users():
    token = get_auth0_token()
    auth = "%s %s" % (token['token_type'], token['access_token'])
    headers = {'authorization':  auth}
    dt = requests.get(url=config.get_config("auth_api") + "users?per_page=100&page=0", headers=headers)
    userlist = dt.json()
    oauth_users = []
    for user in userlist:
        userid = user['user_id']
        email = user['email']
        oauth_users.append({"userid":userid, "email":email})
        print(userid+" --- " + email)
    return oauth_users



@app.route('/login')
def login():
    redirect_uri = 'http://%s:%s/callback' % (config.get_config("server"), config.get_config("server_port"))
    return auth0.authorize_redirect(redirect_uri=redirect_uri, audience=config.get_config("auth_api_base_url")+'/userinfo')

@app.route('/logout')
def logout():
    # Clear session stored data
    session.clear()
    # Redirect user to logout endpoint
    params = {'returnTo': url_for('login', _external=True), 'client_id': config.get_config("auth_client_id")}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))


@app.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    # Store the user information in flask session.
    session['jwt_payload'] = userinfo
    given_name = ''
    family_name=''
    if 'given_name' in userinfo:
        given_name = userinfo['given_name']

    if 'family_name' in userinfo:
        family_name = userinfo['family_name']

    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': given_name,
        'surname': family_name,
        'picture': userinfo['picture']
    }
    try:
        create_profile_record(session['profile'])
        usr = User.get(User.oauth_id == str(userinfo['sub']))
        usr.is_administrator = True
        login_user(usr)
    except DoesNotExist:
        pass
    return redirect('/')

@app.route("/login_test_user", methods=['GET'])
def login_test_user():
    User.delete().where(User.name == "test").execute()

    session["profile"] = {
        'name':'test',
        'surname' : 'test',
        'user_id': 'abc',
        'picture': '',
        'jwt_payload': ''
    }
    session['jwt_payload'] = {}
    create_profile_record(session['profile'])

    usr = User.get(User.name == "test")
    usr.is_administrator = True

    login_user(usr)
    return "Test user logged in"



def create_profile_record(profile):
    try:
        usr = User.get_by_oauth(str(profile['user_id']))
    except DoesNotExist:
        oauth_users = get_auth0_users()
        oauth_user = filter(lambda x: x['userid'] == profile['user_id'], oauth_users)
        email = None
        if len(oauth_users) > 0:
            email = oauth_users[0]['email']
        inv1 = User.create(name=profile['name'],
                           surname=profile['surname'],
                           telephone='',
                           email=email,
                           password=None,
                           oauth_id=profile['user_id'],
                           oauth_profile_image=profile['picture'],
                           oauth_xml=session['jwt_payload'])
    return None

@app.route('/dashboard')
@requires_auth
def dashboard():
    return render_template('dashboard.html',
                           userinfo=session['profile'],
                           userinfo_pretty=json.dumps(session['jwt_payload'], indent=4))

@login_manager.user_loader
def load_user(userid):
    try:
        user = User.get_by_oauth(session['profile']['user_id'])
        if (user):
            return user
    except DoesNotExist:
        return None
    return None


@app.route("/suggestion", methods=['GET','POST'])
def suggestion():
    if request.method == 'POST':
        ip_address = request.environ['REMOTE_ADDR']
        Suggestions.create(
                           email=request.form['email'],
                           name=request.form['name'],
                           comment=request.form['suggestion'],
                           date_posted = datetime.datetime.now(),
                           ip_address=ip_address)
        return redirect("/")
    else:
        return render_template("suggestion.html")


@app.route("/logout_old")
@login_required
def logout_old():
    logout_user()
    return redirect("/login")

@app.route("/login_old", methods=['GET'])
def login_old():
    return render_template("login.html")

@app.route("/invalid_login", methods=['GET'])
def invalid_login():
    return render_template("invalid_login.html")

@app.route("/login", methods=['POST'])
def login_post():
    email = request.form["email"]
    password = request.form["password"]
    try:
        usr = User.get(User.email == email)
        if usr.activated == False:
            return render_template("not_activated.html")
        if usr.disabled == True:
            return render_template("account_disabled.html")
        if usr.email == email and password==usr.password:
            login_user(usr)
            return redirect("/")
        else:
            return redirect("/invalid_login")
    except DoesNotExist:
        return render_template("error.html")

@app.route("/reset_password", methods=['GET'])
def reset_password():
    return render_template("reset_password.html")

@app.route("/reset/<id>", methods=['GET'])
def reset(id):
    usr = User.get_by_uuid(id)
    return render_template("new_password.html", data=usr)

@app.route("/change_password", methods=['POST'])
def change_password():
    usr= User.change_password(request.form['id'], request.form['password'])
    login_user(usr)
    return redirect("/")

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body

    mail.send(msg)

@app.route("/request_reset", methods=['POST'])
def request_reset():
    usr = User.get_user_by_email(request.form['email'])
    sender=config.get_config("SENDRE_EMAIL_ADDRESS")
    send_email("Reset Password",
               sender,
               [usr.email],
               render_template("email_reset_password_template.txt",  userid=usr.uuid, server=config.get_config['server'], port=config.get_config['server_port']),
               render_template("email_reset_password_template.html", userid=usr.uuid, server=config.get_config['server'], port=config.get_config['server_port']))
    return render_template("reset_password_email_send.html")

@app.errorhandler(401)
def page_not_found(e):
    return redirect("/login")

@app.route("/activate/<id>", methods=['GET'])
def activate(id):
    try:
        usr = User.activate_user(id)
        login_user(usr)
        return render_template("activated.html")
    except DoesNotExist:
        return render_template("error.html")

@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")





@app.route("/admin", methods=['GET'])
@requires_auth
def admin():
    return render_template("admin.html")

@app.route("/view_investors", methods=['GET'])
@requires_auth
def view_investors():
    return render_template("view_investors.html",
                           data=User.get_all()
                           )







@app.before_request
def before_request():
    msg = []
    msg.append("----BEGIN REQUEST----")
    msg.append("Date: %s" % (datetime.datetime.now()))
    msg.append("IP Address: %s" % (request.remote_addr))
    msg.append("Method: %s" % (request.method))
    msg.append("URL: %s" % (request.url))
    if request.args is not None and len(request.args)>0:
        msg.append("Args: %s" % (request.args))
    if request.json is not None:
        msg.append("JSON: %s" % (request.json))
    if request.form is not None and len(request.form) > 0:
        msg.append("FORM: %s" % (request.form))
    msg.append("----END REQUEST----\n")
    log.log_debug("\n".join(msg))

    if config.get_config("environment") == "PROD":
        if "/static/" in request.url:
            pass
        else:
            if "/pre_signup" not in request.url:
                return redirect("/pre_signup")

    g.total_messages = 0
    if current_user.is_authenticated:
        usr = User.get(User.uuid == current_user.uuid)
        data = ContactMessage.get_user_messages(current_user.uuid)
        g.total_messages = len(data)


@app.route("/register", methods=['GET','POST'])
def register():
    if request.method == 'POST':
        inv1 = User.create(name=request.form['name'],
                           surname=request.form['surname'],
                           telephone=request.form['telephone'],
                           email=request.form['email'],
                           password=request.form['password1'])
        u = User.get_user_by_email(request.form['email'])

        send_email(
            "Activate Account",
            config.get_config("SENDER_EMAIL_ADDRESS"),
            [request.form['email']],
            render_template("email_activate_template.txt",
                            userid=str(u.uuid),
                            server=config.get_config('server'),
                            port=config.get_config('server_port')),
            render_template("email_activate_template.html",
                            userid=str(u.uuid),
                            server=config.get_config('server'),
                            port=config.get_config('server_port'))
        )

        return render_template("activate.html")
    else:
        return render_template("register.html")



@app.route("/users_signed_up", methods=['GET'])
def users_signed_up():
    return render_template("users_signed_up.html",
                           data=SignupUser.get_all()
                           )


@app.route("/disable_user/<id>", methods=['GET'])
@requires_auth
def disable_user(id):
    User.disabled_user(id)
    return redirect("/view_investors")

@app.route("/enable_user/<id>", methods=['GET'])
@requires_auth
def enable_user(id):
    User.enabled_user(id)
    return redirect("/view_investors")




@app.route("/terms_conditions", methods=['GET'])
def terms_conditions():
    return render_template("terms_conditions.html")


@app.route("/how_it_works", methods=['GET'])
def how_it_works():
    return render_template("how_it_works.html")


frm = DealTypeForm(request=request, endpoint_name="deal_types", caption="Deal Type")
frm.set_app(app)

frmProfile = ProfileForm(request=request, endpoint_name="profile", caption="User Profile")
frmProfile.set_app(app)

frmFAQAdmin = FAQForm(request=request, endpoint_name="faq_admin", caption="Frequenty Asked Questions")
frmFAQAdmin.set_app(app)

frmFavourites = FavouritesForm(request=request, endpoint_name="favourites", caption="Favourites")
frmFavourites.set_app(app)

frmAddDealForm = AddDealForm(request=request, endpoint_name="deals", caption="Deals")
frmAddDealForm.set_app(app)

frmInbox = InboxForm(request=request, endpoint_name="inbox", caption="Inbox")
frmInbox.set_app(app)


#@run_with_reloader
def run_server():
    local_debug = True
    app.jinja_env.cache = {}
    if local_debug == True:
        app.run(
            host=config.get_config('server'),
            port=int(config.get_config('server_port')),
            debug=True
        )
    else:
        serve(
            app,
            host=config.get_config('server'),
            port=int(config.get_config('server_port'))
        )
        app.run()
    log.log_normal("Server started")

if __name__ == '__main__':
    run_migration.run_migration()
    log.log_normal("Running Server")
    run_server()

