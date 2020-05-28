import pymysql

def connect_mysql(host,port=None,user=None,password=None,database=None):
    if port == None:
        port = 3306
    if password == None:
        password = ''
    if database==None:
        database = 'mysql'

    try:
        conn = pymysql.connect(host=host,user=user,password=password,port=port,database=database,connect_timeout=5)
        # cur = conn.cursor(cursor=pymysql.cursors.DictCursor)
        # cur.execute('select user,host from user')
        # ret1 = cur.fetchone()
        # print(ret1)
        # cur.close()
        conn.close()
        return (True,{'user':user,'password':password})
    except Exception as e:
        print(e)
        return (False,None)