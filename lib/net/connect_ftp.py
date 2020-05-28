from ftplib import FTP

def connect_ftp(host,port=None,user=None,password=None):
    if port == None:
        port = 21
    if user == None :
        user = 'anonymous'
    if password == None:
        password = ''

    try:
        ftp = FTP(host=host,timeout=5)
        ftp.port = port
        ftp.login(user=user,passwd=password)
        # ftp.dir()
        ftp.quit()
        return (True, {'user': user, 'password': password})
    except Exception as e:
        return (False, None)

# print(connect_ftp('10.1.11.34',user='cp_audit',password='cp_audit'))