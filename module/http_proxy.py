import socket
import ssl
import re
from  http.server import HTTPServer,BaseHTTPRequestHandler

class Http_proxy(BaseHTTPRequestHandler):
    def __init__(self,address):
        self.client = address

    def req(self):
        if isinstance(self.request, ssl.SSLSocket):
            self.protocol = 'https://'
        else:
            self.protocol = 'http://'
        self.method = self.command
        self.host = self.headers['host'].strip()
        if self.method=='CONNECT':
            self.method_CONNECT()
        elif self.method in ('OPTIONS', 'GET', 'HEAD', 'POST', 'PUT',
                             'DELETE', 'TRACE'):
            self.method_others()
        print("[info] %s" % (self.host))

    def method_CONNECT(self):
        self._connect_target(self.host)
        self.client.send('HTTP/1.1 200 Connection established')
        self.client_buffer = ''
        self._read_write()

    def method_others(self):
        pass

    def _connect_target(self, host):
        i = host.find(':')
        if i!=-1:
            port = int(host[i+1:])
            host = host[:i]
        else:
            port = 80
        try:
            (soc_family, _, _, _, address) = socket.getaddrinfo(host, port)[0]
            self.target = socket.socket(soc_family)
            self.target.connect(address)
        except:
            print("[error _connect_target] " + host)

