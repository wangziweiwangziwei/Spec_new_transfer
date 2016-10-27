
# -*- coding: utf-8 -*-


from src.Package.package import *
import struct
import time
import os
from src.CommonUse.staticVar import staticVar
import cPickle as pickle
import socket
from src.Package.logg import Log
class SendTdoaFile():
    def __init__(self):

        self.FILE_PATH=os.getcwd()+"\\LocalData\\Tdoa\\"
        self.indexOfNameList=0
        self.nameListTdoa=[]






    def upload_tdoa(self):
        if(self.nameListTdoa==[]):
            self.nameListTdoa=os.listdir(self.FILE_PATH)

            if(len(self.nameListTdoa)>=500):
                self.upload()
            else:
                self.nameListTdoa=[]


        else:
            self.upload()

    def upload(self):
        #数到了最后

        if(self.indexOfNameList==len(self.nameListTdoa)):
            self.indexOfNameList=0
            self.nameListTdoa=[]


        else:
            # 传输文件

            fileName=self.nameListTdoa[self.indexOfNameList]
            self.indexOfNameList+=1
            if(os.path.isfile(self.FILE_PATH+fileName)):
                fid = open(".\LocalData\\Tdoa\\" + fileName, 'rb')
                d=pickle.load(fid)
                fid.close()

                head=d['head']
                block=d['block']

                fileNameLen = len(fileName)
                fileContentLen = sizeof(head) + sizeof(block) + 1




                ###########SendToServer###################(H :2字节  Q:8 字节)
                if(not staticVar.getSockFile()==0):
                    try:
                        sockFile = staticVar.getSockFile()
                        str1 = struct.pack("!2BHQ", 0x00, 0xFF, fileNameLen, fileContentLen)
                        sockFile.sendall(str1 + fileName)

                        sockFile.sendall(bytearray(head))

                        sockFile.sendall(bytearray(block))
                        sockFile.sendall(struct.pack("!B", 0x00))

                        print fileName
                        os.remove(self.FILE_PATH + fileName)
                        Log.getLogger().debug("send_tdoa_file_ok:%s"% fileName)
                    except socket.error, e:
                        Log.getLogger().debug(" socket_error_found_in_send_tdoa_file: %s" % e)
                        Log.getLogger().debug(" Cur socket sockFile=: %s" % staticVar.sockFile)

                        print 'socket error occur in send tdoa ', e
                        staticVar.sockFile = 0












