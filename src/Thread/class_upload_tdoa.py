
# -*- coding: utf-8 -*-


from src.Package.package import *
import struct
import time

from src.CommonUse.staticVar import staticVar

class SendTdoaFile():
    def __init__(self,mainframe):
        self.queueTdoa = mainframe.queueTdoa

        self.countTdoa=0

    def upload_tdoa(self):
        if(not self.queueTdoa.empty()):
            self.IQList = []
            recvIQList = self.queueTdoa.get()
            for recvIQ in recvIQList:
                block = IQBlock(recvIQ.CurBlockNo, recvIQ.IQDataAmp)
                self.IQList.append(block)

            head = IQUploadHeader(0x00, recvIQ.LonLatAlti, recvIQ.Param)

            #####组合tdoa 文件################

            count = (recvIQList[0].SecondCount[0] << 24) + \
                    (recvIQList[0].SecondCount[1] << 16) + \
                    (recvIQList[0].SecondCount[2] << 8) + \
                    (recvIQList[0].SecondCount[3])

            Time = recvIQ.Time

            Year = (Time.HighYear << 4) + Time.LowYear
            Month = Time.Month
            Day = Time.Day
            Hour = (Time.HighHour << 2) + Time.LowHour + 8
            Minute = Time.Minute
            Second = Time.Second
            ID = staticVar.getid()
            
            if (not Year == 2016):
                curTime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
                Year = int(curTime[0:4])
                Month = int(curTime[4:6])
                Day = int(curTime[6:8])
                Hour = int(curTime[8:10])
                Minute = int(curTime[10:12])
                Second = int(curTime[12:14])
                

            fileName = str(Year) + "-" + str(Month) + "-" + str(Day) + \
                       "-" + str(Hour) + "-" + str(Minute) + \
                       "-" + str(Second) + '-' + str(count) + '-' + str(ID) + '-' + \
                       '.tdoa'

            print fileName

            fileNameLen = len(fileName)
            fileContentLen = sizeof(head) + sizeof(block) * len(self.IQList) + 1

            print fileName
            ###########SendToServer###################(H :2字节  Q:8 字节)

            sockFile=staticVar.getSockFile()
            str1 = struct.pack("!2BHQ", 0x00, 0xFF, fileNameLen, fileContentLen)
            sockFile.sendall(str1 + fileName)

            sockFile.sendall(bytearray(head))
            for block in self.IQList:
                sockFile.sendall(bytearray(block))
            sockFile.sendall(struct.pack("!B", 0x00))
            del self.IQList

            self.countTdoa+=1
            print 'self.countTdoa',self.countTdoa





