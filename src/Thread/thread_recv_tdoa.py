
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
import math
import cPickle as pickle

from numpy import  cos,sin,pi
class ReceiveTdoaThread(threading.Thread):
    def __init__(self,mainframe):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.event.set()

        ###########################
        self.byte_to_package=mainframe.byte_to_package
        self.mainframe=mainframe
      



        # self.SweepRangeTdoa=[]
        self.Fs=5e6
        ##########################
        self.draw_intv=0
    def stop(self):
        self.event.clear()

    def run(self):
       
        while(1):
            try:
                self.event.wait()
              
                recvIQ=self.byte_to_package.ReceiveTdoa()
                if(not recvIQ==0):
                    # self.queueTdoa.put(recvIQ)
                    self.SaveIQ(recvIQ)
                #    self.DrawIQ(recvIQ) #会卡，所以还是关了
           

            except usb.core.USBError,e:
                print "  TDOA NO DATA"
                time.sleep(1)
                 

    def DrawIQ(self,recvIQ):
        self.draw_intv+=1
        
        
        if (self.mainframe.WaveFrame == None):  # 有IQ数据来时自动弹出WaveFrame
            self.mainframe.WaveFrame = WaveIQ(self.mainframe, u"TDOA波形图                ")
            self.mainframe.WaveFrame.Activate()

        if(self.draw_intv==5):
            self.draw_intv=0
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

            max_I = [abs(i) for i in IDataSet]
            max_Q = [abs(i) for i in QDataSet]
            max_value = math.sqrt(max(max_I) ** 2 + max(max_Q) ** 2)
            Idata = [float(i) / max_value for i in IDataSet]
            Qdata = [float(i) / max_value for i in QDataSet]
            try:
                if(len(IDataSet)==2000):
                    self.mainframe.WaveFrame.Wave(Idata,'y')
                    self.mainframe.WaveFrame.Wave(Qdata,'r')
            except Exception ,e:
                self.mainframe.WaveFrame=None
                print e

    def SaveIQ(self,recvIQ):


        block = IQBlock(recvIQ.CurBlockNo, recvIQ.IQDataAmp)


        head = IQUploadHeader(0x00, recvIQ.LonLatAlti, recvIQ.Param)

        #####组合tdoa 文件################

        count = (recvIQ.SecondCount[0] << 24) + \
                (recvIQ.SecondCount[1] << 16) + \
                (recvIQ.SecondCount[2] << 8) + \
                (recvIQ.SecondCount[3])


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


        list1=[str(Month),str(Day),str(Hour),str(Minute),str(Second)]
        for i in range(5):
            if(len(list1[i])==1):
                list1[i]='0'+list1[i]



        fileName = str(Year) + "-" + list1[0] + "-" + list1[1] + \
                   "-" + list1[2] + "-" + list1[3] +  \
                   "-" + list1[4] + '-' +str(count)+'-'+ str(ID) + \
                   '.tdoa'

        #print fileName

        ###########SaveToLocal####################
        fid=open(".\LocalData\\Tdoa\\"+ fileName,'wb')
        # fid = open(self.dir_iq + fileName, 'wb+')
        # fid.write(bytearray(head))
        #
        # fid.write(bytearray(block))
        # fid.write(struct.pack("!B", 0x00))
        d=dict(head=head,block=block)
        pickle.dump(d, fid)
        fid.close()
        #########################################








