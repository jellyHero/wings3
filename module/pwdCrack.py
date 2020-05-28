# -*- coding: utf-8 -*-

#根据用户名，生成一些包含用户名在内的弱口令
def getUserNameAlikePwd(user):
    return ['',user,'{}1'.format(user),'{}!'.format(user),'{}123'.format(user),'{}@123'.format(user),'{}!@#'.format(user),'{}123456'.format(user)]
