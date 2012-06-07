#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
DATA STRUCTURES OBJECTS
'''


class AdminSocketObject():
    def __init__(self, boxUUID, hostname, platform, websocketInstance):
        self.uuid = boxUUID
        self.platform = platform
        self.hostname = hostname
        self.webSocket = websocketInstance

    def getWebSocket(self):
        return self.webSocket

    def getUUID(self):
        return self.uuid

    def getPlatform(self):
        return self.platform

    def getHostname(self):
        return self.hostname


class CommandSocketObject():
    ''' Socket Tracking Object '''
    def __init__(self, boxUUID, hostname, platform,
                     username, websocketInstance):
        self.uuid = boxUUID
        self.platform = platform
        self.hostname = hostname
        self.webSocket = websocketInstance
        self.username = username

    def getWebSocket(self):
        return self.webSocket

    def getUUID(self):
        return self.uuid

    def getPlatform(self):
        return self.platform

    def getHostname(self):
        return self.hostname

    def getUsername(self):
        return self.username


class CommandDataObject():
    '''Command Data Object'''
    def __init__(self, boxUUID, hostname, platform, username, command)
        self.uuid = boxUUID
        self.platform = platform
        self.hostname = hostname
        self.username = username
        self.command = command

    def createJSONObject():
        pythonDictionaryObject = {'uuid':self.uuid,'hostname':self.hostname,
         'platform':self.platform,'username':self.username,'command':self.command}

        jsonObject = json.dumps(pythonDictionaryObject)



