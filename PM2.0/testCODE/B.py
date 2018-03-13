# from A import Aclass
# class Bclass(object):
#     def __init__(self):
#         print("IN B class Init.")
#
#     def run(self):
#
#         obj = Aclass()
#         obj.run()

import socket,traceback,time,threading
# sockets = []
# for i in range(5):
#     try:
#         client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#         client.connect(("192.168.2.101",20108))
#         sockets.append(client)
#     except Exception,e:
#         traceback.print_exc()
#         print(client,"connect fail[{}]".format(i))
#         continue
def getdata(n):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("192.168.2.109", 20108))
    # client.setblocking(False)
    print "Server: ", client.getpeername(), "Client{}: ".format(n), client.getsockname(),"\n"
    while 1:
        t1 = time.time()
        try:
            datas = client.recv(102)
        except socket.error, e:
            if (str(e).find("10035") != -1):
                print "Client{}: ".format(n),"get nodatas."
            time.sleep(1)
            continue
        print "[Client{}: ".format(n),"len=", len(datas),"] \r\n"#"time spend: ",time.time() - t1,



if  __name__ == "__main__":
    # client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # client.connect(("192.168.2.101",20108))
    # print "Server: ",client.getpeername(),"Client0: ",client.getsockname(),"\r\n"
    # client.setblocking(True)

    for i in range(5):
        # thread_socketRead = threading.Thread(target=getdata,args={i})
        thread_socketRead = threading.Timer(i,getdata, args={i})
        thread_socketRead.setDaemon(True)
        thread_socketRead.start()


    while True:
        time.sleep(5)

        # t1 = time.time()
        # try:
        #     #print "client0 enter recv................"
        #     datas = client.recv(102)
        #     #print "client0 out recv................"
        # except socket.error,e:
        #     if (str(e).find("10035") != -1):
        #         print "get nodatas."
        #     else:
        #         print e
        #     continue
        # print "Client0: ",  "time spend: ", time.time() - t1, "len=", len(datas),"\r\n"
        #

