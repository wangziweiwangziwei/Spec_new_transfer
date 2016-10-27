
# -*- coding: utf-8 -*-


from src.Package.package import *
import struct
import time

from src.CommonUse.staticVar import staticVar

class SendIQFile():
    def __init__(self,mainframe):
       self.queueIQUpload=mainframe.queueIQUpload
       self.mainframe=mainframe


    def upload_iq(self):

        self.IQList=[]
        recvIQList = self.queueIQUpload.get()
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

        fileNameLen = len(fileName)
        fileContentLen = sizeof(head) + sizeof(block) * len(self.IQList) + 1

        print fileName
        ###########SendToServer###################(H :2字节  Q:8 字节)

        sockFile=staticVar.getSockFile()
        str1 = struct.pack("!2BHQ", 0x00, 0xFF, fileNameLen, fileContentLen)
        sockFile.send(str1 + fileName)

        sockFile.send(bytearray(head))
        for block in self.IQList:
            sockFile.send(bytearray(block))
        sockFile.send(struct.pack("!B", 0x00))



        del self.IQList





