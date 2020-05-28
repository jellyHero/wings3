import svn.remote

def connect_svn(host,user,password=None):
    if password == None :
        password = ''
    try:
        r = svn.remote.RemoteClient('svn://{}'.format(host),username=user,password=password)
        info = r.info()
        return (True, {'user': user, 'password': password})
    except Exception as e:
        return (False, None)