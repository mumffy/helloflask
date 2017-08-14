from gevent import monkey
monkey.patch_all()

from gevent.wsgi import WSGIServer
# from hello_flask_restful import app
from hello_socket import socket

WSGIServer(('', 5000), application=socket).serve_forever()
