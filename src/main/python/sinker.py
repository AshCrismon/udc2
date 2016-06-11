#!/usr/bin/python
# encoding:utf-8

import threading
import xmpp
import sys
import zlib
import base64


def compress(string, method=zlib):
    """
    Compress the data and encode them with base64
    :param string:
    :param method:
    :return:
    """
    data = method.compress(string)
    return base64.encodestring(data)


def decompress(data, method=zlib):
    """
    Decompress the data and deencode them with base64
    :param data:
    :param method:
    :return:
    """
    string = base64.decodestring(data)
    return method.decompress(string)


class DataSinker(threading.Thread):
    __ACCOUNT = 'udc2@localhost'
    __PASSWORD = '000000'

    def __init__(self, server_addr=('localhost', 5222)):
        super(DataSinker, self).__init__()
        self.__jid = xmpp.protocol.JID(DataSinker.__ACCOUNT)
        self.__client = xmpp.Client(self.__jid.getDomain(), debug=[])
        self.__client.connect(server=server_addr)
        if self.__client.connected:
            print 'connect to xmpp server %s successfully' % self.__jid.getDomain()
        else:
            print 'cannot connect to xmpp server %s' % self.__jid.getDomain()
            sys.exit()
        auth = self.__client.auth(self.__jid.getNode(), DataSinker.__PASSWORD)
        if auth:
            print 'authentication passed'
        else:
            print 'authentication failed for token(%s, %s)' % (self.__jid.getNode(), DataSinker.__PASSWORD)
        self.__client.sendInitPresence()

    def register_handler(self, handler):
        self.__client.RegisterHandler('message', handler)

    def run(self):
        # self.__client.RegisterHandler('message', self.register_handler2)
        while True:
            if self.__client.Process(1) is None:
                print 'lost connection'
                break


def msg_handler(client, msg):
    print '1--------->', decompress(msg.getBody())


if __name__ == '__main__':
    datasinker = DataSinker(server_addr=('192.168.1.113', 5222))
    datasinker.register_handler(msg_handler)
    datasinker.register_handler(msg_handler2)
    datasinker.start()