from gevent.wsgi import WSGIServer
from werkzeug.debug import DebuggedApplication
from run import app

http_server = WSGIServer(('', 5000), DebuggedApplication(app))
http_server.serve_forever()