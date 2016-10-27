# -*- coding: utf-8 -*-
import socket 
class ServerCommunication():
    def __init__(self):
        self.sock=0
        self.sockFile=0
    def ConnectToServerMoni(self,ip,port):
        


        #sock.connect(('115.156.209.42',9123))
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,4096)
        sock.connect((ip, port))

        self.sock = sock
        # if(port==9000):    #####监控服务器#############

        # elif(port==9988):  ######文件服务器############
            #

    def ConnectToServerFile(self,ip,port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 1024*20)
        sock.connect((ip, port))

        self.sockFile=sock



    def SendQueryData(self,structrueObj):
        if(not self.sock==0):
            self.sock.send(bytearray(structrueObj))

    def DisconnectToServer(self):
        self.sock.close()
    def RecvConnectFlag(self):
        data =self.sock.recv(1024)
        return data
