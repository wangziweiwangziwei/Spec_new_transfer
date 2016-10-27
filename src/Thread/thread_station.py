# -*- coding: utf-8 -*-
import threading
import wx
from src.Package.package import *
import time
import select 
import sqlite3
from src.CommonUse.staticVar import staticVar
from src.CommonUse.staticFileUpMode import staticFileUp
from src.Package.package import Hour5bit
import os

import  thread_recv_iq
import class_upload_iq
import  class_upload
import class_upload_poa

import thread_recv_tdoa
import  class_upload_tdoa
import socket
import struct

from threading import Thread
from src.CommonUse.byte_2_package import ByteToPackage
from numpy import linspace
from src.Package.logg import Log
############中心站响应数据接收##################################
class ReceiveServerData(threading.Thread): 
    def __init__(self,mainframe): 
        threading.Thread.__init__(self)
        
        self.dictFreqPlan=staticVar.getdictFreqPlan()
        self.event = threading.Event()
        self.event.set()
        self.sock=staticVar.getSock()
        self.sockFile=staticVar.getSockFile()
        self.outPoint=staticVar.outPoint
        self.specFrame=mainframe.SpecFrame
        self.specFrame.iq_sequence=0

        self.mainframe=mainframe

        self.thread_tdoa=0

        '''这里是四个发送文件的class'''
        self.send_file_class=class_upload.SendFileClass(self.specFrame,self.mainframe.queueFFTUpload,
                                                        self.mainframe.queueAbUpload)

        self.send_file_iq_class=class_upload_iq.SendIQFile(self.mainframe)

        self.send_file_poa_class=class_upload_poa.SendPoaFile()

        self.send_file_tdoa_class=class_upload_tdoa.SendTdoaFile()

        self.count_heart_beat=0
        self.thread_timer=0
        self.thread_timer=0
        '''0:spec   1:iq    2: POA  3: TDOA  文件上传'''
        self.switch_to_transfer=0

        self.rlist=[self.sock,self.sockFile]
        self.wlist=[self.sock,self.sockFile]
        self.xlist=[self.sock,self.sockFile]

    def hello(self):
        self.thread_timer=1 #控制定时心跳线程开启
        self.sock.sendall(struct.pack("!B", 0x55))
        self.sock.sendall(struct.pack("!B", 0x66))
        Log.getLogger().debug("###send heartbeat to server####")
        self.count_heart_beat+=1
        time.sleep(15)
        self.thread_timer=0




    def stop(self):
        self.event.clear()
    def run(self):
#         self.sock.setblocking(0)
#         self.sockFile.setblocking(0)
        while(1):
            self.event.wait()
            dataLen=[]
            ListData=[]
            readyInput,readyOutput,readyException=select.select(self.rlist,self.wlist,self.xlist,60)

            if(readyInput==[] and readyOutput==[] and  readyException==[]):
                print 'not ready ---'
            #
#                 ip="27.17.8.142"
#                 data = os.system("ping -n 1 -w 1 "+ip)#使用os.system返回值判断是否正常
#                 if data==0:
#                     print u"%s: 正常运行" % ip
#                 else:
#                     print u"%s: 停止工作,正在重新连接" % ip
            else:
                if(len(readyOutput)):
                    for outsock in readyOutput:

                        if outsock == self.sock:
                            # 发送服务请求
                            try:
                                if(not self.mainframe.queueRequest.empty() ):
                                    obj=self.mainframe.queueRequest.get()
                                    self.sock.sendall(bytearray(obj))
                                    Log.getLogger().debug(" send the request to server: %s" % obj)

                                else:
                                    if(self.thread_timer==0):
                                        thread=Thread(target=self.hello)
                                        thread.start()
                            except socket.error, e:
                                print e.message, '--->send_in_sock'
                                Log.getLogger().debug(" socket_error_found_in_self.sock_send_process: %s" % e)
                                Log.getLogger().debug(" Cur self.sock: %s" % self.sock)

                                self.ReConnect()

                            #发送文件（POA，TDOA，功率谱，IQ 四种文件）
                        elif outsock == self.sockFile:
                            try:

                                if(self.switch_to_transfer==0):
                                    self.send_file_class.SendSpec()
                                elif(self.switch_to_transfer==1):
                                    self.send_file_iq_class.upload_iq()
                                    self.switch_to_transfer=0  #恢复成spec 方式
                                elif(self.switch_to_transfer==2):
                                    self.send_file_poa_class.send_poa_data()
                                elif(self.switch_to_transfer==3):
                                    self.send_file_tdoa_class.upload_tdoa()


                            except socket.error,e:
                                print e.message,'--->send_in_sockFile'
                                Log.getLogger().debug(" socket_error_found_in_self.sockFile_send_process: %s" % e)
                                Log.getLogger().debug(" Cur self.sockFile: %s" % self.sockFile)

                                self.ReConnect()



                if(len(readyInput)):
                    try:
                        for insock in readyInput:
                            if insock == self.sock:

                                ListData = []
                                data = self.sock.recv(2)
                                for i in data:
                                    ListData.append(ord(i))
                                if(len(ListData)==2):
                                    Log.getLogger().debug("Read command from server")

                                    self.funcParaDecide(dataLen, ListData)


                                # count = 0
                                # while (count < 5):
                                #     try:
                                #         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                #         self.sock = sock.connect(('115.156.209.42', 9000))
                                #         self.sockeFile = sock.connect(('115.156.209.42', 9988))
                                #     except socket.error, e:
                                #         count += 1
                                #         time.sleep(5)
                                # if (count < 5):
                                #     staticVar.sock = self.sock
                                #     staticVar.sockFile = self.sockFile
                                #
                                #     self.rlist = [self.sock, self.sockFile]  ##便于timer 控制
                                #     self.wlist = [self.sockFile]
                                #     self.xlist = [self.sock, self.sockFile]



                            elif insock == self.sockFile:
                                self.sockFile.recv(1024)
                                '''
                                self.sockFile.recv(2)
                                list1=[]
                                data = self.sockFile.recv(2)
                                for i in data:
                                    list1.append(ord(i))
                                fileNameLen=(list1[0]<<8)+(list1[1])
                                fileName=''
                                data=self.sockFile.recv(fileNameLen)
                                for i in data:
                                    fileName+=chr(ord(i))

                                print fileName ,' recv filename'

                                if(self.switch_to_transfer==3):
                                    os.remove(os.getcwd()+"\\LocalData\\Tdoa\\" + fileName)
                                elif(self.switch_to_transfer==2):
                                    os.remove(os.getcwd()+"\\LocalData\\Poa\\" + fileName)
                                '''

                                # print 'ready input ---sockFile---'
                                #
                                # try:
                                #     data=self.sockFile.recv(2)
                                #     if(data[0]==0x00 and data[1]==0xFF):
                                #         data=self.sock.recv(2)
                                #         for i in data:
                                #             ListData.append(ord(i))
                                #     self.historyDataDecide(ListData)
                                # except socket.error, e:
                                #     print "socket error: %s" % e
                                #     staticVar.sock=0
                                #     staticVar.sockFile=0
                                #     self.input1=[]
                    except socket.error,e:
                        print e.message,'--->>>input'
                        Log.getLogger().debug(" socket_error_found_in_recv_server_command: %s",e)
                        Log.getLogger().debug(" Cur self.sock: %s" % self.sock)
                        Log.getLogger().debug(" Cur self.sockFile: %s" % self.sockFile)


                        self.ReConnect()



                if (len(readyException)):
                    for i in readyException:
                        print i.message,'--->exception'
                        Log.getLogger().debug("Find some Exception: %s"%(i.message))
                        Log.getLogger().debug(" Cur self.sock: %s" % self.sock)
                        Log.getLogger().debug(" Cur self.sockFile: %s" % self.sockFile)
                    #self.ReConnect()


    def setTick(self,begin_lab,end_lab,begin,end):
        ###设置线条的xdata################
        begin_lab = int(round(begin_lab))
        end_lab = int(round(end_lab))
        

        xx = linspace(begin, end, 1024)        
        
        self.mainframe.SpecFrame.panelFigure.lineSpec.set_xdata(xx)
        self.mainframe.SpecFrame.panelFigure.lineSpecBack.set_xdata(xx)

        ##设置显示范围（包括文本框和Label）####################
        self.mainframe.FreqMin = begin_lab
        self.mainframe.FreqMax = end_lab
        self.mainframe.SpecFrame.panelFigure.Min_X.SetLabel(str(begin_lab))
        self.mainframe.SpecFrame.panelFigure.Max_X.SetLabel(str(end_lab))

        self.mainframe.SpecFrame.panelFigure.setSpLabel(begin_lab, end_lab)


    def ReConnect(self):
        Log.getLogger().debug("---Start reconnect--")


        print 'reconnect---------------reconnect------------------->>>>>>>>>>>>'
        flag_sock = 0
        flag_sockFile = 0
        count = 0

        self.rlist = []
        self.wlist = []
        self.xlist = []
        try:
            staticVar.sock.close()
            staticVar.sockFile.close()
        except Exception , e:
            pass
        staticVar.sock=0
        staticVar.sockFile=0
        
        
        self.count_heart_beat=0
        staticVar.count_heart_beat=0



        while (count < 1000):
            if (staticVar.sock == 0 and flag_sock == 0):
                try:
                    self.mainframe.serverCom.ConnectToServerMoni(self.mainframe.ip_moni,self.mainframe.port_moni)
                    staticVar.sock = self.mainframe.serverCom.sock
                    flag_sock = 1
                    self.sock=staticVar.sock
                except Exception, e:
                    print e
            if (staticVar.sockFile == 0 and flag_sockFile == 0):
                try:
                    self.mainframe.serverCom.ConnectToServerFile(self.mainframe.ip_file,self.mainframe.port_file)
                    staticVar.sockFile = self.mainframe.serverCom.sockFile
                    flag_sockFile = 1
                    self.sockFile=staticVar.sockFile
                except Exception,e:
                    print e


            if (flag_sock and flag_sockFile):
                break
            else:
                count += 1
                time.sleep(5)

        if(count<1000):
            connect = ConnectServer()

            connect.CommonHeader = FrameHeader(0x55, 0xA1, staticVar.getid() & 0x00FF, staticVar.getid() >> 8)
            connect.CommonTail = self.mainframe.tail

            if (self.mainframe.GPS_list == []):
                # 临时加的测试
                self.GPS_list = [0] * 9
                #############################

                Lon = 114.4202
                Lat = 30.5100
                Alti = 35
                Lon_fen = 0.4202 * 60
                Lat_fen = 0.51 * 60
                Lon_fen_I = int(Lon_fen)
                Lon_fen_f = int((Lon_fen - int(Lon_fen)) * 1000)
                Lat_fen_I = int(Lat_fen)
                Lat_fen_f = int((Lat_fen - int(Lat_fen)) * 1000)

                self.GPS_list[1] = 114
                self.GPS_list[2] = (Lon_fen_I << 2) + (Lon_fen_f >> 8)
                self.GPS_list[3] = Lon_fen_f & 0x00FF
                self.GPS_list[4] = 30
                self.GPS_list[5] = (Lat_fen_I << 2) + (Lat_fen_f >> 8)
                self.GPS_list[6] = Lat_fen_f & 0x00FF
                self.GPS_list[8] = 35

            list = self.mainframe.GPS_list

            connect.LonLatAlti = LonLatAltitude(list[0], list[1], list[2], list[3], list[4] >> 7, list[4] & 0x7F,
                                                list[5], list[6], list[7] >> 7, list[7] & 0x7F, list[8])
            self.sock.sendall(bytearray(connect))

            self.rlist = [self.sock, self.sockFile]
            self.wlist = [self.sock, self.sockFile]
            self.xlist = [self.sock, self.sockFile]

            Log.getLogger().debug(" ---ReConnect Complete---")
            Log.getLogger().debug(" Cur self.sock: %s" % self.sock)
            Log.getLogger().debug(" Cur self.sockFile: %s" % self.sockFile)


    def historyDataDecide(self,ListData):
        BUFSIZE=4096
        for i in ListData:
            print i,
        print '########'
        ##在这里判断是功率谱或者IQ(spec:0x00,0xFF,fileNameLen,fileLen,Name,Content)
        ######(iq:0x00,0xFF,fileNameLen,fileLen,Name,Content) \
        fileLen_l=[]
        fileNameLen=(ListData[0]<<8)+(ListData[1])
        fileName=[]
        ListData=[]
        
        ## receive fileContentLen  ###        
        data=self.sock.recv(8)
        for i in data:
            fileLen_l.append(ord(i))
        
        ## receive fileName  ##
        
        data=self.sock.recv(fileNameLen)
        for i in data:
            fileName.append(chr(i))
        
        ## receive content  ##
        
        Content=self.RecvContent(self.sockFile,fileLen_l,ListData, BUFSIZE)
        
        ## save file to local ##
        
        self.saveFile(fileName,Content)
    
    def saveFile(self,fileName,Content):
        ##########SaveToLocal#####################
#         fid=open(".\LocalData\\"+ fileName,'wb+')
        if(not os.path.exists("./LocalData//SpecHistory//")):
            os.makedirs('./LocalData//SpecHistory//')
            os.makedirs('./LocalData//IQHistory//')
            
        dir='./LocalData//SpecHistory//'
        if(fileName[-2:]=='iq'):
            dir='./LocalData//IQHistory//'
            
        fileName1=''
        for i in fileName:
            fileName1+=str(i)
        fid=open(dir +fileName1,'wb+')
        fid.write(bytearray(Content))
        
        fid.close()
         
                                    
    def funcParaDecide(self,dataLen,ListData):
        if(ListData[0]==0x77 and ListData[1]==0x88):
            print '#### server heart beat #####'
            staticVar.count_heart_beat+=1
            Log.getLogger().debug("##Receive Server HeartBeat##")

            if(abs(self.count_heart_beat-staticVar.count_heart_beat)>2):
                print 'heart beat stop'
                Log.getLogger().debug("##HeartBeat is not equal ##")

                raise socket.error

            
        else:
            # ListData[0]=0x55

            BUFSIZE=4096
            frameFlag=ListData[1]
            print 'frameflag',frameFlag
            if(frameFlag>0 and frameFlag<=14):  ##服务器设置指令下发##
                print 'recv set command'

                if(frameFlag==11): #中心站发下来的停止功率谱上传的帧(关闭上传)
                    self.sock.recv(5)
                    staticFileUp.setUploadMode(0)  ##设置成手动，然后recv_fft 线程就不会往上传队列里面加

                elif(frameFlag==10):  #功率谱数据上传开启
                    self.sock.recv(5)
                    staticFileUp.setUploadMode(2)

                elif(frameFlag==6):  #模板下发
                    data=self.sock.recv(257)
                    for i in data:
                        ListData.append(ord(i))
                    self.outPoint.write(bytearray(ListData))



                else:
                    data=self.sock.recv(15)
                    for i in data:
                        ListData.append(ord(i))

                    if(frameFlag==0x01):
                        ### 扫频设置 ###
                        byte_to_pacakge=ByteToPackage()
                        obj=byte_to_pacakge.ByteToSweepRange(ListData)

                        staticFileUp.setUploadMode(obj.FileUploadMode-1)
                        staticFileUp.setUploadMode(obj.ExtractM)


                        begin_lab= 70+(obj.StartSectionNo-1 )*25 +\
                        ((obj.HighStartFreq<<8)+(obj.LowStartFreq))*25.0/1024
                        end_lab =  70+(obj.EndSectionNo-1 )*25 +\
                        ((obj.HighEndFreq <<8)+(obj.LowEndFreq))*25.0/1024

                        begin = 70+(obj.StartSectionNo-1 )*25
                        end = 70+(obj.EndSectionNo)*25
                        
                        self.setTick(begin_lab,end_lab,begin,end)

                    self.outPoint.write(bytearray(ListData))


                    if (frameFlag == 0x02):
                        thread = thread_recv_iq.ReceiveIQThread(self.mainframe)

                        thread.start()
                        self.switch_to_transfer=1



                '''
                if(frameFlag==0x07):

                    
                    #######  转UTC 格式 ########
                    hour=((ListData[8]&0x07)<<2)+(ListData[9]&0x03)
                    temp1=ListData[8]&0xF8
                    temp2=ListData[9]&0xFC 
                    hour-=8
                    HourStruct=Hour5bit(hour,0)
                    ListData[8]=temp1+(HourStruct.Hour>>2)
                    ListData[9]=temp2+(HourStruct.Hour&0x03)
                    ############################    
                    '''

            elif(frameFlag>=17 and frameFlag<=30):  ##服务器查询指令下发####
                print 'recv query'
                data=self.sock.recv(5)
                for i in data:
                    ListData.append(ord(i))

                if(frameFlag==0x1A):  ##查询上传是否开启
                    structObj=Query()
                    structObj.CommonTail=FrameTail(0,0,0xAA)
                    status=staticFileUp.getUploadMode()
                    if(status):
                        structObj.CommonHeader=\
                            FrameHeader(0x66,0x2A,staticVar.getid()&0x00FF,staticVar.getid()>>8)
                    else:
                        structObj.CommonHeader= \
                            FrameHeader(0x66, 0x2B, staticVar.getid() & 0x00FF, staticVar.getid() >> 8)
                    self.sock.sendall(bytearray(structObj))
                else:
                    self.outPoint.write(bytearray(ListData))
                    li=0
                    count=0
                    while(count<3):
                        try:
                            li = list(staticVar.inPointRecv.read(260,100))
                            if(li): break
                        except Exception,e:
                            time.sleep(0.5)
                            count+= 1
                            print e

                    if(not li == 0):
                        if(len(li)==260):
                            self.sock.sendall(bytearray(li[0:-1]))
                        else:
                            self.sock.sendall(bytearray(li))

            
            elif(frameFlag==0x41 or frameFlag==0x42):
                print 'recv iq tdoa **'
                data=self.sock.recv(15)
                for i in data:
                    ListData.append(ord(i))
                self.sock.recv(2)    
               
                self.specFrame.iq_sequence=(ListData[-2]<<8)+ListData[-3]
                ListData[-3]=0
                ListData[-2]=0
                ListData[-1]=0xAA
                    
                # ListData[0]=0x55
                    
                if(frameFlag==0x42):
                    
                    ListData[1]=0x07
                    #######  转UTC 格式 ########
                    hour=((ListData[8]&0x07)<<2)+(ListData[9]&0x03)
                    temp1=ListData[8]&0xF8
                    temp2=ListData[9]&0xFC 
                    hour-=8
                    ListData[8]=temp1+(hour>>2)
                    ListData[9]=temp2+(hour&0x03)
                    ############################
                else:
                    ListData[1]=0x02
                   
                print 'ListData',ListData      
                self.outPoint.write(bytearray(ListData))

                if(frameFlag == 0x42):
                    thread = thread_recv_iq.ReceiveIQThread(self.mainframe)
                    thread.start()

                    self.switch_to_transfer=1

            elif(frameFlag==49):
                '''POA frame '''
                data = self.sock.recv(15)
                for i in data:
                    ListData.append(ord(i))
                self.outPoint.write(bytearray(ListData))

                self.switch_to_transfer=2

                print 'POA frame has been write'

            elif(frameFlag==50):
                '''TDOA frame'''
                data = self.sock.recv(17)
                for i in data:
                    ListData.append(ord(i))
                self.outPoint.write(bytearray(ListData))
                print 'TDOA frame has been write'
                self.mainframe.thread_recvfft.stop()

                if(self.thread_tdoa==0):
                    self.thread_tdoa=thread_recv_tdoa.ReceiveTdoaThread(self.mainframe)
                    self.thread_tdoa.start()
                else:
                    self.thread_tdoa.event.set()



                self.switch_to_transfer=3

            elif(frameFlag==51):
                '''stop POA TDOA'''
                data = self.sock.recv(15)
                for i in data:
                    ListData.append(ord(i))

                '''设置横坐标范围 '''
                StartSectionNo=ListData[5]
                HighStartFreq=ListData[6]&0x03
                LowStartFreq=ListData[7]
                EndSectionNo=ListData[8]
                HighEndFreq=ListData[9]&0x03
                LowEndFreq=ListData[10]

                begin_lab = 70 + (StartSectionNo - 1) * 25 + \
                        ((HighStartFreq << 8) + (LowStartFreq)) * 25.0 / 1024
                end_lab = 70 + (EndSectionNo - 1) * 25 + \
                      ((HighEndFreq << 8) + (LowEndFreq)) * 25.0 / 1024

                begin = 70+(StartSectionNo-1 )*25
                end = 70+(EndSectionNo)*25
                      
                

                self.setTick(begin_lab,end_lab,begin,end)

                self.outPoint.write(bytearray(ListData))
                print 'stop command has been write'

                if(self.switch_to_transfer==3):
                    self.thread_tdoa.stop()
                    self.mainframe.thread_recvfft.event.set()

                self.switch_to_transfer=0

                self.remove( os.getcwd()+"\\LocalData\\Tdoa\\")
                self.remove( os.getcwd()+"\\LocalData\\Poa\\")


            elif(frameFlag==177):
                data=self.sock.recv(16)
                for i in data:
                    ListData.append(ord(i)) 
                    
                self.ReadConnect(ListData)
            

        ############以下是长度+帧内容#############
            else:
                data=self.sock.recv(6)
                for i in data:
                    ListData.append(ord(i))
                print ListData

                dataLen=[i for i in ListData]
                ListData=[]
                ListData=self.RecvContent(self.sock,dataLen,ListData,BUFSIZE)
                frameFlag=ListData[1]
                if(frameFlag==178):
                    self.ReadElecTrend(ListData)
                elif(frameFlag==179):
                    self.ReadElecPath(ListData)
                elif(frameFlag==180):
                    self.ReadAbFreq(ListData)
                elif(frameFlag==181):
                    self.ReadStationPro(ListData)
                elif(frameFlag==182):
                    self.ReadStationCurPro(ListData)
                elif(frameFlag==183):
                    List=[(0,u"起始频率（MHz）"),(1,u"终止频率（MHz）"),(2,u"业务类型 1")]
                    for i in range(3):
                        col = self.specFrame.panelQuery.GetColumn(i)
                        col.SetText(List[i][1])
                        self.specFrame.panelQuery.SetColumn(i, col)      
                    for i in range(7):
                        self.specFrame.panelQuery.InsertColumn(i+3,u"业务类型"+str(i+3))
                        self.specFrame.panelQuery.SetColumnWidth(i+3,100)
                        
                    self.ReadFreqPlan(ListData)
                elif(frameFlag==184):
                    self.ReadAllStationPro(ListData)
                
                elif(frameFlag==185):
                    self.ReadOnlinePortPro(ListData)
                elif(frameFlag==186):
                    self.ReadRegisterPortPro(ListData)
            
    #                     elif(frameFlag==187):
    #                      
    #                         self.ReadSpecData(ListData)
    #                     elif(frameFlag==188):
    #                     
    #                         self.ReadIQData(ListData)
                
                elif(frameFlag==0xD1):
                    obj=self.mainframe.byte_to_package.ByteToAntGain(ListData)
                    self.mainframe.show_recv_set.ShowAntGain(obj)
    
                    # self.outPoint.write(bytearray(ListData))
                elif(frameFlag==0xD2):
                    print ListData
                    print len(ListData)
                    
                    obj = self.mainframe.byte_to_package.ByteToAntGain(ListData)
                    self.mainframe.show_recv_set.ShowAntGain(obj)
    
                    # self.outPoint.write(bytearray(ListData))
                
                
                else:
                    print 'frameFlag error'

    def remove(self,delDir):
        delList = []  
       
        delList = os.listdir(delDir )  
          
        for f in delList:  
            filePath = os.path.join( delDir, f )  
            if os.path.isfile(filePath):  
                os.remove(filePath)  
                 
        

    
    def RecvContent(self,sock,dataLen,ListData,BUFSIZE):
        dataLength=(dataLen[0]<<56)+(dataLen[1]<<48)+(dataLen[2]<<40)+ \
        (dataLen[3]<<32)+(dataLen[4]<<24)+(dataLen[5]<<16)+(dataLen[6]<<8)+dataLen[7]
        totalLen=0
        while(totalLen<dataLength):
            data=sock.recv(min(BUFSIZE,dataLength-totalLen))
            for i in data:
                ListData.append(ord(i))
            totalLen+=len(data)               
        
        return ListData
     
    def ReadConnect(self,ListData):
        print ' response from server'
        Log.getLogger().debug("##Connect Response from Server##")

        if(ListData[4]==0x0F):
            TerminalType=ListData[5]
            Pos=self.ByteToPos(ListData[6:15])


                        

        else:
            wx.MessageBox(u'服务器拒绝连接', \
                          u'警告',wx.ICON_EXCLAMATION | wx.STAY_ON_TOP)
            
            self.stop()
            '''    
            wx.lib.dialogs.ScrolledMessageDialog(parent, msg, caption,
            pos=wx.wxDefaultPosition, size=(500,300))
            '''
    ###########################辅助函数######################
    def ByteToTime(self,Data):
        Time =(((Data[0]<<4)+((Data[1])>>4)),(Data[1]&0x0F),(Data[2]>>3), \
                                        (((Data[2]&0x07)<<2)+(Data[3]&0x03)),(Data[3]>>2))
        return Time 
    
    def ByteToPos(self,Data):
        lonFlag=1
        latFlag=1
        altiFlag=1
        
        if(Data[0]):
            lonFlag=-1
        if(Data[4]>>7):
            latFlag=-1
        if(Data[7]>>7):
            altiFlag=-1
        
        LonLatAlti=LonLatAltitude(Data[0],Data[1],Data[2],Data[3],Data[4]>>7, \
                                        Data[4]&0x7F,Data[5],Data[6],Data[7]>>7,  \
                                        Data[7]&0x7F,Data[8])
        
        fen=float((LonLatAlti.HighLonFraction<<8) + LonLatAlti.LowLonFraction)/2**16
        Lon=LonLatAlti.LonInteger+fen

        fen =float((LonLatAlti.HighLatFraction <<8) + LonLatAlti.LowLatFraction)/2**16
        Lat = LonLatAlti.LatInteger + fen

        Alti=(LonLatAlti.HighAltitude<<8)+LonLatAlti.LowAltitude

        print 'Lon,Lat,Alti ',Lon,Lat,Alti
        Lon=Lon*lonFlag

        Lat=Lat*latFlag

        Alti=Alti*altiFlag
        if(Lon==0):
            Lon=114.420239
            Lat=30.515488
            Alti=29

        return (Lon,Lat,Alti)

    def ByteToPower(self,Data):
        if(Data[0]>>7):
            Power=((Data[0]&0x7F)<<5)+(Data[1]>>3)+float((Data[1]&0x03))/8
            Power=-Power
        else:
            Power=(Data[0]<<5)+(Data[1]>>3)+float((Data[1]&0x03))/8

        return Power
    
    def TimeToStr(self,ListTime):
        strTimeList=[]
        for time in ListTime:
            strTime=str(time[0])+'-'+str(time[1])+'-'+str(time[2])+'-' \
            +str(time[3])+'-'+str(time[4])
            strTimeList.append(strTime)
        return strTimeList   
    
    def MessageBox(self,x):
        wx.MessageBox(u'数据库插入   '+str(x)+u"  行" ,
                         
                       'Alert', wx.ICON_EXCLAMATION | wx.STAY_ON_TOP)
        
    ##########################################################
    def ReadElecTrend(self,ListData):
        stationID=ListData[2]+(ListData[3]<<8)
        centreFreq=(ListData[4]<<8)+(ListData[5])
        bandWidth=ListData[6]
        counts=ListData[7]
        intervalTime=ListData[8]
        N_x=ListData[9]
        N_y=ListData[10]
        delta=(ListData[11]>>3)+float(ListData[11]&0x07)/8
        ListTime=[]
        ListP=[]
        i=12
        lenData=len(ListData)
        while(i<lenData-3):
            Time=self.ByteToTime(ListData[i:i+4])
            ListTime.append(Time)
            Pos=self.ByteToPos(ListData[i+4:i+13])
            Power=self.ByteToPower(ListData[i+13:i+15])
                                
            efficent=(ListData[i+15]>>4)+float(ListData[i+15]&0x0F)/16
            ListP.append((Pos[0],Pos[1],Pos[2],Power,efficent)) 
            i=i+16
        ##转成str格式  YY-MM-DD-HH-MM-SS
         
        strTimeList=self.TimeToStr(ListTime)
        ####数据库插入操作############
        conn=sqlite3.connect('C:/DataBase/PortSRF.db')
        print"Create database successfully"

        for i in range(len(strTimeList)):
            conn.execute("INSERT INTO  ELEC_DISTRIBUTION    \
            (TERMINALID,CENTERFREQUENCY ,BANDWIDTH ,COUNTS,INTERVALTIME, \
            NX ,NY ,DLETA,DTIME,LONGITUDE, LATITUDE ,HEIGHT ,TRANSFERPOWER ,TRANSINDEX ) \
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", \
            (stationID,centreFreq,bandWidth,counts,intervalTime,  \
             N_x,N_y,delta,strTimeList[i],ListP[i][0],ListP[i][1], \
             ListP[i][2],ListP[i][3],ListP[i][4]));
    
        conn.commit()
        print "Records created successfully-elec_distribute";
            
#         ####测试看是否写入了############
#         cursor = conn.execute("SELECT * from ELEC_DISTRIBUTION ")
#         for row in cursor:
#             for each in row :
#                 print each,
#             print 

        x=conn.total_changes
        conn.close()
        self.MessageBox(x)               
        
    def ReadElecPath(self,ListData):
        stationID=ListData[2]+(ListData[3]<<8)
        centreFreq=(ListData[5]<<8)+ListData[6]
        bandWidth=ListData[7]
        i=8
        ListTime=[]
        ListP=[]
        while(i<len(ListData)-17):
            Time =self.ByteToTime(ListData[i:i+4])
            ListTime.append(Time)
            Pos=self.ByteToPos(ListData[i+4:i+13])
            Power=self.ByteToPower(ListData[i+13:i+15])
    
            ListP.append((Pos[0],Pos[1],Pos[2],Power)) 
            i=i+15
        
        strTimeList=self.TimeToStr(ListTime)
        (Lon,Lat,Alti)=self.ByteToPos(ListData[i:i+9])
        Power_TPOA=self.ByteToPower(ListData[i+9:i+11])
        CEP_Radius=(ListData[i+11]<<8)+(ListData[i+12])
        
        ####数据库插入操作############
        conn=sqlite3.connect('C:/DataBase/PortSRF.db')
        print"Create database successfully"

        for i in range(len(strTimeList)):
            conn.execute("INSERT INTO  ROUTE    \
            (TERMINALID,CENTERFREQUENCY ,BANDWIDTH ,DTIME, \
            LONGITUDE, LATITUDE ,HEIGHT ,RECEIVEDPOWER ) \
            VALUES (?,?,?,?,?,?,?,?)", \
            (stationID,centreFreq,bandWidth,  \
             strTimeList[i],ListP[i][0],ListP[i][1], \
             ListP[i][2],ListP[i][3]));
    
        conn.commit()
        print "Records created successfully-route";
            
#         ####测试看是否写入了############
#         cursor = conn.execute("SELECT * from ROUTE ")
#         for row in cursor:
#             for each in row :
#                 print each,
#             print 

        x=conn.total_changes
        conn.close()
        self.MessageBox(x)        
        
    def ReadAbFreq(self,ListData):
        stationID=ListData[2]+(ListData[3]<<8)
        centreFreq=(ListData[4]<<6)+(ListData[5]&0x3F)+float(((ListData[5]>>6)<<8)+ListData[6])/2**10
        bandWidth=(ListData[7]&0x3F) + float(((ListData[7]>>6)<<8)+ListData[8])/2**10
        modulateMode=0
        modulateParam=0
        if(ListData[9]):
            modulateMode=ListData[9]
            modulateParam=ListData[10]+float(ListData[11])/2**8
        i=12
        ListP=[]
        Pos=self.ByteToPos(ListData[i:i+9])
        Power=self.ByteToPower(ListData[i+9:i+11])
                            
        efficent=(ListData[i+11]>>4)+float(ListData[i+11]&0x0F)/16
        ListP.append((Pos[0],Pos[1],Pos[2],Power,efficent)) 
        
#         TimeComsume=str(ListData[i+12])+'%'
#         WorkPro=dictFreqPlan[ListData[i+13]]   
        ActivityDegree=ListData[i+12]
        ServiceAttribute=ListData[i+13]      
        IsIllegal=ListData[i+14]
        
        # belonging (1:liantong 2:yidong 3:dianxin)
        OwnUint=''
        for j in xrange((i+15),(i+23),1):
            if(ListData[j]==1):
                OwnUint='chinaUnion'
            elif(ListData[j]==2):
                OwnUint='chinaMove'
            elif(ListData[j]==3):
                OwnUint='chinaNet'
            else:
                pass 
        
        
        ####数据库插入操作############
        conn=sqlite3.connect('C:/DataBase/PortSRF.db')
        print"Create database successfully"

        
        conn.execute("INSERT INTO  ABNORMAL    \
        (ABNORMALID ,BELONGING,LONGITUDE,LATITUDE,  \
       HEIGHT,CENTERFREQUENCY,BANDWIDTH,PARAMETER, \
  MODULATIONMODE,TRANSPOWER ,TRANSINDEX ,ACTIVITYDEGREE , \
  SERVICEATTRIBUTE,ISILLEGAL) \
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", \
        (stationID, OwnUint,ListP[0][0],ListP[0][1], \
         ListP[0][2],centreFreq,bandWidth,modulateParam, \
         modulateMode,ListP[0][3],ListP[0][4],ActivityDegree,\
         ServiceAttribute,IsIllegal));

        conn.commit()
        print "Records created successfully-ab";
        
#         ####测试看是否写入了############
#         cursor = conn.execute("SELECT * from ABNORMAL")
#         for row in cursor:
#             for each in row :
#                 print each,
#             print 

        x=conn.total_changes
        conn.close()
        self.MessageBox(x)            
            
    def ReadStationPro(self,ListData):
        ListStation=[]
        i=4
        while(i<len(ListData)-3):
            OwnUnit=''
            for j in xrange(i,i+8,1):
                OwnUnit+=chr(ListData[j])
            Identifier=(ListData[i+8]<<16)+(ListData[i+9]<<8)+ListData[i+10]
            Pos=self.ByteToPos(ListData[i+11:i+20])
            FreqStart=(ListData[i+20]<<8)+ListData[i+21]
            FreqEnd=(ListData[i+22]<<8)+ListData[i+23]
            Power=self.ByteToPower(ListData[i+24:i+26])
            bandWidth=(ListData[i+26]&0x3F) + float(((ListData[i+26]>>6)<<8)+ListData[i+27])/2**10
#             modulate=List[ListData[i+28]]
            modulateMode=ListData[i+28]
            modulateParam=ListData[i+29]+float(ListData[i+30])/2**8
            ServiceAttribute=ListData[i+31]
#             WorkPro=dictFreqPlan[ListData[i+31]]
            Radius=ListData[i+32]
#             TimeComsume=str(ListData[i+33])+'%'
            ActivityDegree=ListData[i+33]
            ListStation.append((Identifier,OwnUnit,Pos[0],Pos[1],Pos[2],FreqStart,FreqEnd, \
                                 Power,bandWidth,modulateMode,modulateParam, \
                                    ServiceAttribute,Radius,ActivityDegree))
            
            i+=34
        

        ####数据库插入操作############
        conn=sqlite3.connect('C:/DataBase/PortSRF.db')
        print"Create database successfully"

        for i in range(len(ListStation)):
            conn.execute("INSERT INTO  REGISTEREDSTATION    \
            (STATIONID,BELONGING,LONGITUDE, LATITUDE,HEIGHT,  \
            STARTFREQ,ENDFREQ ,MAXTRANSPOWER,BANDWIDTH ,MODULATIONMODE, \
            PARAMETER ,SERVICEATTRIBUTE,COVERAGERADIUS,ACTIVITYDEGREE) \
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", \
            (ListStation[i][0],ListStation[i][1],ListStation[i][2],ListStation[i][3],
             ListStation[i][4],ListStation[i][5],ListStation[i][6],ListStation[i][7],
             ListStation[i][8],ListStation[i][9],ListStation[i][10],ListStation[i][11],
             ListStation[i][12],ListStation[i][13]));
    
        conn.commit()
        print "Records created successfully-registerStation";
            
#         ####测试看是否写入了############
#         cursor = conn.execute("SELECT * from REGISTEREDSTATION ")
#         for row in cursor:
#             for each in row :
#                 print each,
#             print 

        x= conn.total_changes
        conn.close()
        self.MessageBox(x)        
        
            
    def ReadStationCurPro(self,ListData):
        i=4
        
        OwnUnit=''
        for j in xrange(i,i+8,1):
            OwnUnit+=chr(ListData[j])
        Identifier=(ListData[i+8]<<16)+(ListData[i+9]<<8)+ListData[i+10]
        Pos=self.ByteToPos(ListData[i+11:i+20])
        centreFreq=(ListData[i+20]<<6)+(ListData[i+21]&0x3F)+float(((ListData[i+21]>>6)<<8)+ListData[i+22])/2**10
        Power=self.ByteToPower(ListData[i+23:i+25])
        efficent=(ListData[i+25]>>4)+float(ListData[i+25]&0x0F)/16
        
        bandWidth=(ListData[i+26]&0x3F) + float(((ListData[i+26]>>6)<<8)+ListData[i+27])/2**10
#         modulate=List[ListData[i+28]]
        modulateMode=ListData[i+28]
        modulateParam=ListData[i+29]+float(ListData[i+30])/2**8
#         WorkPro=dictFreqPlan[ListData[i+31]]
#         TimeComsume=str(ListData[i+32])+'%'
        ServiceAttribute=ListData[i+31]
        ActivityDegree=ListData[i+32]
        IsIllegal=ListData[i+33]
        
        ####数据库插入操作############
        conn=sqlite3.connect('C:/DataBase/PortSRF.db')
        print"Create database successfully"

       
        conn.execute("INSERT INTO  STATIONPROPERTY    \
        (STATIONID,BELONGING,LONGITUDE, LATITUDE,HEIGHT,  \
         CENTERFREQUENCY,TRANSPOWER,TRANSINDEX,BANDWIDTH,MODULATIONMODE,\
         PARAMETER,SERVICEATTRIBUTE,ACTIVITYDEGREE,ISILLEGALWORKING) \
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", \
        (Identifier,OwnUnit,Pos[0],Pos[1],Pos[2],centreFreq,Power, \
         efficent,bandWidth,modulateMode,modulateParam,ServiceAttribute,\
         ActivityDegree,IsIllegal));

        conn.commit()
        print "Records created successfully-curPro";
            
#         ####测试看是否写入了############
#         cursor = conn.execute("SELECT * from STATIONPROPERTY ")
#         for row in cursor:
#             for each in row :
#                 print each,
#             print 

        x=conn.total_changes
        conn.close()
        self.MessageBox(x)        
        
        
            
    def ReadFreqPlan(self,ListData):
        i=4
        count=0
        lenData=len(ListData)
        while(i<lenData-3):
            startHigh4bit=(ListData[i+2])>>4
            startLow4bit=ListData[i+2]&0x0F
            endHigh4bit=ListData[i+6]>>4
            endLow4bit=ListData[i+6]&0x0F
            startFreqInteger=(ListData[i]<<12)+(ListData[i+1]<<4)+startHigh4bit
            startFreqFraction=float((startLow4bit<<8)+ListData[i+3])/2**12
            endFreqInteger=(ListData[i+4]<<12)+(ListData[i+5]<<4)+endHigh4bit
            endFreqFraction=float((endLow4bit<<8)+ListData[i+7])/2**12
            
            startFreq=startFreqInteger+startFreqFraction
            endFreq=endFreqInteger+endFreqFraction
            j=i+8
            freqPro=[]
            r=0
            while(r<8 and ListData[j]):
                freqPro.append(ListData[j])
                r=r+1
                j=j+1
            
            self.specFrame.panelQuery.SetStringItem(count,0,str('%0.5f'%startFreq))
            self.specFrame.panelQuery.SetStringItem(count,1,str('%0.5f'%endFreq))
            for k in xrange(len(freqPro)):
                self.specFrame.panelQuery.SetStringItem(count,k+2,self.dictFreqPlan[freqPro[k]])
            count=count+1
            i=i+16
            
        while(count<1000):
            self.specFrame.panelQuery.SetStringItem(count,0,'')
            self.specFrame.panelQuery.SetStringItem(count,1,'')
            self.specFrame.panelQuery.SetStringItem(count,2,'')
            count=count+1
    
    def ReadAllStationPro(self,ListData):
        ListStation=[]

        i=4
        while(i<len(ListData)-3):
            OwnUnit=''
            for j in xrange(i,i+8,1):
                OwnUnit+=chr(ListData[j])
            Pos=self.ByteToPos(ListData[i+11:i+20])
            FreqStart=(ListData[i+20]<<8)+ListData[i+21]
            FreqEnd=(ListData[i+22]<<8)+ListData[i+23]
            Power=self.ByteToPower(ListData[i+24:i+26])
            bandWidth=(ListData[i+26]&0x3F) + float(((ListData[i+26]>>6)<<8)+ListData[i+27])/2**10
#             modulate=List[ListData[i+28]]
            modulateMode=ListData[i+28]
            modulateParam=ListData[i+29]+float(ListData[i+30])/2**8
#             WorkPro=dictFreqPlan[ListData[i+31]]
            ServiceAttribute=ListData[i+31]
            Radius=ListData[i+32]
#             TimeComsume=str(ListData[i+33])+'%'
            ActivityDegree=ListData[i+33]
            
            Identifier=0xFF
    
            if(not ((ListData[i+8])==0xFF)):
                Identifier=(ListData[i+8]<<16)+(ListData[i+9]<<8)+ListData[i+10]
                
            ListStation.append((Identifier,OwnUnit,Pos[0],Pos[1],Pos[2],Identifier,FreqStart,FreqEnd, \
                                Power,bandWidth,modulateMode,modulateParam, \
                                ServiceAttribute,Radius,ActivityDegree))
            
            i+=34
            
        ####数据库插入操作############
        conn=sqlite3.connect('C:/DataBase/PortSRF.db')
        print"Create database successfully"

        for i in range(len(ListStation)):
            conn.execute("INSERT INTO  REGISTEREDSTATION    \
            (STATIONID,BELONGING,LONGITUDE, LATITUDE,HEIGHT,  \
            STARTFREQ,ENDFREQ ,MAXTRANSPOWER,BANDWIDTH ,MODULATIONMODE, \
            PARAMETER ,SERVICEATTRIBUTE,COVERAGERADIUS,ACTIVITYDEGREE) \
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", \
            (ListStation[i][0],ListStation[i][1],ListStation[i][2],ListStation[i][3],
             ListStation[i][4],ListStation[i][5],ListStation[i][6],ListStation[i][7],
             ListStation[i][8],ListStation[i][9],ListStation[i][10],ListStation[i][11],
             ListStation[i][12],ListStation[i][13]));
    
        conn.commit()
        print "Records created successfully-registerStation";
            
#         ####测试看是否写入了############
#         cursor = conn.execute("SELECT * from REGISTEREDSTATION ")
#         for row in cursor:
#             for each in row :
#                 print each,
#             print 

        x=conn.total_changes
        conn.close()
        self.MessageBox(x)        

    def ReadOnlinePortPro(self,ListData):
        ListPort=[]
        i=6
        count=0
        N=(ListData[4]<<8)+ListData[5]
        while(count<N):
            ID=(ListData[i+1]<<8)+ListData[i]
            Pos=self.ByteToPos(ListData[i+3:i+12])
            
            TerminalGrade=ListData[i+2]
            ListPort.append((ID,TerminalGrade,Pos[0],Pos[1],Pos[2],""))
            count+=1
            i=i+12
        
        ####数据库插入操作############
        conn=sqlite3.connect('C:/DataBase/PortSRF.db')
        print"Create database successfully"

        for i in range(N):
            conn.execute("INSERT INTO  ONLINE_TERMINAL    \
            (TERMINALID,TERMINAL_GRADE,LONGITUDE, LATITUDE,HEIGHT,LOGINTIME) \
            VALUES (?,?,?,?,?,?)", \
            (ListPort[i][0],ListPort[i][1],ListPort[i][2],ListPort[i][3],
             ListPort[i][4],ListPort[i][5]));
    
        conn.commit()
        print "Records created successfully-online_terminal";
            
#         ####测试看是否写入了############
#         cursor = conn.execute("SELECT * from ONLINE_TERMINAL ")
#         for row in cursor:
#             for each in row :
#                 print each,
#             print 

        x=conn.total_changes
        conn.close()
        self.MessageBox(x)        
        
    def ReadRegisterPortPro(self,ListData):
        ListPort=[]
        i=6
        count=0
        N=(ListData[4]<<8)+ListData[5]
        while(count<N):
            ID=(ListData[i+1]<<8)+ListData[i]
            Pos=self.ByteToPos(ListData[i+3:i+12])
            TerminalGrade=ListData[i+2]
            ListPort.append((ID,TerminalGrade,Pos[0],Pos[1],Pos[2],"","",1))
            count+=1
            i=i+12
        ####数据库插入操作############
        conn=sqlite3.connect('C:/DataBase/PortSRF.db')
        print"Create database successfully"

        for i in range(N):
            conn.execute("INSERT INTO  TERMINALINFO    \
            (TERMINALID,GRADE,LONGITUDE, LATITUDE,HEIGHT,REGISTRATION_TIME, \
            LOGINTIME,STATUS) \
            VALUES (?,?,?,?,?,?,?,?)", \
            (ListPort[i][0],ListPort[i][1],ListPort[i][2],ListPort[i][3],
             ListPort[i][4],ListPort[i][5],ListPort[i][6],ListPort[i][7]));
    
        conn.commit()
        print "Records created successfully-register_terminal";
            
#         ####测试看是否写入了############
#         cursor = conn.execute("SELECT * from TERMINALINFO ")
#         for row in cursor:
#             for each in row :
#                 print each,
#             print 

        x= conn.total_changes
        conn.close()
        self.MessageBox(x)        
        
    def ReadSpecData(self,ListData):
        '''
        self.threadDrawFFT.stop()
        
        self.specFrame.panelFigure.setSpLabel()
        '''
        for i in ListData:
            print i,
        
    def ReadIQData(self,ListData):
        for i in ListData:
            print i,
    
    
    
            
'''
    
class PopFrame(wx.MDIChildFrame):
    def __init__(self,parent,name):
        wx.MDIChildFrame.__init__(self,parent,-1,name,size=(500,600))
        pane=wx.Panel(self,-1)
        self.list = wx.ListCtrl(pane,-1,style=wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES)
        self.list.InsertColumn(0, "StartFreq(MHz)")
        self.list.InsertColumn(1, 'EndFreq(MHz)')
        self.list.InsertColumn(2, 'Type')
        self.list.SetColumnWidth(0,120)
        self.list.SetColumnWidth(1, 120)
        self.list.SetColumnWidth(2, 120)
        for i in range(1,100):
            self.list.InsertStringItem(i-1,str(i))
        self.list.Fit()
          
'''


            

    
