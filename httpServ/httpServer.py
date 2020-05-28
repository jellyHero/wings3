import json
from urllib.parse import parse_qs

from  http.server import HTTPServer,BaseHTTPRequestHandler

class HTTP_Serv(BaseHTTPRequestHandler):
    # url参数转换成字典
    # 'DB_name=zaobao&mission_name=12&ip_24='
    # >
    # {'DB_name': 'zaobao', 'mission_name': '12'}
    def url2dict(self, post_data):
        # print(dict([(k, v[0].strip()) for k, v in parse_qs(post_data).items()]))
        return dict([(k, v[0].strip()) for k, v in parse_qs(post_data).items()])

    #返回json格式的数据
    def do_respnose_json(self,json_data):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(json_data).encode())

    #返回html格式的页面
    def do_respnose_html(self, byte_data):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        # self.send_header('Content-Length', str(len(byte_data)))
        self.end_headers()
        self.wfile.write(byte_data)

    #响应get请求
    def do_GET(self):
        self.webName = str(self.path.replace('://','').split('/')[1])
        htmlStr = 'Please POST to API'.encode('utf-8')
        self.do_respnose_html(htmlStr)

    #响应post请求，对应api接口http_api
    def do_POST(self):
        self.webName = str(self.path.replace('://','').split('/')[1])
        try:
            post_data = self.rfile.peek().decode()
            if self.webName == 'portScan':
                return self.do_respnose_json({'result':'port scan'})
            else:
                return self.do_respnose_json({'result': 'no this API'})
        except Exception as e:
            pass
            return self.do_respnose_json({'result': e})


def start_server(port):
    http_server = HTTPServer(('', int(port)),HTTP_Serv)
    http_server.serve_forever()


if __name__ == "__main__":
    start_server(3333)