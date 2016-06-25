#!/usr/bin/python
# encoding:utf-8

import socket
import xmpp
import sys
import time
import json
import zlib
import base64
import argparse
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
    data = ''
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(addr)
    except socket.gaierror, e:
        sys.stderr.write('Unavailable host or port. Error code: ' + str(e[0]) + ', error message: ' + e[1] + '.')
        sys.exit(1)
    except socket.error, e:
        sys.stderr.write('Failed to create socket. Error code: ' + str(e[0]) + ', error message: ' + e[1] + '.')
        sys.exit(1)
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


SERVER = 'cicbd.jabber.org'
PORT = 5222
SINKER = 'sinker@' + SERVER  # sinker account : sinker@cicbd.jabber.org
ACCOUNT = socket.gethostname() + '@' + SERVER
DEFAULT_PASSWORD = '000000'


class Transmitter:
    """
    Transmit the data collected from ganglia-gmetad node to a sink node by a XMPP server,
        the XMPP server's default address is : localhost:5222,
        the sink node's default account is : udc2@localhost,
        the source node's default account is : hostname@localhost,
        data is collected once per second and transmited from `hostname@localhost` to `udc2@localhost`.
    """
    def __init__(self, frm=None, to=None):
        frm = ACCOUNT if frm is None else frm
        to = SINKER if to is None else frm
        self.__to = to
        self.__jid = xmpp.protocol.JID(frm)
        self.__client = xmpp.Client(self.__jid.getDomain(), debug=[])
        self.__client.connect()
        if self.__client.connected:
            sys.stdout.write('Connect to xmpp server %s successfully.' % self.__jid.getDomain())
        else:
            sys.stderr.write('Cannot connect to xmpp server %s.' % self.__jid.getDomain())
            sys.exit(1)

        self.ensure_account_exist()
        self.login()

    def ensure_account_exist(self):
        if xmpp.features.register(self.__client, self.__jid.getDomain(),
                                  {'username': self.__jid.getNode(), 'password': DEFAULT_PASSWORD}):
            sys.stdout.write("Successfully register user: %s!\n" % self.__jid.getNode())
        else:
            sys.stderr.write("Error while registering! User %s already exists or other errors.\n"
                             % self.__jid.getNode())

    def login(self):
        authres = self.__client.auth(self.__jid.getNode(), DEFAULT_PASSWORD)
        if authres:
            sys.stdout.write('Authentication passed.')
        else:
            sys.stderr.write('Unable to authenticate - check your login account(%s, %s).'
                             % (self.__jid.getNode(), DEFAULT_PASSWORD))
        self.__client.sendInitPresence()

    def transmit(self, data):
        self.__client.send(xmpp.protocol.Message(self.__to, data))


class GmetadDataClear(set):
    """
    If the reported time of data is the same as the collected last time, just remove it.
    """
    def __init__(self):
        super(GmetadDataClear, self).__init__()

    def dataclear(self, xml_str):
        """
        If the reported time of a host is duplicate, just remove the part from the data collected,
        If not, add the oid which represent a tuple like `(clustername/hostname, reported_time)` to a set.
        @:param xml_str
        @:return
        """
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
        """
        If the reported time of a host is duplicate, just remove the part from the data collected,
        If not, add the oid which represent a tuple like `(clustername/hostname, reported_time)` to a set.
        @:param xml_str
        @:return
        """
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
    Compress the data and encode them with base64.
    :param string:
    :param method:
    :return:
    """
    data = method.compress(string)
    return base64.encodestring(data)


def decompress(data, method=zlib):
    """
    Decompress the data and deencode them with base64.
    :param data:
    :param method:
    :return:
    """
    string = base64.decodestring(data)
    return method.decompress(string)

INTERVAL = 1


def start(source=('gmetad', ('localhost', 8651)), trans=None, debug=False):
    if source[0] == 'gmetad':
        dc = GmetadDataClear()
    else:
        dc = GmondDataClear()

    transmitter = Transmitter(trans[0], trans[1])

    while True:
        # 1. retrieve primitive xml data
        data = retrievedata(source[1], 'xml')     # type: xml_str
        # 2. data clean and format
        data = dc.dataclear(data)                 # type: xml_str
        data = XMLStrToDict(data)                 # type: dict
        data = json.dumps(data)                   # type: json_str
        if debug:
            sys.stdout.write(data)
        # 3. data compression
        data = compress(data, zlib)               # base64_str
        # 4. data transmission
        transmitter.transmit(data)
        time.sleep(INTERVAL)

if __name__ == '__main__':
    """
    The data is collected from `gmetad [ localhost:8651 ] ` by default
    and then transmitted out from a client to another client,
    the source client's default account is 'hostname@cicbd.jabber.org',
    the sinker client's default account is 'sinker@cicbd.jabber.org'.
    """
    parser = argparse.ArgumentParser()
    note = "The data is transmited out by a xmpp client, " \
           "the client's default account is `hostname@cicbd.jabber.org`, " \
           "you can specify the client's account."
    parser.add_argument('--frm', nargs='?', help=note)
    note = "The data is sent to a sinker client, " \
           "you can specify the client's account such as 'sinker@cicbd.jabber.org'."
    parser.add_argument('--to', nargs='?', help=note)

    note = "Specify the data source such as 'gmetad' or 'gmond'."
    parser.add_argument('--source', nargs='?', default='gmetad', help=note)
    note = "Specify the address of the data source such as 'localhost:8651' for gmetad or 'localhost:8649' for gmond."
    parser.add_argument('--addr', nargs='?', default='localhost:8651', help=note)

    note = "If you want to print data collected to stdout, set the debug=1."
    parser.add_argument('--debug', nargs='?', type=int, default=0, help=note)

    args = parser.parse_args()

    srcip = args.addr.split(':')[0]
    srcport = int(args.addr.split(':')[1])
    start((args.source, (srcip, srcport)), (args.frm, args.to), args.debug == 1)
    # start(('gmond', ('192.168.1.32', 8649)), (args.frm, args.to))
