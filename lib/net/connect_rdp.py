import socket
from lib.code.binaryConversion import bytesToHexString,hexStringTobytes

def connect_rdp(host,port=None,user=None,password=None):
    if port == None:
        port = 3389
    if user == None :
        user = 'administrator'
    if password == None:
        password = '123456'


# connect the sockets and return the received data plus the connection in a Tuple
def socket_connection(obj, address, port=None, receive_size=4000):
    if port == None:
        port = 3389
    try:
        session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        session.connect((address, port))
        session.sendall(obj)
        return session.recv(receive_size), session
    except Exception as e:
        print(e)
        return None


# check if the ip is running RDP or not
def check_rdp_service(address,port=None):
    if port == None:
        port = 3389
    rdp_correlation_packet = hexStringTobytes("436f6f6b69653a206d737473686173683d75736572300d0a010008000100000000")
    test_packet = hexStringTobytes('030000130ee000000000000100080003000000')
    send_packet = test_packet + rdp_correlation_packet
    results = socket_connection(send_packet, address, receive_size=9126,port=port)
    print(results)
    if results is not None:
        if results[0]:
            print("successfully connected to RDP service on host: {}:{}".format(address,port))
            return "{}:{}".format(address,port)
        else:
            print("unknown response provided from RDP session")
    else:
        print("unable to connect")



rdp_correlation_packet = hexStringTobytes("436f6f6b69653a206d737473686173683d75736572300d0a010008000100000000")
test_packet = hexStringTobytes('030000130ee000000000000100080003000000')
send_packet = test_packet + rdp_correlation_packet
#
print(send_packet)
print(hexStringTobytes('030000130ee000000000000100080003000000436f6f6b69653a206d737473686173683d75736572300d0a010008000100000000'))
check_rdp_service('172.16.11.197')