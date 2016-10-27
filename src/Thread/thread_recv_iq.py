
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
import  math

class ReceiveIQThread(threading.Thread):
    def __init__(self,mainframe):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.event.set()
        
        ###########################
        self.byte_to_package=mainframe.byte_to_package
        self.mainframe=mainframe
       
        
        self.SweepRangeIQ=[]
        self.Fs=5e6
        ##########################
        if(not os.path.exists("./LocalData//IQ//")):
            os.makedirs('./LocalData//IQ//')
            
    
    def run(self):
        count=0
        while(count<100):
            try:
                recvIQ=self.byte_to_package.ReceiveIQ()
                if(not recvIQ==0):
                    self.SweepRangeIQ.append(recvIQ)
                    while(len(self.SweepRangeIQ)<self.SweepRangeIQ[0].Param.UploadNum):
                        recvIQ=self.byte_to_package.ReceiveIQ()
                        if(not recvIQ==0):
                            self.SweepRangeIQ.append(recvIQ)
                    break
            except usb.core.USBError,e:
                print e
                time.sleep(3)
                count+=1
        
        if(self.mainframe.WaveFrame==None):   #有IQ数据来时自动弹出WaveFrame
            self.mainframe.WaveFrame=WaveIQ(self.mainframe,u"定频波形图                ")  
            self.mainframe.WaveFrame.Activate()

        ########################## 加到队列 方便class_upload_iq 上传 ###################
        if (not self.mainframe.start_local_iq):  ##如果没有启动本地定频才是中心站发起的
            self.mainframe.queueIQUpload.put(self.SweepRangeIQ)
        else:
            self.mainframe.start_local_iq = 0

        self.SaveIQ()


                ### 循环画五次 ####
        for i in range(5):
            for recvIQ in self.SweepRangeIQ:
                if(isinstance(self.mainframe.WaveFrame,WaveIQ)):
                    Idata,Qdata=self.ParseIQ(recvIQ)
                    try:
                        self.mainframe.WaveFrame.Wave(Idata,'y')
                        self.mainframe.WaveFrame.Wave(Qdata, 'r')
                    except Exception,e:
                        self.mainframe.WaveFrame.Destroy()
                        self.mainframe.WaveFrame=None
                        del self.SweepRangeIQ
                        break
        
                        
        if(self.mainframe.WaveFrame):
            self.mainframe.WaveFrame.Destroy()
            self.mainframe.WaveFrame=None
            del self.SweepRangeIQ



        


                    
                                        
    def ParseIQ(self,recvIQ):
        
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


        max_I=[abs(i) for i in IDataSet]
        max_Q= [abs(i) for i in QDataSet]
        max_value = math.sqrt(max(max_I)**2+ max(max_Q)**2)
        Idata=[float(i)/max_value for i in IDataSet]
        Qdata=[float(i)/max_value for i in QDataSet]



        return Idata,Qdata
    
        

    def SaveIQ(self):
        self.IQList=[]
        recvIQList = self.SweepRangeIQ
        for recvIQ in recvIQList:
            block = IQBlock(recvIQ.CurBlockNo, recvIQ.IQDataAmp)
            self.IQList.append(block)

        head = IQUploadHeader(0x00, recvIQ.LonLatAlti, recvIQ.Param)

        #####组合IQ文件################

        Time=recvIQ.Time_
        # CommonHeader=recvIQ.CommonHeader
        # ID=(CommonHeader.HighDeviceID<<8)+CommonHeader.LowDeviceID
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
                   "-" + str(Second) + '-' + str(ID) +  '-'+\
                   str(self.mainframe.SpecFrame.iq_sequence)+ '.iq'

        print fileName

        ###########SaveToLocal####################
        fid=open(".\LocalData\\IQ\\"+ fileName,'wb+')
        # fid = open(self.dir_iq + fileName, 'wb+')
        fid.write(bytearray(head))
        for block in self.IQList:
            fid.write(bytearray(block))
        fid.write(struct.pack("!B", 0x00))
        fid.close()
        #########################################

        del self.IQList





