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


class SendPoaFile():
    def __init__(self, queuePoa):


        self.queuePoa=queuePoa




        self.countPoa=0

        self.sockFile=staticVar.getSockFile()

    def send_poa_data(self):


        if(not self.queuePoa.empty()):
            list_poa=self.queuePoa.get()
            list_for_ab=[]

            count_ab=0

            for recvPoa in list_poa:
                for i in range(recvPoa.AbNum):
                    list_for_ab.extend(bytearray(recvPoa.AbBlock[i]))
                count_ab+=recvPoa.AbNum

            ###组合POA 文件 时间 ####

            Time=list_poa[0].Time
            CommonHeader=list_poa[0].CommonHeader
            ID=(CommonHeader.HighDeviceID<<8)+CommonHeader.LowDeviceID
            Year=(Time.HighYear<<4)+Time.LowYear
            Month=Time.Month
            Day=Time.Day
            Hour=(Time.HighHour<<2)+Time.LowHour+8
            Minute=Time.Minute
            Second=Time.Second

            if(not Year==2016):
                curTime=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
                Year=int(curTime[0:4])
                Month=int(curTime[4:6])
                Day=int(curTime[6:8])
                Hour=int(curTime[8:10])
                Minute=int(curTime[10:12])
                Second=int(curTime[12:14])

            ID=staticVar.getid()

            count=(list_poa[0].SecondCount[0]<<24)+ \
                  (list_poa[0].SecondCount[1] << 16) + \
                  (list_poa[0].SecondCount[2] << 8) + \
                  (list_poa[0].SecondCount[3])

            fileName=str(Year)+"-"+str(Month)+"-"+str(Day)+  \
                 "-"+str(Hour)+"-"+str(Minute)+"-"+str(Second)+\
                     "-"+str(count)+'-'+str(ID)+'.poa'


            ##### 经纬度 ############
            LonLat= list_poa[0].LonLatAlti

            fileNameLen=len(fileName)
            fileContentLen=sizeof(LonLat)+5*count_ab+3



            str1=struct.pack("!2BHQ",0x00,0xFF,fileNameLen,fileContentLen)
            self.sockFile.sendall(str1+fileName)
            self.sockFile.sendall(struct.pack("!B", 0x00))
            self.sockFile.sendall(bytearray(LonLat))
            self.sockFile.sendall(struct.pack("!B",  count_ab))
            self.sockFile.sendall(bytearray(list_for_ab))
            self.sockFile.sendall(struct.pack("!B",0x00))

            self.countPoa+=1
            if(self.countPoa%50==0):
                print fileName
                print 'self.countPoa',self.countPoa























