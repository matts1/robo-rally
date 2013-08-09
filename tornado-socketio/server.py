# coding: utf-8
import datetime
import tornado.web
try:
    import simplejson as json
except ImportError:
    import json
import tornadio2
from tornadio2 import SocketConnection, TornadioRouter, SocketServer, event


class IndexHandler(tornado.web.RequestHandler):
    def post(self):
        event_type = self.get_argument('event', 'message')
        event_data = self.get_argument('data', None)
        try:
            data = json.loads(event_data)
        except:
            data = event_data
        to_send = {
            'event': event_type,
            'data': data
        }
        print repr(event_data)
        print repr(data)

        for player in data['players'].split(' '):
            conn = ChatConnection.participants.get(player)
            conn.send(to_send)
        self.finish()


class SocketIOHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('socket.io.js')


class ChatConnection(tornadio2.conn.SocketConnection):
    # Class level variable
    participants = {}
    nolobby = {} # TODO: DO STUFF WITH THIS

    def on_open(self, info):
        print 'client connected'
        self.participants[None].add(self)

    def on_close(self):
        print 'client disconnected'
        for lobby in self.participants.values():
            if self in lobby:
                lobby.remove(self)


# Create chat server
ChatRouter = TornadioRouter(ChatConnection, dict(websocket_check=True))


# Create socket application
application = tornado.web.Application(
    ChatRouter.apply_routes([(r'/', IndexHandler),
                           (r'/socket.io/socket.io.js', SocketIOHandler)]),
    socket_io_port = 8001
)

if __name__ == '__main__':
    import logging
    logging.getLogger().setLevel(logging.DEBUG)

    # Create and start tornado server
    SocketServer(application)



