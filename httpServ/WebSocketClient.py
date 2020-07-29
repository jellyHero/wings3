#-*- coding: utf-8 -*-
import websocket
from websocket import create_connection

class WebSocketClient:
    def __init__(self,url,http_proxy_host=None,http_proxy_port=None):
        self.url = url
        if http_proxy_host:
            self.ws = websocket.WebSocket()
            self.ws.connect(self.url, http_proxy_host=http_proxy_host, http_proxy_port=http_proxy_port)
        else:
            self.ws= create_connection(self.url)

    def send(self,msg):
        self.ws.send(msg)
        result = self.ws.recv()
        return result

    def close(self):
        self.ws.close()


test = WebSocketClient('ws://127.0.0.1:1234')
result = test.send('admin:123456')
print(result)
while True:
    msg = input('>')
    print(test.send(msg))