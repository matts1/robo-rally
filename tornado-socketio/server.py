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
        print 'Sending message from %s to users "%s"' % (data['user'], ", ".join(data['players'].split()))
        print 'action is "%s", data is "%s"' % (data['action'], data['text'])

        for player in data['players'].split(' '):
            conn = ChatConnection.participants.get(player)
            if conn is not None:
                conn.send(to_send)
            else:
                print 'player %s not found' % player
        self.finish()


class SocketIOHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('socket.io.js')


class ChatConnection(tornadio2.conn.SocketConnection):
    # Class level variable
    participants = {}
    no_name = set()

    def on_open(self, info):
        print 'client connected'
        ChatConnection.no_name.add(self)

    def on_close(self):
        print 'client disconnected'
        if self in ChatConnection.participants:
            del ChatConnection.participants[self]

    def on_message(self, msg):
        print "Putting %s in correct lobby" % msg
        ChatConnection.participants[msg.lower()] = self
        if self in ChatConnection.no_name:
            ChatConnection.no_name.remove(self)


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



