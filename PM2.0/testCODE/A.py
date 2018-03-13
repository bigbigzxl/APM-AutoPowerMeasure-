
# from B import Bclass
#
# class Aclass(object):
#     def __init__(self):
#         print("IN A class Init.")
#
#
#     def run(self):
#
#         obj = Bclass()
#         obj.run()

#ob = Aclass()
#ob.run()

import socket

HOST = "127.0.0.1"#"172.16.31.75"
PORT = 8008
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(5)
print "server start @:%s:%s"%(HOST,PORT)
print "wait for connection...."
while True:
    conn,addr = s.accept()
    print "connected by",addr
    while True:
        data = conn.recv(1024)
        print "received data:",data
        conn.send("server received your message.")
        #conn.close()