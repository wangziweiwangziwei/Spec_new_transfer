
# -*- coding: utf-8 -*-
import threading
import wx
from src.Package.package import *
import struct
import time
import Queue
import usb
import os
from src.Wave.IQWave import WaveIQ
from src.CommonUse.staticVar import staticVar
from numpy import  cos,sin,pi
class ReceiveTdoaThread(threading.Thread):
    def __init__(self,mainframe):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.event.set()

        ###########################
        self.byte_to_package=mainframe.byte_to_package
        self.mainframe=mainframe
        self.queueTdoa=mainframe.queueTdoa



        self.SweepRangeTdoa=[]
        self.Fs=5e6
        ##########################
        if(not os.path.exists("./LocalData//Tdoa//")):
            os.makedirs('./LocalData//Tdoa//')


    def stop(self):
        self.event.clear()

    def run(self):
        count=0
        while(count<100):
            try:
                recvIQ=self.byte_to_package.ReceiveTdoa()
                if(not recvIQ==0):
                    self.SweepRangeTdoa.append(recvIQ)
                while(1):
                    self.event.wait()
                    try:
                        recvIQ = self.byte_to_package.ReceiveTdoa()
                        if(not recvIQ==0):
                            self.SweepRangeTdoa.append(recvIQ)
                            if(recvIQ.CurBlockNo==recvIQ.Param.UploadNum):
                                if(len(self.SweepRangeTdoa)==recvIQ.CurBlockNo):
                                    if(self.queueTdoa._qsize()<16):
                                        self.queueTdoa.put(self.SweepRangeTdoa)
                                        self.SaveIQ()
                                        if(not self.mainframe.WaveFrame==None):
                                            self.DrawIQ(recvIQ)

                                self.SweepRangeTdoa=[]

                    except usb.core.USBError, e:
                        print e

            except usb.core.USBError,e:
                print e
                time.sleep(3)
                count+=1

    def DrawIQ(self,recvIQ):
        if (self.mainframe.WaveFrame == None):  # 有IQ数据来时自动弹出WaveFrame
            self.mainframe.WaveFrame = WaveIQ(self.mainframe, u"定频波形图                ")
            self.mainframe.WaveFrame.Activate()

        try:
            #chData=[]
            IDataSet=[]
            QDataSet=[]
            DataRate=recvIQ.Param.DataRate

            if(DataRate==0x01):self.Fs=5e6
            elif(DataRate==0x02): self.Fs=2.5e6
            elif(DataRate==0x03):self.Fs=1e6
            elif(DataRate==0x04):self.Fs=0.5e6
            elif(DataRate==0x05): self.Fs=0.1e6
            else:
                pass

            Fc=(recvIQ.Param.HighCentreFreqInteger << 6) + recvIQ.Param.LowCentreFreqInteger + \
                  float((recvIQ.Param.HighCentreFreqFraction << 8) +recvIQ.Param.LowCentreFreqFraction)/ 2 ** 10




            DataArray=recvIQ.IQDataAmp
            for i in range(len(DataArray)):
                HighIPath=DataArray[i].HighIPath
                HighQPath=DataArray[i].HighQPath
                LowIPath=DataArray[i].LowIPath
                LowQPath=DataArray[i].LowQPath
                if(HighIPath>=8):
                    IData=-(2**12-(HighIPath<<8)-LowIPath)
                else:
                    IData=((HighIPath<<8)+LowIPath)
                if(HighQPath>=8):
                    QData=-(2**12-(HighQPath<<8)-LowQPath)
                else:
                    QData=((HighQPath<<8)+LowQPath)

                IDataSet.append(IData)
                QDataSet.append(QData)

            data = []
            for i in range(len(IDataSet)):
                dataTmp = 2 * pi * Fc / self.Fs * i
                data.append(IDataSet[i]*cos(dataTmp)+QDataSet[i]*sin(dataTmp))

            self.mainframe.WaveFrame.Wave(self.Fs,data)
        except:
            self.mainframe.WaveFrame=None
            pass

    def SaveIQ(self):
        self.IQList=[]
        recvIQList = self.SweepRangeTdoa
        for recvIQ in recvIQList:
            block = IQBlock(recvIQ.CurBlockNo, recvIQ.IQDataAmp)
            self.IQList.append(block)

        head = IQUploadHeader(0x00, recvIQ.LonLatAlti, recvIQ.Param)

        #####组合tdoa 文件################

        count = (recvIQList[0].SecondCount[0] << 24) + \
                (recvIQList[0].SecondCount[1] << 16) + \
                (recvIQList[0].SecondCount[2] << 8) + \
                (recvIQList[0].SecondCount[3])


        Time=recvIQ.Time

        Year=(Time.HighYear<<4)+Time.LowYear
        Month=Time.Month
        Day=Time.Day
        Hour=(Time.HighHour<<2)+Time.LowHour+8
        Minute=Time.Minute
        Second=Time.Second
        ID = staticVar.getid()

        if(not Year==2016):
            curTime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
            Year = int(curTime[0:4])
            Month = int(curTime[4:6])
            Day = int(curTime[6:8])
            Hour = int(curTime[8:10])
            Minute = int(curTime[10:12])
            Second = int(curTime[12:14])
            

        fileName = str(Year) + "-" + str(Month) + "-" + str(Day) + \
                   "-" + str(Hour) + "-" + str(Minute) +  \
                   "-" + str(Second) + '-' +str(count)+'-'+ str(ID) +  '-'+\
                   '.tdoa'

        print fileName

        ###########SaveToLocal####################
        fid=open(".\LocalData\\Tdoa\\"+ fileName,'wb+')
        # fid = open(self.dir_iq + fileName, 'wb+')
        fid.write(bytearray(head))
        for block in self.IQList:
            fid.write(bytearray(block))
        fid.write(struct.pack("!B", 0x00))
        fid.close()
        #########################################
        del self.IQList







