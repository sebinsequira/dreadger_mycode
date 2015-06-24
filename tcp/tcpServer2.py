import socket
import time

TIMEOUT = 10
HOST = ''              
PORT = 5000             


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#s.settimeout(TIMEOUT)
s.bind((HOST, PORT))
s.listen(1)

while 1:
    try:
        conn, addr = s.accept()         # Blocking statement, waits for a connection

        
        while 1:
            try:
                conn.send('ACK_FROM_SERVER')          #Dummy send to make sure that connection is correct
                data = conn.recv(1024)
                if data:
                    print 'Client: '+ data
                    conn.send(data.upper())
            except Exception as e:
                print e
                break                   # Break and wait for new conn, if dummy send fails

    except socket.timeout:
        print "Timeout!!\nConnection lost. Listening for a new controller."
        