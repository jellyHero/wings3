import copy
import ssl
import socket
import zlib
import gzip
from http import client
from conf.conf import User_Agent
from urllib import parse
#代码复制自HackRequests，微改动
def extract_dict(text, sep, sep2="="):
    """根据分割方式将字符串分割为字典
    Args:
        text: 分割的文本
        sep: 分割的第一个字符 一般为'\n'
        sep2: 分割的第二个字符，默认为'='
    Return:
        返回一个dict类型，key为sep2的第0个位置，value为sep2的第一个位置

        只能将文本转换为字典，若text为其他类型则会出错
    """
    _dict = dict([l.split(sep2, 1) for l in text.split(sep)])
    return _dict


class httpcon(object):
    #httpcon用于生成HTTP中的连接。
    #Attributes:
        #timeout: 超时时间

    def __init__(self, timeout=10):
        self.timeout = timeout
        self.protocol = []
        self._get_protocol()

    def _get_protocol(self):
        if not self.protocol:
            ps = (
                'PROTOCOL_SSLv23', 'PROTOCOL_TLSv1',
                'PROTOCOL_SSLv2', 'PROTOCOL_TLSv1_1', 'PROTOCOL_TLSv1_2')
            for p in ps:
                pa = getattr(ssl, p, None)
                if pa:
                    self.protocol.append(pa)

    #得到一个连接
    #这是连接池中最重要的一个参数，连接生成、复用相关操作都在这

    def get_con(self, url, proxy=None):
        scheme, host, port, path = url
        conn = self._make_con(scheme, host, port, proxy)
        return conn

    def _make_con(self, scheme, host, port, proxy=None):
        if "https" != scheme.lower():
            if proxy:
                con = client.HTTPConnection(
                    proxy[0], int(proxy[1]), timeout=self.timeout)
                con.set_tunnel(host, port)
            else:
                con = client.HTTPConnection(host, port, timeout=self.timeout)
            # con.connect()
            return con
        for p in self.protocol:
            context = ssl._create_unverified_context(p)
            try:
                if proxy:
                    con = client.HTTPSConnection(
                        proxy[0], proxy[1], context=context,
                        timeout=self.timeout)
                    con.set_tunnel(host, port)
                else:
                    con = client.HTTPSConnection(
                        host, port, context=context, timeout=self.timeout)
                # con.connect()
                return con
            except ssl.SSLError:
                pass
        raise Exception('connect err')

class response(object):

    def __init__(self, rep, redirect, oldcookie=''):
        # print(rep.peek())
        self.rep = rep
        self.status_code = self.rep.status  # response code
        self.url = redirect
        self._content = ''
        self.body = self.content()

        _header_dict = dict()
        self.cookie = ""
        for k, v in self.rep.getheaders():
            _header_dict[k] = v
            # handle cookie
            if k == "Set-Cookie":
                if ";" in v:
                    self.cookie += v.strip().split(";")[0] + "; "
                else:
                    self.cookie = v.strip() + "; "

        if oldcookie:
            cookie_dict = self._cookie_update(oldcookie, self.cookie)
            self.cookie = ""
            for k, v in cookie_dict.items():
                self.cookie += "{}={}; ".format(k, v)
        self.cookie = self.cookie.rstrip("; ")
        try:
            self.cookies = extract_dict(self.cookie, "; ", "=")
        except:
            self.cookies = {}

        self.headers = _header_dict
        self.header = self.rep.msg  # response header
        charset = self.rep.msg.get('content-type', 'utf-8')
        try:
            self.charset = charset.split("charset=")[1]
        except:
            self.charset = "utf-8"

    def content(self):
        if self._content:
            return self._content
        encode = self.rep.msg.get('content-encoding', None)
        try:
            # print(self.rep.peek())
            body = self.rep.read()
        except socket.timeout:
            body = b''
        if encode == 'gzip':
            body = gzip.decompress(body)
        elif encode == 'deflate':
            try:
                body = zlib.decompress(body, -zlib.MAX_WBITS)
            except:
                body = zlib.decompress(body)
        # redirect = self.rep.msg.get('location', None)   # handle 301/302
        self._content = body
        return body

    def text(self):
        '''

        :return: text
        '''
        body = self.body

        try:
            text = body.decode(self.charset, 'ignore')
        except:
            text = str(body)
        return text

    def _cookie_update(self, old, new):
        '''
        用于更新旧cookie,与新cookie得出交集后返回新的cookie
        :param old:旧cookie
        :param new:新cookie
        :return:Str:新cookie
        '''
        # 先将旧cookie转换为字典，再将新cookie转换为字典时覆盖旧cookie
        old_sep = old.strip().split(";")
        new_sep = new.strip().split(";")
        cookie_dict = {}
        for sep in old_sep:
            if sep == "":
                continue
            try:
                k, v = sep.split("=")
                cookie_dict[k.strip()] = v
            except:
                continue
        for sep in new_sep:
            if sep == "":
                continue
            try:
                k, v = sep.split("=")
                cookie_dict[k.strip()] = v
            except:
                continue
        return cookie_dict

def _send_output(oldfun, con):
    def _send_output_hook(*args, **kwargs):
        oldfun(*args, **kwargs)
        con._send_output = oldfun
    return _send_output_hook

#http req raw: core
def httpreq_raw(method,scheme,host,port=None,path=None,headers=None,body=None,proxy=None):
    if port == None:
        port = 80
    if path == None:
        path = '/'
    if headers == None:
        headers['Host'] = host
        headers['User-Agent'] = User_Agent
    else:
        if 'Host' not in headers.keys():
            headers['Host'] = host
        if 'User-Agent' not in headers.keys():
            headers['User-Agent'] = User_Agent

    urlinfo = (scheme, host, port, path)
    _url = None
    rep= None

    conn = httpcon().get_con(urlinfo,proxy=proxy)
    conn._send_output = _send_output(conn._send_output, conn)
    try:
        conn.putrequest(method, path, skip_host=True, skip_accept_encoding=True)
        for k, v in headers.items():
            conn.putheader(k, v)
        if body and "Content-Length" not in headers and "Transfer-Encoding" not in headers:
            length = conn._get_content_length(body, method)
            conn.putheader("Content-Length", length)
        conn.endheaders()
        if body:
            if headers.get("Transfer-Encoding", '').lower() == "chunked":
                body = body.replace('\r\n', '\n')
                body = body.replace('\n', '\r\n')
                body = body + "\r\n" * 2
            conn.send(body.encode('utf-8'))
        rep = conn.getresponse()
        if port == 80 or port == 443:
            _url = "{scheme}://{host}{path}".format(scheme=scheme, host=host, path=path)
        else:
            _url = "{scheme}://{host}{path}".format(scheme=scheme, host=host + ":" + port, path=path)
        return response(rep=rep, redirect=_url)
    except socket.timeout:
        print("socket connect timeout")
    except socket.gaierror:
        print("socket don't get hostname")
    except KeyboardInterrupt:
        print("user exit")
    finally:
        conn.close()

#http req: 可以填写下列参数，当然，除了url参数外都不是必须的
#url（必须）	用于传递一个地址	Str
#post	post参数用于传递post提交，此参数被选择时，method自动变为POST,post参数的类型可以为Str或者Dict	Str/Dict
#method	访问模式，目前支持三种 HEAD、GET、POST，默认为GET	Str
#location	当状态码为301、302时会自动跳转，默认为True	Bool
#proxy	代理，需要传入一个tuple，类似 ('127.0.0.1','8080')	Tuple
#headers	自定义HTTP头，可传入字典或原始的请求头	Str/Dict
#cookie	自定义Cookie，可传入字典或原始cookie字符串	Str/Dict
#referer	模拟用户Referer	Str
#user_agent	用户请求头，若为空则会模拟一个正常的请求头	Str
#
#real_host	用于host头注入中在header host字段填写注入语句，这里填写真实地址 如 "127.0.0.1:8000"
# 具体参考：https://github.com/boy-hack/hack-requests/blob/master/demo/CVE-2016-10033.py	str
def httpreq(url, **kwargs):
    method = kwargs.get("method", "GET")
    post = kwargs.get("post", None) or kwargs.get("data", None)
    location = kwargs.get('location', True)
    locationcount = kwargs.get("locationcount", 0)

    proxy = kwargs.get('proxy', None)
    headers = kwargs.get('headers', {})

    # real host:ip
    real_host = kwargs.get("real_host", None)

    if isinstance(headers, str):
        headers = extract_dict(headers.strip(), '\n', ': ')
    cookie = kwargs.get("cookie", None)
    if cookie:
        cookiestr = cookie
        if isinstance(cookie, dict):
            cookiestr = ""
            for k, v in cookie.items():
                cookiestr += "{}={}; ".format(k, v)
            cookiestr = cookiestr.strip("; ")
        headers["Cookie"] = cookiestr
    for arg_key, h in [
        ('referer', 'Referer'),
        ('user_agent', 'User-Agent'), ]:
        if kwargs.get(arg_key):
            headers[h] = kwargs.get(arg_key)
    if "Content-Length" in headers:
        del headers["Content-Length"]


    def _get_urlinfo(url, realhost: str):
        p = parse.urlparse(url)
        scheme = p.scheme.lower()
        if scheme != "http" and scheme != "https":
            raise Exception("http/https only")
        hostname = p.netloc
        port = 80 if scheme == "http" else 443
        if ":" in hostname:
            hostname, port = hostname.split(":")
        path = ""
        if p.path:
            path = p.path
            if p.query:
                path = path + "?" + p.query
        if realhost:
            if ":" not in realhost:
                realhost = realhost + ":80"
            hostname, port = realhost.split(":")
        return scheme, hostname, int(port), path
    urlinfo = scheme, host, port, path = _get_urlinfo(url, real_host)
    try:
        conn = httpcon().get_con(urlinfo, proxy=proxy)
    except:
        raise
    conn._send_output = _send_output(conn._send_output, conn)
    tmp_headers = copy.deepcopy(headers)
    if post:
        method = "POST"
        if isinstance(post, str):
            try:
                post = extract_dict(post, sep="&")
            except:
                pass
        try:
            post = parse.urlencode(post)
        except:
            pass
        tmp_headers["Content-Type"] = kwargs.get(
            "Content-type", "application/x-www-form-urlencoded")
        tmp_headers["Accept"] = tmp_headers.get("Accept", "*/*")
    tmp_headers['Accept-Encoding'] = tmp_headers.get("Accept-Encoding", "gzip, deflate")
    tmp_headers['Connection'] = 'close'
    tmp_headers['User-Agent'] = tmp_headers['User-Agent'] if tmp_headers.get('User-Agent') else User_Agent
    rep = None
    try:
        conn.request(method, path, post, tmp_headers)
        rep = conn.getresponse()
        # body = rep.read()
    except socket.timeout:
        print("socket connect timeout")
    except socket.gaierror:
        print("socket don't get hostname")
    except KeyboardInterrupt:
        print("user exit")
    finally:
        conn.close()

    redirect = rep.msg.get('location', None)  # handle 301/302
    if redirect and location and locationcount < 10:
        if not redirect.startswith('http'):
            redirect = parse.urljoin(url, redirect)
        return httpreq(redirect, post=None, method=method, headers=tmp_headers, location=True,
                         locationcount=locationcount + 1)

    if not redirect:
        redirect = url
    return response(rep=rep, redirect=redirect,oldcookie=cookie)


# if __name__ == '__main__':
#     method = 'GET'
#     scheme,host = 'http', '10.178.31.61'
#     port = 80
#     path = '/dvwa/vulnerabilities/xss_r/?name=123'
#     headers =  {'Cookie':'security=low; PHPSESSID=ol5ao8q989b8ajs9inu1bnosv5'}
#     body = None
#
#     hh = httpreq_raw(method,scheme,host,port,path,headers=headers,body=body)
#     # print(hh.text(),hh.status_code,hh.headers)
#     text = hh.text()
#     print(text)

    # url = "http://10.178.31.61/dvwa/vulnerabilities/xss_r/?name=123"
    # u = httpreq(url, method="GET")
    # print(u.text())

