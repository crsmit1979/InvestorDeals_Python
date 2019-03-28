from functools import wraps
from flask import session, redirect

def convert_to_bool(value):
    try:
        return float(value) == 1
    except:
        return 0


def get_json_value(js, name):
    try:
            return js[name]
    except:
        return None


def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    if 'profile' not in session:
      # Redirect to Login page here
      return redirect('/login')
    return f(*args, **kwargs)

  return decorated
