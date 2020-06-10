# # #!/usr/bin/python
# # # -*- coding: utf-8 -*-
# # import os
# #
# #
# # add_str = ''
# # target_dir = './'
# # for fpathe,dirs,fs in os.walk(target_dir):
# #     for f in fs:
# #         FILE = os.path.join(fpathe,f)
# #         if 'php' == '{}{}{}'.format(FILE[-3],FILE[-2],FILE[-1]):
# #             with open(FILE, 'r') as original:
# #                 data = original.read()
# #             with open(FILE, 'w') as modified:
# #                 modified.write("{}\n".format(add_str) + data)
#
# import socket, thread, select
# import re
#
# __version__ = '0.1.0 Draft 1'
# BUFLEN = 8192
# VERSION = 'Python Proxy/'+__version__
# HTTPVER = 'HTTP/1.1'
#
# class ConnectionHandler:
#     def __init__(self, connection, address, timeout):
#         self.client = connection
#         self.client_buffer = ''
#         self.timeout = timeout
#         self.method, self.path, self.protocol = self.get_base_header()
#         self.host = self.get_host()
#         conf = AclConfig()
#         if conf.is_allow_hosts or conf.is_deny_hosts or conf.is_deny_images:
#             self.acl(conf)
#         if self.method=='CONNECT':
#             self.method_CONNECT()
#         elif self.method in ('OPTIONS', 'GET', 'HEAD', 'POST', 'PUT',
#                              'DELETE', 'TRACE'):
#             self.method_others()
#         print("[info] %s" % (self.host))
#         self.client.close()
#         self.target.close()
#
#     def acl(self, conf):
#         if not re.search(conf.allow_hosts, self.host):
#             quit("[deny_hosts1] " + self.host)
#         elif re.search(conf.deny_hosts, self.host):
#             quit("[deny_hosts2] " + self.host)
#         elif re.search(conf.deny_images, self.path):
#             quit("[deny_images] " + self.path)
#
#     def get_host(self):
#         i = self.path.find(':443')
#         if i != -1:
#             return self.path
#         path = self.path[7:]
#         i = path.find('/')
#         return path[:i]
#
#     def get_base_header(self):
#         while 1:
#             self.client_buffer += self.client.recv(BUFLEN)
#             end = self.client_buffer.find('\n')
#             if end!=-1:
#                 break
#         #print '%s'%self.client_buffer[:end]#debug
#         data = (self.client_buffer[:end+1]).split()
#         self.client_buffer = self.client_buffer[end+1:]
#         return data
#
#     def method_CONNECT(self):
#         self._connect_target(self.path)
#         self.client.send(HTTPVER+' 200 Connection established\n'+
#                          'Proxy-agent: %s\n\n'%VERSION)
#         self.client_buffer = ''
#         self._read_write()
#
#     def method_others(self):
#         i = self.path.find(':443')
#         if i != -1:
#             self.path = self.path[8:]
#         else:
#             self.path = self.path[7:]
#         i = self.path.find('/')
#         host = self.path[:i]
#         path = self.path[i:]
#         self._connect_target(host)
#         self.target.send('{} {} {}\n'.format(self.method, path, self.protocol)+self.client_buffer)
#         self.client_buffer = ''
#         self._read_write()
#
#     def _connect_target(self, host):
#         i = host.find(':')
#         if i!=-1:
#             port = int(host[i+1:])
#             host = host[:i]
#         else:
#             port = 80
#         try:
#             (soc_family, _, _, _, address) = socket.getaddrinfo(host, port)[0]
#         except:
#             print "[error _connect_target] " + host
#         self.target = socket.socket(soc_family)
#         self.target.connect(address)
#
#     def _read_write(self):
#         time_out_max = self.timeout/3
#         socs = [self.client, self.target]
#         count = 0
#         while 1:
#             count += 1
#             (recv, _, error) = select.select(socs, [], socs, 3)
#             if error:
#                 break
#             if recv:
#                 for in_ in recv:
#                     try:
#                         data = in_.recv(BUFLEN)
#                     except:
#                         print "[recv error] "+self.host
#                         exit(-1)
#                     if in_ is self.client:
#                         out = self.target
#                     else:
#                         out = self.client
#                     if data:
#                         out.send(data)
#                         count = 0
#             if count == time_out_max:
#                 break
#
# def quit(message=""):
#     if message != "":
#         print message
#     exit(0)
#
#
# def start_server(host='localhost', port=8080, IPv6=False, timeout=60,
#                   handler=ConnectionHandler):
#     if IPv6==True:
#         soc_type=socket.AF_INET6
#     else:
#         soc_type=socket.AF_INET
#     soc = socket.socket(soc_type)
#     soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     soc.bind((host, port))
#     print "Serving on %s:%d."%(host, port)#debug
#     soc.listen(0)
#     while 1:
#         try:
#             thread.start_new_thread(handler, soc.accept()+(timeout,))
#         except KeyboardInterrupt:
#             quit("[quit] KeyboardInterrupt.")
#     soc.close()
#
# class AclConfig:
#     port=8080
#     #allow_hosts = ("(php.net|python.org|github.com|akamai.net|gravatar.com|qiita.com|google.com|google.co.jp)")
#     allow_hosts = (".*")
#     deny_hosts = ("(youtube.com|goo.ne.jp)")
#     deny_images = ("\.(jpg|jpeg|gif|bmp|png|flv|swf)$")
#     #
#     # True: check acl. False:pass
#     #is_allow_hosts = True
#     #is_deny_hosts = True
#     #is_deny_images = True
#     is_allow_hosts = False
#     is_deny_hosts = False
#     is_deny_images = False
#     def __init__(self):
#         pass
#
# if __name__ == '__main__':
#     config = AclConfig()
#     port=config.port
#     try:
#         start_server(host='0.0.0.0', port=port)
#     except socket.error:
#         #print "[warn] port %d already used. trying use port %d" % (port, port+1)
#         #start_server(host='0.0.0.0', port=port+1)
#         quit("[quit] port %d already used." % port)