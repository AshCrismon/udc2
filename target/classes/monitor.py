#!/usr/bin/python
# encoding:utf-8

import xml.etree.cElementTree as ET
import socket


class XMLToDict(dict):
    def __init__(self, element_tree):
        super(XMLToDict, self).__init__()
        if element_tree:
            for element in element_tree:
                if element.attrib:
                    self.update({element.tag: element.attrib})
                children = XMLToDict(element.getchildren())
                if children:
                    self[element.tag].update(children)


HOST = 'localhost'
PORT = 8651
ADDR = (HOST, PORT)


def retrievedata():
	client = None
	data = ''
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDR)
    except socket.gaierror, e:
        print 'Unavailable host or port. Error code: ' + str(e[0]) + ', error message: ' + e[1]
    except socket.error, e:
        print 'Failed to create socket. Error code: ' + str(e[0]) + ', error message: ' + e[1]
    while True:
        buf = client.recv(1024)
        if len(buf) == 0:
            break
        data = ''.join([data, buf])
    root = ET.fromstring(data)
    return XMLToDict(root)
	

if __name__ == '__main__':
    client = None
    data = ''
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(ADDR)
    except socket.gaierror, e:
        print 'Unavailable host or port. Error code: ' + str(e[0]) + ', error message: ' + e[1]
    except socket.error, e:
        print 'Failed to create socket. Error code: ' + str(e[0]) + ', error message: ' + e[1]
    while True:
        buf = client.recv(1024)
        if len(buf) == 0:
            break
        data = ''.join([data, buf])
    root = ET.fromstring(data)
    result = XMLToDict(root)
    print result
