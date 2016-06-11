#!/usr/bin/python
# encoding:utf-8

import socket
import xmpp
import sys
import time
import json
import zlib
import base64
try:
    import xml.etree.cElementTree as cET
except ImportError:
    import xml.etree.ElementTree as cET


class XMLToDict(dict):
    """
    Convert a xml document or xml-format string to a dict.
    """
    def __init__(self, root):
        super(XMLToDict, self).__init__()
        self.update({root.tag: self.children(root)})

    def children(self, parent):
        if parent is None:
            return None
        else:
            result = {}
            # the result contains two part: {attribute: value, ...} and {child_tag: [{child}, ...], ...}
            # if there are any attributes for a tag, add to the result map
            if parent.attrib:
                result.update(parent.attrib)
            for node in parent.getchildren():
                if node.tag not in result:
                    result[node.tag] = []
                result[node.tag].append(self.children(node))
            return result


class XMLStrToDict(XMLToDict):
    """
    Convert a xml-format string to a dict.
    """
    def __init__(self, xml_str):
        root = cET.fromstring(xml_str)
        super(XMLStrToDict, self).__init__(root)


def retrievedata(addr=None, formatter='json'):
    """
    Retrieve metric data from ganglia-gmetad node, the default `address:port` of gmetad node is `localhost:8651`,
    you can specified the `address:port` and the data format : `dict | json_str | xml_str`.
    :param addr:
    :param formatter:
    :return:
    """
    addr = ('localhost', 8651) if addr is None else addr
    client = None
    data = ''
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(addr)
    except socket.gaierror, e:
        print 'Unavailable host or port. Error code: ' + str(e[0]) + ', error message: ' + e[1]
    except socket.error, e:
        print 'Failed to create socket. Error code: ' + str(e[0]) + ', error message: ' + e[1]
    while True:
        buf = client.recv(1024)
        if len(buf) == 0:
            break
        data = ''.join([data, buf])
    if data:
        if formatter == 'dict':
            root = cET.fromstring(data)
            return XMLToDict(root)
        if formatter == 'json':
            root = cET.fromstring(data)
            return json.dumps(XMLToDict(root))
        if formatter == 'xml':
            return data
    return ''


class Transmitter:
    """
    Transmit the data collected from ganglia-gmetad node to a sink node by a XMPP server,
        the XMPP server's default address is : localhost:5222,
        the sink node's default account is : udc2@localhost,
        the source node's default account is : hostname@localhost,
        data is collected once per second and transmited from `hostname@localhost` to `udc2@localhost`.
    """
    __ACCOUNT = socket.gethostname() + '@localhost'
    __PASSWORD = '000000'
    __TO = 'udc2@localhost'

    def __init__(self, server_addr=('localhost', 5222)):
        self.__jid = xmpp.protocol.JID(Transmitter.__ACCOUNT)
        self.__client = xmpp.Client(self.__jid.getDomain(), debug=[])
        self.__client.connect(server=server_addr)
        if self.__client.connected:
            print 'connect to xmpp server %s successfully' % self.__jid.getDomain()
        else:
            print 'cannot connect to xmpp server %s' % self.__jid.getDomain()
            sys.exit()
        auth = self.__client.auth(self.__jid.getNode(), Transmitter.__PASSWORD)
        if auth:
            print 'authentication passed'
        else:
            print 'authentication failed for token(%s, %s)' % (self.__jid.getNode(), Transmitter.__PASSWORD)
        self.__client.sendInitPresence()

    def transmit(self, data):
        self.__client.send(xmpp.protocol.Message(Transmitter.__TO, data))


class GmetadDataClear(set):
    """
    If the reported time of data is the same as the collected last time, just remove it.
    """
    def __init__(self):
        super(GmetadDataClear, self).__init__()

    def dataclear(self, xml_str):
        root = cET.fromstring(xml_str)
        for grid_node in root.findall('GRID'):
            for cluster_node in grid_node.findall('CLUSTER'):
                for host_node in cluster_node.findall('HOST'):
                    hostid = ''.join([cluster_node.get('NAME'), '/', host_node.get('NAME')])
                    reported = host_node.get('REPORTED')
                    oid = (hostid, reported)
                    if oid in self:
                        cluster_node.remove(host_node)
                    else:
                        self.add(oid)
        return cET.tostring(root)


class GmondDataClear(set):
    """
    If the reported time of data is the same as the collected last time, just remove it.
    """
    def __init__(self):
        super(GmondDataClear, self).__init__()

    def dataclear(self, xml_str):
        root = cET.fromstring(xml_str)
        for cluster_node in root.findall('CLUSTER'):
            for host_node in cluster_node.findall('HOST'):
                hostid = ''.join([cluster_node.get('NAME'), '/', host_node.get('NAME')])
                reported = host_node.get('REPORTED')
                oid = (hostid, reported)
                if oid in self:
                    cluster_node.remove(host_node)
                else:
                    self.add(oid)
        return cET.tostring(root)


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

INTERVAL = 1


def start():
    dc = GmondDataClear()
    transmitter = Transmitter(('192.168.1.113', 5222))
    while True:
        # 1. retrieve primitive xml data
        data_xml = retrievedata(('192.168.1.32', 8649), 'xml')
        # 2. data clean and format
        data_cleared = dc.dataclear(data_xml)
        data_dict = XMLStrToDict(data_cleared)
        data_json = json.dumps(data_dict)
        # 3. data compression
        data = compress(data_json, zlib)
        # 4. data transmission
        transmitter.transmit(data)
        time.sleep(INTERVAL)

if __name__ == '__main__':
    start()
