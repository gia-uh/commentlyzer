from gevent.pywsgi import WSGIServer
from app import create_app

app = create_app('production')

http_server = WSGIServer(('', 8001), app)
http_server.serve_forever()