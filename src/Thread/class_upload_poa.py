# -*- coding: utf-8 -*-
import threading
import time
import wx
from src.Package.package import *
from src.Spectrum import Spectrum_1
import struct
from src.CommonUse.staticVar import staticVar
from src.CommonUse.staticFileUpMode import staticFileUp
import socket
import os
import cPickle as pickle

from src.Package.logg import Log
class SendPoaFile():
    def __init__(self):


        self.FILE_PATH=os.getcwd()+"\\LocalData\\Poa\\"
        self.indexOfNameList=0
        self.nameListPoa=[]



    def send_poa_data(self):
        if (self.nameListPoa == []):
            self.nameListPoa = os.listdir(self.FILE_PATH)

            if (len(self.nameListPoa) >= 500):
                self.upload()
            else:
                self.nameListPoa = []

        else:
            self.upload()

    def upload(self):

        if (self.indexOfNameList == len(self.nameListPoa)):
           
            self.indexOfNameList = 0
            self.nameListPoa = []


        else:
            # 传输文件

            fileName = self.nameListPoa[self.indexOfNameList]
            self.indexOfNameList += 1
            if(os.path.isfile(self.FILE_PATH+fileName)):
                    
                fid = open(".\LocalData\\Poa\\" + fileName, 'rb')
                d = pickle.load(fid)
                fid.close()

                LonLat= d['LonLat']
                count_ab= d['count_ab']
                list_for_ab=d['list_for_ab']


                fileNameLen=len(fileName)
                fileContentLen=sizeof(LonLat)+5*count_ab+3

                sockFile = staticVar.getSockFile()
                if(not sockFile==0):
                    try:
                        str1=struct.pack("!2BHQ",0x00,0xFF,fileNameLen,fileContentLen)
                        sockFile.sendall(str1+fileName)
                        sockFile.sendall(struct.pack("!B", 0x00))
                        sockFile.sendall(bytearray(LonLat))
                        sockFile.sendall(struct.pack("!B",  count_ab))
                        sockFile.sendall(bytearray(list_for_ab))
                        sockFile.sendall(struct.pack("!B",0x00))

                        print fileName
                        os.remove(self.FILE_PATH + fileName)
                        Log.getLogger().debug("send_poa_file_ok:%s" % fileName)

                    except socket.error,e:
                        print 'socket error occur in send poa ',e
                        Log.getLogger().debug(" socket_error_found_in_send_poa_file: %s" % e)
                        Log.getLogger().debug(" Cur socket sockFile=: %s" % staticVar.sockFile)

                        staticVar.sockFile=0
























