#!/usr/bin/python
# encoding:utf-8

import threading
import xmpp
import sys
import zlib
import base64
import socket
import argparse
import json
from pymongo import MongoClient


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


SERVER = 'cicbd.jabber.org'
PORT = 5222
SINKER = 'sinker@' + SERVER  # sinker account : sinker@cicbd.jabber.org
DEFAULT_PASSWORD = '000000'


class DataSinker(threading.Thread):
    """
    Receive data from other xmpp clients who monitor the gmetad or gmond node and send out the data collected.
    """
    def __init__(self, sinker=None):
        super(DataSinker, self).__init__()
        self.__account = SINKER if sinker is None else sinker
        self.__jid = xmpp.protocol.JID(self.__account)
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

    def register_handler(self, handler):
        self.__client.RegisterHandler('message', handler)

    def run(self):
        # self.__client.RegisterHandler('message', self.register_handler2)
        while True:
            if self.__client.Process(1) is None:
                print 'lost connection!'
                break


def todigit(string):
    try:
        n = float(string)
        return n
    except ValueError:
        return string


class GmondDataAdaptor(dict):
    """
    Format the data received from gmond node.
    """
    def __init__(self, data):
        super(GmondDataAdaptor, self).__init__()
        self['metriclist'] = []
        self['hostdesclist'] = []
        self['metricdesclist'] = []
        if data:
            for cluster in data['GANGLIA_XML']['CLUSTER']:
                if 'HOST' in cluster:
                    for host in cluster['HOST']:
                        hostdesc = self.gethostdesc(cluster['NAME'], host)
                        cid = cluster['NAME'] + '/' + host['NAME']
                        metricdata = []
                        if 'METRIC' in host:
                            for metric in host['METRIC']:
                                metricdata.append(self.getmetricdata(metric, host['REPORTED']))
                                metricdesc = self.getmetricdesc(cluster['NAME'], host['NAME'], host['IP'], metric)
                                self['metricdesclist'].append(metricdesc)
                            self['metriclist'].append({'cid': cid, 'data': metricdata})
                            self['hostdesclist'].append(hostdesc)

    @staticmethod
    def gethostdesc(cluster_name, host):
        """
        Provide an identical format for the data, just like:
        {
            hid: 'cluster_name/hostname'
            cluster: '',
            gmond_started: '',
            name: '',
            tags: '',
            ip: '',
            tmax: '',
            tn: '',
            location: '',
            dmax: ''

        }
        :param cluster_name:
        :param host:
        :return:
        """
        return {
            'hid': cluster_name + '/' + host['NAME'],
            'cluster': cluster_name,
            'gmond_started': host['GMOND_STARTED'],
            'name': host['NAME'],
            'tags': host['TAGS'],
            'ip': host['IP'],
            'tmax': host['TMAX'],
            'tn': host['TN'],
            'location': host['LOCATION'],
            'dmax': host['DMAX']
        }

    @staticmethod
    def getmetricdata(metric, timestamp):
        """
        Provide an identical format for the data, just like:
        {
            cid: 'cluster_name/hostname',
            data: [
                {
                    timestamp: value,
                    metric: 'cpu_aidle',
                    value: ''
                },
                ...
            ]
        }
        :param metric:
        :param timestamp:
        :return:
        """
        return {
            'metric': metric['NAME'],
            'value': todigit(metric['VAL']),
            'clock': int(timestamp)
        }

    @staticmethod
    def getmetricdesc(cluster_name, hostname, ip, metric):
        """
        Provide an identical format for the data, just like:
        {
            mid: 'cluster_name/hostname:ip/metric',
            title: '',
            desc: '',
            group: '',
            tn: '',
            tmax: '',
            dmax: '',
            units: '',
            source: '',
        }
        :param cluster_name:
        :param hostname:
        :param ip:
        :param metric:
        :return:
        """
        mid = cluster_name + '/' + hostname + '/' + metric['NAME']

        metricdesc = {
            'mid': mid,
            'tmax': metric['TMAX'],
            'tn': metric['TN'],
            'dmax': metric['DMAX'],
            'source': metric['SOURCE'],
            'units': metric['UNITS']
        }

        for extradata in metric['EXTRA_DATA']:
            for element in extradata['EXTRA_ELEMENT']:
                metricdesc.update({element['NAME']: element['VAL']})
        return metricdesc


class GmetadDataAdaptor(GmondDataAdaptor):
    """
    Format the data received from gmetad node.
    """
    def __init__(self, data):
        super(GmetadDataAdaptor, self).__init__(None)
        if data:
            for grid in data['GANGLIA_XML']['GRID']:
                for cluster in grid['CLUSTER']:
                    if 'HOST' in cluster:
                        for host in cluster['HOST']:
                            hostdesc = self.gethostdesc(cluster['NAME'], host)
                            cid = cluster['NAME'] + '/' + host['NAME']
                            metricdata = []
                            for metric in host['METRIC']:
                                metricdata.append(self.getmetricdata(metric, host['REPORTED']))
                                metricdesc = self.getmetricdesc(cluster['NAME'], host['NAME'], host['IP'], metric)
                                self['metricdesclist'].append(metricdesc)
                            self['metriclist'].append({'cid': cid, 'data': metricdata})
                            self['hostdesclist'].append(hostdesc)


DBCONFIG = {
    'URL': 'mongodb://localhost:27017/udc2_ganglia',

    'HOST': '',
    'PORT': 27017,
    'USERNAME': 'ganglia',
    'PASSWORD': 'ganglia',

    'MAX_POOL_SIZE': 200,  # The maximum number of connections that the pool will open simultaneously

    'DBNAME': 'udc2_ganglia',
    'COLLECTIONS': {
        'HOST_INFO': 'host_info',       # This collection is used to save stable host information
        'METRIC_INFO': 'metric_info'    # This collection is used to save stable metric information
    }
}


class MongodbOps(object):
    """
    Provide base options for mongodb.
    """
    def __init__(self, host=None, port=None, url=None):
        if host and port:
            self.__client = MongoClient(host, port, maxPoolSize=DBCONFIG['MAX_POOL_SIZE'])
            self.__db = self.__client.get_database(DBCONFIG['DBNAME'])
        elif url:
            self.__client = MongoClient(url, maxPoolSize=DBCONFIG['MAX_POOL_SIZE'])
            self.__db = self.__client.get_default_database()
        else:
            self.__client = MongoClient(DBCONFIG['URL'], maxPoolSize=DBCONFIG['MAX_POOL_SIZE'])
            self.__db = self.__client.get_default_database()

    def save_or_update(self, collection_name, data):
        return self.db[collection_name].save(data)

    def insert(self, collection_name, documents):
        return self.db[collection_name].insert_many(documents)

    def create_index(self, collection_name, keys):
        self.db[collection_name].create_index(keys)

    def drop_indexes(self, collection_name):
        self.db[collection_name].drop_indexes()

    @property
    def db(self):
        return self.__db
    
    @property
    def client(self):
        return self.__client


class MongoDBSaver(MongodbOps):
    """
    Used to save data to mongodb, the data collected is split into three part:
    metric data, metric description, host description.
    """
    def __init__(self, host=None, port=None, url=None):
        super(MongoDBSaver, self).__init__(host, port, url)

    def _save_metric_data(self, metriclist):
        for metric in metriclist:
            self.insert(metric['cid'], metric['data'])

    def _save_metric_desc(self, metricdesclist):
        for metricdesc in metricdesclist:
            result = self.db[DBCONFIG['COLLECTIONS']['METRIC_INFO']].find_one({'mid': metricdesc['mid']})
            if not result:
                result = {}
            result.update(metricdesc)
            self.save_or_update(DBCONFIG['COLLECTIONS']['METRIC_INFO'], result)

    def _save_host_desc(self, hostdesclist):
        for hostdesc in hostdesclist:
            result = self.db[DBCONFIG['COLLECTIONS']['HOST_INFO']].find_one({'hid': hostdesc['hid']})
            if not result:
                result = {}
            result.update(hostdesc)
            self.save_or_update(DBCONFIG['COLLECTIONS']['HOST_INFO'], result)

    def save(self, data):
        if data:
            self._save_metric_data(data['metriclist'])
            self._save_metric_desc(data['metricdesclist'])
            self._save_host_desc(data['hostdesclist'])

    def msg_saver(self, client, msg):
        data_recv = json.loads(decompress(msg.getBody()))  # json_str --> dict
        if data_recv['GANGLIA_XML']['SOURCE'] == 'gmetad':
            output = GmetadDataAdaptor(data_recv)
        else:
            output = GmondDataAdaptor(data_recv)
        self.save(output)


class Transmitter(threading.Thread):
    """
    Used to transmit the data received to any new connection to port 6666.
    """
    def __init__(self, debug=False):
        super(Transmitter, self).__init__()
        self.__debug = debug
        self.__addr = ('', 6666)
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.bind(self.__addr)
        self.__sock.listen(5)
        self.data_recv = ''

    def flush_msg(self, client, msg):
        self.data_recv = decompress(msg.getBody())
        if self.__debug:
            sys.stdout.write(self.data_recv)

    def transmit(self):
        while True:
            print('waiting for connection...')
            tcpclientsock, remoteaddr = self.__sock.accept()
            print('connect from ', remoteaddr)
            tcpclientsock.send(self.data_recv.encode('utf-8'))
            tcpclientsock.close()

    def run(self):
        self.transmit()


if __name__ == '__main__':

    gmonddata = {"GANGLIA_XML": {"SOURCE": "gmond", "VERSION": "3.7.2", "CLUSTER": [{"NAME": "cloudservers", "URL": "unspecified", "HOST": [{"GMOND_STARTED": "1465785138", "NAME": "192.168.1.32", "TAGS": "", "IP": "192.168.1.32", "TMAX": "20", "TN": "15", "REPORTED": "1465817105", "LOCATION": "unspecified", "DMAX": "86400", "METRIC": [{"SLOPE": "both", "NAME": "mem_buffers", "VAL": "318448", "TMAX": "180", "TN": "17", "SOURCE": "gmond", "UNITS": "KB", "DMAX": "0", "EXTRA_DATA": [{"EXTRA_ELEMENT": [{"NAME": "GROUP", "VAL": "memory"}, {"NAME": "DESC", "VAL": "Amount of buffered memory"}, {"NAME": "TITLE", "VAL": "Memory Buffers"}]}], "TYPE": "float"}, {"SLOPE": "both", "NAME": "cpu_system", "VAL": "0.6", "TMAX": "90", "TN": "34", "SOURCE": "gmond", "UNITS": "%", "DMAX": "0", "EXTRA_DATA": [{"EXTRA_ELEMENT": [{"NAME": "GROUP", "VAL": "cpu"}, {"NAME": "DESC", "VAL": "Percentage of CPU utilization that occurred while executing at the system level"}, {"NAME": "TITLE", "VAL": "CPU System"}]}], "TYPE": "float"}, {"SLOPE": "both", "NAME": "part_max_used", "VAL": "45.8", "TMAX": "180", "TN": "119", "SOURCE": "gmond", "UNITS": "%", "DMAX": "0", "EXTRA_DATA": [{"EXTRA_ELEMENT": [{"NAME": "GROUP", "VAL": "disk"}, {"NAME": "DESC", "VAL": "Maximum percent used for all partitions"}, {"NAME": "TITLE", "VAL": "Maximum Disk Space Used"}]}], "TYPE": "float"}, {"SLOPE": "both", "NAME": "disk_total", "VAL": "485.532", "TMAX": "1200", "TN": "3181", "SOURCE": "gmond", "UNITS": "GB", "DMAX": "0", "EXTRA_DATA": [{"EXTRA_ELEMENT": [{"NAME": "GROUP", "VAL": "disk"}, {"NAME": "DESC", "VAL": "Total available disk space"}, {"NAME": "TITLE", "VAL": "Total Disk Space"}]}], "TYPE": "double"}, {"SLOPE": "both", "NAME": "mem_shared", "VAL": "0", "TMAX": "180", "TN": "17", "SOURCE": "gmond", "UNITS": "KB", "DMAX": "0", "EXTRA_DATA": [{"EXTRA_ELEMENT": [{"NAME": "GROUP", "VAL": "memory"}, {"NAME": "DESC", "VAL": "Amount of shared memory"}, {"NAME": "TITLE", "VAL": "Shared Memory"}]}], "TYPE": "float"}, {"SLOPE": "both", "NAME": "cpu_wio", "VAL": "0.2", "TMAX": "90", "TN": "34", "SOURCE": "gmond", "UNITS": "%", "DMAX": "0", "EXTRA_DATA": [{"EXTRA_ELEMENT": [{"NAME": "GROUP", "VAL": "cpu"}, {"NAME": "DESC", "VAL": "Percentage of time that the CPU or CPUs were idle during which the system had an outstanding disk I/O request"}, {"NAME": "TITLE", "VAL": "CPU wio"}]}], "TYPE": "float"}, {"SLOPE": "zero", "NAME": "machine_type", "VAL": "x86_64", "TMAX": "1200", "TN": "58", "SOURCE": "gmond", "UNITS": "", "DMAX": "0", "EXTRA_DATA": [{"EXTRA_ELEMENT": [{"NAME": "GROUP", "VAL": "system"}, {"NAME": "DESC", "VAL": "System architecture"}, {"NAME": "TITLE", "VAL": "Machine Type"}]}], "TYPE": "string"}, {"SLOPE": "both", "NAME": "proc_total", "VAL": "360", "TMAX": "950", "TN": "58", "SOURCE": "gmond", "UNITS": " ", "DMAX": "0", "EXTRA_DATA": [{"EXTRA_ELEMENT": [{"NAME": "GROUP", "VAL": "process"}, {"NAME": "DESC", "VAL": "Total number of processes"}, {"NAME": "TITLE", "VAL": "Total Processes"}]}], "TYPE": "uint32"}, {"SLOPE": "zero", "NAME": "cpu_num", "VAL": "4", "TMAX": "1200", "TN": "58", "SOURCE": "gmond", "UNITS": "CPUs", "DMAX": "0", "EXTRA_DATA": [{"EXTRA_ELEMENT": [{"NAME": "GROUP", "VAL": "cpu"}, {"NAME": "DESC", "VAL": "Total number of CPUs"}, {"NAME": "TITLE", "VAL": "CPU Count"}]}], "TYPE": "uint16"}, {"SLOPE": "zero", "NAME": "cpu_speed", "VAL": "2500", "TMAX": "1200", "TN": "58", "SOURCE": "gmond", "UNITS": "MHz", "DMAX": "0", "EXTRA_DATA": [{"EXTRA_ELEMENT": [{"NAME": "GROUP", "VAL": "cpu"}, {"NAME": "DESC", "VAL": "CPU Speed in terms of MHz"}, {"NAME": "TITLE", "VAL": "CPU Speed"}]}], "TYPE": "uint32"}, {"SLOPE": "both", "NAME": "pkts_out", "VAL": "0.35", "TMAX": "300", "TN": "180", "SOURCE": "gmond", "UNITS": "packets/sec", "DMAX": "0", "EXTRA_DATA": [{"EXTRA_ELEMENT": [{"NAME": "GROUP", "VAL": "network"}, {"NAME": "DESC", "VAL": "Packets out per second"}, {"NAME": "TITLE", "VAL": "Packets Sent"}]}], "TYPE": "float"}, {"SLOPE": "both", "NAME": "swap_free", "VAL": "0", "TMAX": "180", "TN": "17", "SOURCE": "gmond", "UNITS": "KB", "DMAX": "0", "EXTRA_DATA": [{"EXTRA_ELEMENT": [{"NAME": "GROUP", "VAL": "memory"}, {"NAME": "DESC", "VAL": "Amount of available swap memory"}, {"NAME": "TITLE", "VAL": "Free Swap Space"}]}], "TYPE": "float"}, {"SLOPE": "both", "NAME": "cpu_steal", "VAL": "0.0", "TMAX": "90", "TN": "34", "SOURCE": "gmond", "UNITS": "%", "DMAX": "0", "EXTRA_DATA": [{"EXTRA_ELEMENT": [{"NAME": "GROUP", "VAL": "cpu"}, {"NAME": "DESC", "VAL": "cpu_steal"}, {"NAME": "TITLE", "VAL": "CPU steal"}]}], "TYPE": "float"}, {"SLOPE": "both", "NAME": "load_one", "VAL": "0.00", "TMAX": "70", "TN": "29", "SOURCE": "gmond", "UNITS": " ", "DMAX": "0", "EXTRA_DATA": [{"EXTRA_ELEMENT": [{"NAME": "GROUP", "VAL": "load"}, {"NAME": "DESC", "VAL": "One minute load average"}, {"NAME": "TITLE", "VAL": "One Minute Load Average"}]}], "TYPE": "float"}, {"SLOPE": "zero", "NAME": "mem_total", "VAL": "3582528", "TMAX": "1200", "TN": "58", "SOURCE": "gmond", "UNITS": "KB", "DMAX": "0", "EXTRA_DATA": [{"EXTRA_ELEMENT": [{"NAME": "GROUP", "VAL": "memory"}, {"NAME": "DESC", "VAL": "Total amount of memory displayed in KBs"}, {"NAME": "TITLE", "VAL": "Memory Total"}]}], "TYPE": "float"}, {"SLOPE": "zero", "NAME": "os_release", "VAL": "3.2.30", "TMAX": "1200", "TN": "58", "SOURCE": "gmond", "UNITS": "", "DMAX": "0", "EXTRA_DATA": [{"EXTRA_ELEMENT": [{"NAME": "GROUP", "VAL": "system"}, {"NAME": "DESC", "VAL": "Operating system release date"}, {"NAME": "TITLE", "VAL": "Operating System Release"}]}], "TYPE": "string"}, {"SLOPE": "both", "NAME": "proc_run", "VAL": "1", "TMAX": "950", "TN": "58", "SOURCE": "gmond", "UNITS": " ", "DMAX": "0", "EXTRA_DATA": [{"EXTRA_ELEMENT": [{"NAME": "GROUP", "VAL": "process"}, {"NAME": "DESC", "VAL": "Total number of running processes"}, {"NAME": "TITLE", "VAL": "Total Running Processes"}]}], "TYPE": "uint32"}, {"SLOPE": "both", "NAME": "load_five", "VAL": "0.04", "TMAX": "325", "TN": "29", "SOURCE": "gmond", "UNITS": " ", "DMAX": "0", "EXTRA_DATA": [{"EXTRA_ELEMENT": [{"NAME": "GROUP", "VAL": "load"}, {"NAME": "DESC", "VAL": "Five minute load average"}, {"NAME": "TITLE", "VAL": "Five Minute Load Average"}]}], "TYPE": "float"}, {"SLOPE": "zero", "NAME": "gexec", "VAL": "OFF", "TMAX": "300", "TN": "180", "SOURCE": "gmond", "UNITS": "", "DMAX": "0", "EXTRA_DATA": [{"EXTRA_ELEMENT": [{"NAME": "GROUP", "VAL": "core"}, {"NAME": "DESC", "VAL": "gexec available"}, {"NAME": "TITLE", "VAL": "Gexec Status"}]}], "TYPE": "string"}, {"SLOPE": "both", "NAME": "disk_free", "VAL": "365.745", "TMAX": "180", "TN": "119", "SOURCE": "gmond", "UNITS": "GB", "DMAX": "0", "EXTRA_DATA": [{"EXTRA_ELEMENT": [{"NAME": "GROUP", "VAL": "disk"}, {"NAME": "DESC", "VAL": "Total free disk space"}, {"NAME": "TITLE", "VAL": "Disk Space Available"}]}], "TYPE": "double"}, {"SLOPE": "both", "NAME": "mem_cached", "VAL": "939068", "TMAX": "180", "TN": "17", "SOURCE": "gmond", "UNITS": "KB", "DMAX": "0", "EXTRA_DATA": [{"EXTRA_ELEMENT": [{"NAME": "GROUP", "VAL": "memory"}, {"NAME": "DESC", "VAL": "Amount of cached memory"}, {"NAME": "TITLE", "VAL": "Cached Memory"}]}], "TYPE": "float"}, {"SLOPE": "both", "NAME": "pkts_in", "VAL": "0.32", "TMAX": "300", "TN": "180", "SOURCE": "gmond", "UNITS": "packets/sec", "DMAX": "0", "EXTRA_DATA": [{"EXTRA_ELEMENT": [{"NAME": "GROUP", "VAL": "network"}, {"NAME": "DESC", "VAL": "Packets in per second"}, {"NAME": "TITLE", "VAL": "Packets Received"}]}], "TYPE": "float"}, {"SLOPE": "both", "NAME": "bytes_in", "VAL": "40.97", "TMAX": "300", "TN": "180", "SOURCE": "gmond", "UNITS": "bytes/sec", "DMAX": "0", "EXTRA_DATA": [{"EXTRA_ELEMENT": [{"NAME": "GROUP", "VAL": "network"}, {"NAME": "DESC", "VAL": "Number of bytes in per second"}, {"NAME": "TITLE", "VAL": "Bytes Received"}]}], "TYPE": "float"}, {"SLOPE": "both", "NAME": "bytes_out", "VAL": "39.39", "TMAX": "300", "TN": "180", "SOURCE": "gmond", "UNITS": "bytes/sec", "DMAX": "0", "EXTRA_DATA": [{"EXTRA_ELEMENT": [{"NAME": "GROUP", "VAL": "network"}, {"NAME": "DESC", "VAL": "Number of bytes out per second"}, {"NAME": "TITLE", "VAL": "Bytes Sent"}]}], "TYPE": "float"}, {"SLOPE": "zero", "NAME": "swap_total", "VAL": "0", "TMAX": "1200", "TN": "58", "SOURCE": "gmond", "UNITS": "KB", "DMAX": "0", "EXTRA_DATA": [{"EXTRA_ELEMENT": [{"NAME": "GROUP", "VAL": "memory"}, {"NAME": "DESC", "VAL": "Total amount of swap space displayed in KBs"}, {"NAME": "TITLE", "VAL": "Swap Space Total"}]}], "TYPE": "float"}, {"SLOPE": "both", "NAME": "mem_free", "VAL": "1551680", "TMAX": "180", "TN": "17", "SOURCE": "gmond", "UNITS": "KB", "DMAX": "0", "EXTRA_DATA": [{"EXTRA_ELEMENT": [{"NAME": "GROUP", "VAL": "memory"}, {"NAME": "DESC", "VAL": "Amount of available memory"}, {"NAME": "TITLE", "VAL": "Free Memory"}]}], "TYPE": "float"}, {"SLOPE": "both", "NAME": "load_fifteen", "VAL": "0.05", "TMAX": "950", "TN": "29", "SOURCE": "gmond", "UNITS": " ", "DMAX": "0", "EXTRA_DATA": [{"EXTRA_ELEMENT": [{"NAME": "GROUP", "VAL": "load"}, {"NAME": "DESC", "VAL": "Fifteen minute load average"}, {"NAME": "TITLE", "VAL": "Fifteen Minute Load Average"}]}], "TYPE": "float"}, {"SLOPE": "zero", "NAME": "os_name", "VAL": "Linux", "TMAX": "1200", "TN": "58", "SOURCE": "gmond", "UNITS": "", "DMAX": "0", "EXTRA_DATA": [{"EXTRA_ELEMENT": [{"NAME": "GROUP", "VAL": "system"}, {"NAME": "DESC", "VAL": "Operating system name"}, {"NAME": "TITLE", "VAL": "Operating System"}]}], "TYPE": "string"}, {"SLOPE": "zero", "NAME": "boottime", "VAL": "1465696757", "TMAX": "1200", "TN": "58", "SOURCE": "gmond", "UNITS": "s", "DMAX": "0", "EXTRA_DATA": [{"EXTRA_ELEMENT": [{"NAME": "GROUP", "VAL": "system"}, {"NAME": "DESC", "VAL": "The last time that the system was started"}, {"NAME": "TITLE", "VAL": "Last Boot Time"}]}], "TYPE": "uint32"}, {"SLOPE": "both", "NAME": "cpu_idle", "VAL": "96.9", "TMAX": "90", "TN": "34", "SOURCE": "gmond", "UNITS": "%", "DMAX": "0", "EXTRA_DATA": [{"EXTRA_ELEMENT": [{"NAME": "GROUP", "VAL": "cpu"}, {"NAME": "DESC", "VAL": "Percentage of time that the CPU or CPUs were idle and the system did not have an outstanding disk I/O request"}, {"NAME": "TITLE", "VAL": "CPU Idle"}]}], "TYPE": "float"}, {"SLOPE": "both", "NAME": "cpu_user", "VAL": "2.3", "TMAX": "90", "TN": "34", "SOURCE": "gmond", "UNITS": "%", "DMAX": "0", "EXTRA_DATA": [{"EXTRA_ELEMENT": [{"NAME": "GROUP", "VAL": "cpu"}, {"NAME": "DESC", "VAL": "Percentage of CPU utilization that occurred while executing at the user level"}, {"NAME": "TITLE", "VAL": "CPU User"}]}], "TYPE": "float"}, {"SLOPE": "both", "NAME": "cpu_nice", "VAL": "0.0", "TMAX": "90", "TN": "34", "SOURCE": "gmond", "UNITS": "%", "DMAX": "0", "EXTRA_DATA": [{"EXTRA_ELEMENT": [{"NAME": "GROUP", "VAL": "cpu"}, {"NAME": "DESC", "VAL": "Percentage of CPU utilization that occurred while executing at the user level with nice priority"}, {"NAME": "TITLE", "VAL": "CPU Nice"}]}], "TYPE": "float"}, {"SLOPE": "both", "NAME": "cpu_aidle", "VAL": "99.5", "TMAX": "3800", "TN": "34", "SOURCE": "gmond", "UNITS": "%", "DMAX": "0", "EXTRA_DATA": [{"EXTRA_ELEMENT": [{"NAME": "GROUP", "VAL": "cpu"}, {"NAME": "DESC", "VAL": "Percent of time since boot idle CPU"}, {"NAME": "TITLE", "VAL": "CPU aidle"}]}], "TYPE": "float"}]}], "LATLONG": "N30.47 E103.53", "OWNER": "serveradmin", "LOCALTIME": "1465817120"}]}}

    parser = argparse.ArgumentParser()
    note = 'Specify the xmpp account for the sinker process which is used to receive data from other clients.'
    parser.add_argument('--account', nargs='?', default='sinker@cicbd.jabber.org', help=note)
    note = 'Specify the address of mongodb database.'
    parser.add_argument('--mongodb', nargs='?', default='localhost:27017', help=note)
    note = "If you want to print data received to stdout, set the debug=1."
    parser.add_argument('--debug', nargs='?', type=int, default=0, help=note)

    args = parser.parse_args()

    datasinker = DataSinker(args.account)
    dbhost = args.mongodb.split(':')[0]
    dbport = int(args.mongodb.split(':')[1])
    dbsaver = MongoDBSaver(dbhost, dbport)
    datasinker.register_handler(dbsaver.msg_saver)

    transmitter = Transmitter(args.debug == 1)
    datasinker.register_handler(transmitter.flush_msg)
    transmitter.start()

    datasinker.start()

    # dbsaver = MongoDBSaver(args.dbhost, args.dbport)
    # output = GmondDataAdaptor(gmonddata)
    # dbsaver.save(output)
    # print output['metriclist']
    # print output['hostdesclist']
    # print output['metricdesclist']
