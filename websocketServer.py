#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
import time
import optparse
import json
from dataStructures import AdminSocketObject, CommandSocketObject, CommandDataObject


__author__ = "f47h3r - Chase Schultz"

clientListeners = {}
adminListeners = {}
names = {}


class SaveSocket():
    '''Not sure if useful yet.... may need it'''
    def __init__(self):
        pass


class PostHandler(tornado.web.RequestHandler):
    """
    Handles Posted Commands and Sends to Clients
    """
    def post(self):
        if 'message' in self.request.arguments:
            message = self.request.arguments['message'][0]
            group = self.request.arguments.get('group', ['default'])[0]
            print '%s:MESSAGE to %s:%s' % (time.time(), group, message)

            #For every Client Listener in the group specified in post data
            for client in listeners.get(group, []):
                client.write_message(message)

            websocket = listeners.get('admin', ['default'])[0].webSocket

            print 'THE WEBSOCKET = \n\n'
            print websocket
            websocket.write_message(message)
            return 'true'
        return 'false'


class SpawnClientSocket(tornado.web.RequestHandler):
    """
    Handles Spawn of Shells
    """
    def post(self):
        user = self.request.arguments['user'][0]

        for adminSocket in adminListeners:
            commandObject = CommandDataObject(adminListeners[adminSocket].getUUID(), adminListeners[adminSocket].getHostname(), adminListeners[adminSocket].getPlatform(), user, 'spawnclientsocket', '')
            jsonCommandObject = commandObject.createJSONObject()
            print 'JSON COMMAND OBJECT: %s' % jsonCommandObject
            socketInstance = adminListeners[adminSocket].getWebSocket()
            socketInstance.write_message(jsonCommandObject)

        return 'true'


class DistributeHandler(tornado.websocket.WebSocketHandler):
    ''' Registers boxes to groups and manages websockets '''
    def open(self, params):
        params = str(params)
        self.__getParameters__(params)
        print 'Parameters:\n\tType: %s\n\tHostname: %s\n\tPlatform: %s\n\tUUID: %s' % (str(self.type), str(self.hostname), str(self.platform), str(self.uuid))

        """
        group, uuid, name = params.split('/')
        self.group = group or 'default'
        self.uuid = uuid or 'fuck...no UUUID'
        self.name = name or 'anonymous'
        """
        self.__saveWebSocket__()
        print '%s:CONNECT to %s from %s' % (time.time(), self.type, self.hostname)

    def on_message(self, message):
        ''' Sends Messages back to the shell interface '''
        print message
        '''
        for client in listeners.get("shell", []):
            client.write_message(message)
        pass
        '''

    def on_close(self):
        ''' Closes out regular sockets... needs to be addapted for adminObject Structure'''
        #FIXME - READ ABOVE COMMENT!!!\
        print 'CLOSE SOCKET CALLED BY SERVER!!!!! FUCKKK!K!K!'
        if self.uuid in adminListeners:
            #adminListeners[self.uuid].remove(self)
            del adminListeners[self.uuid]
        print '%s:DISCONNECT from %s' % (time.time(), self.hostname)

    def __getParameters__(self, params):
        print 'Parameters: %s' % str(params)
        params = params.split('/')
        if params[0] == 'admin':
            self.type = params[0]
            self.hostname = params[1]
            self.platform = params[2]
            self.uuid = params[3]
        elif params[0] == 'command':
            self.type = params[0]
            self.hostname = params[1]
            self.platform = params[2]
            self.uuid = params[3]
            self.username = params[4]
        else:
            print 'Unable to Obtain Parameters'

    def __saveWebSocket__(self):
        #If group isn't already in the list add it.
        '''THIS IS A CLUSTERFUCK.... CLEAN IT UP!!!!'''
        if self.type == 'admin':
            print 'Made it to AdminSocketCreation\n\n'
            newAdminSocketObject = AdminSocketObject(self.uuid, self.hostname, self.platform, self)
            adminListeners[self.uuid] = newAdminSocketObject
        elif self.type == 'command':
            newCommandSocketObject = CommandSocketObject(self.uuid, self.hostname, self.platform, self.username, self)
            clientListeners[self.uuid] = newCommandSocketObject


'''

#Example Websocket Code

class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print 'new connection'
        self.write_message("Hello Client!")

    def on_message(self, message):
        print 'message received %s' % message
        response = raw_input('Type a response:')
        self.write_message(response)

    def on_close(self):
        print 'connection closed'

'''

if __name__ == "__main__":
    usage = __doc__
    version = "0.01"
    parser = optparse.OptionParser(usage, None, optparse.Option, version)
    parser.add_option('-p',
                      '--port',
                      default='9002',
                      dest='port',
                      help='Listener Port')
    parser.add_option('-l',
                      '--listen',
                      default='127.0.0.1',
                      dest='ip',
                      help='Listener IP address')
    (options, args) = parser.parse_args()
    application = tornado.web.Application([
#For Example
#    (r'/ws', WSHandler),
    (r'/', PostHandler),
    (r'/endpoint/(.*)', DistributeHandler),
    (r'/spawnshells', SpawnClientSocket)
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(int(options.port), address=options.ip)
    tornado.ioloop.IOLoop.instance().start()
