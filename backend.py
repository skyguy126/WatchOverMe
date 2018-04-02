import signal, json
from random import randint
import tornado, tornado.ioloop, tornado.web

status = {
    'c1' : {
        'state' : False,
        'index' : 0
    },
    'c2' : {
        'state' : False,
        'index' : 1
    },
    'c3' : {
        'state' : False,
        'index' : 2
    },
    'c4' : {
        'state' : False,
        'index' : 3
    },
    'c5' : {
        'state' : False,
        'index' : 4
    }
}

class RootHandler(tornado.web.RequestHandler):

    def get(self):
        self.set_header("Content-Type", "text/html")
        self.render("webapp/index.html", google_maps_api_key=secure['google_maps_api_key'])

class StatusHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get(self):
        self.set_header("Content-Type", "appliation/json")
        self.write(json.dumps(status) + '\n')

class ChangeHandler(tornado.web.RequestHandler):

    # send params as {'key':'c1', 'val':True}

    def post(self):
        data = json.loads(self.request.body)
        status[data['key']]['state'] = data['val']

secure = None
app = tornado.web.Application([
        (r"/", RootHandler),
        (r"/status", StatusHandler),
        (r"/change", ChangeHandler),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path" : "./webapp/static"}),
        (r'/(favicon\.ico)', tornado.web.StaticFileHandler, {'path': "./webapp/static"}),
])

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    with open('secure.json', 'r') as f:
        secure = json.loads(f.read())

    print "Starting webserver..."
    app.listen(25565)
    tornado.ioloop.IOLoop.instance().start()
