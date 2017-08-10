from gevent import monkey
monkey.patch_all()

from gevent.wsgi import WSGIServer
from hello_flask_restful import app

WSGIServer(('', 5000), application=app).serve_forever()
