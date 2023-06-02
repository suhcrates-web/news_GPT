from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from app_with_socket import app  # replace with your Flask app import

http_server = WSGIServer(('', 5232), app, handler_class=WebSocketHandler)
http_server.serve_forever()