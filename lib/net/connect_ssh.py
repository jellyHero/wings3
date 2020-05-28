import paramiko

def connect_ssh(host,user,port=None,password=None):
    if 'port' == None:
        port = 22
    if password== None:
        password = ''

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(host,port,user,password,timeout=5)
        # stdin, stdout, stderr = ssh.exec_command('pwd')
        # result = stdout.read().decode()
        # print(result)
        return (True, {'user': user, 'password': password})
    except Exception as e:
        print(e)
        return (False, None)
    finally:
        ssh.close()

def cmd_ssh(ip,username,password=None,port=None,cmd=None):
    if port == None:
        port = 22
    if cmd == None:
        cmd = 'whoami'
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip,port,username,password,timeout=5)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        #stdin.write("Y")   #简单交互，输入 ‘Y’
        out = stdout.readlines()
        return (True, out)
    except Exception as e:
        print(e)
        return (False, None)
    finally:
        ssh.close()

#将ssh证书写入远程ip
def writeRsa_ssh(ip,username,password=None,port=None):
    if port == None:
        port = 22
    ida = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCc/CqnaXgUILsTcqr1EMDf8RS+NWH90XCKf/C3sHJCkBjVLY+fIuCfTB4QzANui9+wxyop9YPp5R1AlzkmfRtmhK8FA7rJO7vOC6qf01OiJ9Et/P6dOVR2pha9eRKGFXDIdaeK8u7x7deuOdzuXCnuQz0qppo3A1rpwjFDIykYO8PMqShCLRNZGI5JmL1heyx6WU722SpS5Jx5rbCwFT1KbVyhR2pLt6TDBL75hkSPqSBoSXJz+u2/kqped7y3kwKD1MyI++AAoXkPkFy5xdEOykQEshg5cUdnWF54ztciLr2FeM1f3LD7YR0RZnteAeUeSlB/sbmWU0L0VsVLlScL admin'
    cmd = 'chmod 700 ~/.ssh && echo "{}" >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys'.format(ida)
    # print(cmd)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip,port,username,password,timeout=5)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        #stdin.write("Y")   #简单交互，输入 ‘Y’
        out = stdout.readlines()
        return (True, out)
    except :
        return (False, None)
    finally:
        ssh.close()