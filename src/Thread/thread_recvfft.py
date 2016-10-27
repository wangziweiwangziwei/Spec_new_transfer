# -*- coding: utf-8 -*-
import threading

import wx
from src.Package.package import *

import time
import Queue
import struct
import sys
import math
from numpy import linspace
import usb
from src.Spectrum import Spectrum_1
from src.CommonUse.staticFileUpMode import staticFileUp
from src.CommonUse.press_hand import press_hand
from src.CommonUse.staticVar import staticVar
import cPickle as pickle

###########接受硬件上传FFT数据和异常频点并放入队列############ 
  
from src.Package.logg import Log

class ReceiveFFTThread(threading.Thread):
    def __init__(self,mainframe):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.event.set()

        self.count_for_test=0
      
        self.recvHardObj=mainframe.byte_to_package
        self.SweepRange=[]
        self.SweepRangeAb=[]
        self.SweepRangeBack=[]
        
        self.DrawIntv=20
        self.DrawBackIntv=2  ###背景功率谱间隔
        self.SweepTotalNum=0
        self.SweepCount=0
        self.SweepBackCount=0
        
         
        ###主窗口引用 从而间接引用子窗口#######
        self.mainframe=mainframe
        
        ###队列引用#####################
        self.queueFFTUpload=self.mainframe.queueFFTUpload
        self.queueAbUpload=self.mainframe.queueAbUpload
        
        self.queueFFTLocalSave=self.mainframe.queueFFTLocalSave
        self.queueAbLocalSave=self.mainframe.queueAbLocalSave

        ###############POA 应急 ########################
        
        self.count_for_abNum=0
        self.contain_poa=[]
        
        #########最大保持时保存前一次功率谱值#################
        self.yData_before = []
        for i in range(1024):
            self.yData_before.append(0)
        self.yData_before_ave = []
        for i in range(1024):
            self.yData_before_ave.append(0)
        self.cont_sty_max = 1
        self.cont_sty_ave = 0
        self.show_fft = 1
        self.show_ave = 1
        self.change_sweep = 0

        
    def stop(self):
        self.event.clear()
        
    def Init(self):  ##初始化，只收一帧功率谱帧和异常频点
        while(1):
            self.event.wait()
            try:
                recvFFT=self.recvHardObj.ReceiveFFT()
                if(isinstance(recvFFT,SpecDataRecv)):
                    if(recvFFT.CurSectionInTotal==1):
                        FuncPara=recvFFT.CommonHeader.FunctionPara
                        self.SweepTotalNum=recvFFT.SweepSectionTotalNum
                        startSectionNo=recvFFT.CurSectionNo
                        if( isinstance(self.mainframe.SpecFrame,Spectrum_1.Spec )):
                            if(self.mainframe.FreqMax==5995):
                                self.SetTicksLable(FuncPara,startSectionNo)
    
                        if(FuncPara==0x56 or FuncPara==0x51):
                            self.SweepRange.append(recvFFT)
                            
                            recvAb=self.recvHardObj.ReceiveAb()
                            if(not recvAb==0):   
                                self.SweepRangeAb.append(recvAb)
                        else:
                            self.SweepRangeBack.append(recvFFT)
                        break
                else:
                    pass
            except usb.core.USBError:
                print 'time out0'
                   
            
                

    def run(self):
        self.Init() 
        while(1):
            self.event.wait()
            try:
                
                recvFFT=self.recvHardObj.ReceiveFFT()   ##收一个功率谱帧,一个异常频点
                if(isinstance(recvFFT,SpecDataRecv)):
                    # print '0000xxxxxxx0000000'
                    funcPara=recvFFT.CommonHeader.FunctionPara
                    self.SweepTotalNum=recvFFT.SweepSectionTotalNum

                    if (not self.change_sweep==self.SweepTotalNum):
                        self.cont_sty_ave = 0
                        self.cont_sty_max = 1
                        
                    

                    if(funcPara==0x51 or funcPara==0x56):
                        self.SweepRange.append(recvFFT)
                        
                        recvAb=self.recvHardObj.ReceiveAb()    
                        if(not recvAb==0):
                            self.SweepRangeAb.append(recvAb)
                        
                    else:
                        self.SweepRangeBack.append(recvFFT)

                    
                    if(recvFFT.CurSectionInTotal==self.SweepTotalNum):   ##如果当前总数到达总数.看列表里是不是总数
                        if(funcPara==0x51 or funcPara==0x56):
                            if(len(self.SweepRange)==self.SweepTotalNum):
                                # self.count_for_test+=1
                                # if(self.count_for_test%500==0):
                                #     print self.count_for_test

                                ##仅仅是在点了上传或者下载后加入队列，不做其他操作########
                                self.FileToQueue()
                                if( isinstance(self.mainframe.SpecFrame,Spectrum_1.Spec )):
                                    self.DrawAndShowAb(funcPara)
                                    
                                           
                            self.SweepRange=[]
                            self.SweepRangeAb=[]
                        
                        else:


                            if(len(self.SweepRangeBack)==self.SweepTotalNum):
                                if( isinstance(self.mainframe.SpecFrame,Spectrum_1.Spec )):
                                    self.DrawBack(funcPara)
                            self.SweepRangeBack=[]

                elif(isinstance(recvFFT,PoaData)):
                    self.SweepRange=[]
                    self.SweepRangeAb=[]
                    self.SweepRangeBack=[]

                    self.count_for_abNum+=recvFFT.AbNum
                    self.contain_poa.append(recvFFT)
                    if(recvFFT.CurSectionNo == recvFFT.SweepTotalNum):
                        if(len(self.contain_poa)==recvFFT.SweepTotalNum):
                            if(self.count_for_abNum):
                                # if(self.queuePoa._qsize()<16):
                                #     self.queuePoa.put(self.contain_poa)
                                self.savePoa()


                        self.count_for_abNum=0
                        self.contain_poa=[]




            except usb.core.USBError:
                print 'time out1'
            
    def savePoa(self):


        list_for_ab = []

        count_ab = 0

        for recvPoa in self.contain_poa:
            for i in range(recvPoa.AbNum):
                list_for_ab.extend(bytearray(recvPoa.AbBlock[i]))
            count_ab += recvPoa.AbNum

        ###组合POA 文件 时间 ####

        Time = self.contain_poa[0].Time
        CommonHeader = self.contain_poa[0].CommonHeader
        ID = (CommonHeader.HighDeviceID << 8) + CommonHeader.LowDeviceID
        Year = (Time.HighYear << 4) + Time.LowYear
        Month = Time.Month
        Day = Time.Day
        Hour = (Time.HighHour << 2) + Time.LowHour + 8
        Minute = Time.Minute
        Second = Time.Second

        if (not Year == 2016):
            curTime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
            Year = int(curTime[0:4])
            Month = int(curTime[4:6])
            Day = int(curTime[6:8])
            Hour = int(curTime[8:10])
            Minute = int(curTime[10:12])
            Second = int(curTime[12:14])

        ID = staticVar.getid()

        count = (self.contain_poa[0].SecondCount[0] << 24) + \
                (self.contain_poa[0].SecondCount[1] << 16) + \
                (self.contain_poa[0].SecondCount[2] << 8) + \
                (self.contain_poa[0].SecondCount[3])

        list1 = [str(Month), str(Day), str(Hour), str(Minute), str(Second)]
        for i in range(5):
            if (len(list1[i]) == 1):
                list1[i] = '0' + list1[i]

        fileName = str(Year) + "-" + list1[0] + "-" + list1[1] + \
                   "-" + list1[2] + "-" + list1[3] + \
                   "-" + list1[4] + '-' + str(count) + '-' + str(ID) + \
                   '.poa'



        ##### 经纬度 ############
        LonLat = self.contain_poa[0].LonLatAlti

        fid = open(".\LocalData\\Poa\\" + fileName, 'wb')
        d = dict(LonLat=LonLat, count_ab=count_ab,list_for_ab=list_for_ab)
        pickle.dump(d, fid)
        fid.close()

    def DrawAndShowAb(self,funcPara):
        self.SweepCount+=1
        if(self.SweepCount>=self.DrawIntv):
            self.SweepCount=0
            yData=self.ExtractPoint(self.SweepRange)
            # yData = self.change_unit(self.xx, yData_before)
            
            if self.show_fft == 1:
                self.DrawSpec(funcPara,yData)
                
            
            show_select = self.mainframe.SpecFrame.panelFigure.show_box.GetSelection()

            if show_select == 0 :
                self.DrawSpec(funcPara,yData)   

            elif show_select == 1 :
                self.change_sweep = self.SweepTotalNum
                if self.cont_sty_max :
                    self.yData_before = yData
                    self.cont_sty_max = 0
                yData_sty_max = self.FindMax(yData)
                self.yData_before = yData_sty_max
                self.DrawSpec(funcPara, yData_sty_max)
                self.show_fft = 0
            
            elif show_select == 2 :
                yData_sty_min = self.FindMin(yData)
                self.yData_before = yData_sty_min
                self.DrawSpec(funcPara, yData_sty_min)
                self.show_fft = 0
                      
            elif show_select == 3 :
                self.change_sweep = self.SweepTotalNum
                if self.show_ave :
                    self.yData_before_ave = yData
                    self.show_ave = 0  
                yData_sty_ave = self.FindAve(yData)
                self.cont_sty_ave += 1
                #print self.cont_sty_ave
                self.yData_before_ave = yData_sty_ave
                self.DrawSpec(funcPara, yData_sty_ave)
                self.show_fft = 0
                
            self.ShowToji(yData)
            self.DrawWater(yData)
            # for recvAb in self.SweepRangeAb:
            #     if(not recvAb.AbFreqNum==0):
            #         self.ShowAb(recvAb)
            self.ShowAllAb()
            if(press_hand.press_hand==1):
                staticVar.outPoint.write(press_hand.press_set)
                staticVar.outPoint.write(press_hand.press_freq)
    
    def FindMax(self,yData): 
        yData_sty_max = []
        for i in range(1024):
            if self.yData_before[i] > yData[i]:
                yData_sty_max.append(self.yData_before[i])
            else :
                yData_sty_max.append(yData[i])
        return yData_sty_max
                
            
    def FindMin(self,yData):
        yData_sty_min = []
        for i in range(1024):
            if self.yData_before[i] < yData[i]:
                yData_sty_min.append(self.yData_before[i])
            else :
                yData_sty_min.append(yData[i])
        return yData_sty_min
    
    
    def FindAve(self,yData):
        yData_sty_ave = [] 
        for i in range(1024):
            yData_sty_ave.append((yData[i] + self.yData_before_ave[i] * self.cont_sty_ave)/(self.cont_sty_ave + 1))   
        return yData_sty_ave
        
    def DrawBack(self,funcPara):
        self.SweepBackCount+=1
        if(self.SweepBackCount>=self.DrawBackIntv):
            self.SweepBackCount=0
            yData =self.ExtractPoint(self.SweepRangeBack)
            # yData = self.change_unit(self.xx, yData_before)
            self.DrawSpec(funcPara,yData)

    def FileToQueue(self):
        if(not len(self.SweepRange)==len(self.SweepRangeAb)):
            return

        if( isinstance(self.mainframe.SpecFrame,Spectrum_1.Spec )):
          
            if(self.queueFFTUpload._qsize()<16 ):
               
                if((self.mainframe.SpecFrame.panelFigure.getstartUploadOnce()) and (staticFileUp.getUploadMode()==0)):

                    self.queueFFTUpload.put_nowait(self.SweepRange)
                    self.queueAbUpload.put_nowait(self.SweepRangeAb)
                    
                    self.mainframe.SpecFrame.panelFigure.restore2unstart()
                    
                elif(staticFileUp.getUploadMode()):
                
                    self.queueFFTUpload.put_nowait(self.SweepRange)
                    self.queueAbUpload.put_nowait(self.SweepRangeAb)

                
                else:
                    pass 

                Log.getLogger().debug("Cur queueFFTUpload: %s, AbUpload: %s"%(self.queueFFTUpload._qsize(),self.queueAbUpload._qsize()) )

                    
            if(self.queueFFTLocalSave.qsize()<=10):
                if(self.mainframe.SpecFrame.panelFigure.getisDownLoad()):
                    self.queueFFTLocalSave.put_nowait(self.SweepRange)
                    self.queueAbLocalSave.put_nowait(self.SweepRangeAb)
                    
            if((not self.mainframe.thread_route_map==0) and self.mainframe.queueRouteMap.qsize()<=100):
                if(self.mainframe.thread_route_map.event.isSet()):
                    recvFFT=self.SweepRange[0]
                    
                    ###### 解析 经纬高 ##############
                    LonLatClass=recvFFT.LonLatAlti
                    fen=(LonLatClass.HighLonFraction >> 2) +float(((LonLatClass.HighLonFraction&0x03)<<8)+ LonLatClass.LowLonFraction)/1000
                    Lon=LonLatClass.LonInteger+float(fen)/60
            
                    fen = (LonLatClass.HighLatFraction >> 2) + float(((LonLatClass.HighLatFraction & 0x03)<<8) + LonLatClass.LowLatFraction) / 1000
                    Lat = LonLatClass.LatInteger + float(fen) / 60
               
                    self.mainframe.queueRouteMap.put_nowait([Lon,Lat])
                
                
                   
# 这里是用来自动判别的，每次关了软件再上传
    def SetTicksLable(self,FuncPara,startSectionNo):
        if(FuncPara==0x51 or FuncPara==0x52):
            endSectionNo=startSectionNo+self.SweepTotalNum-1
            begin=70+(startSectionNo-1)*25
            end=70+endSectionNo*25
            
        elif(FuncPara==0x56 or FuncPara==0x57):
            endSectionNo=startSectionNo+32*self.SweepTotalNum
            begin=70+(startSectionNo-1)*25
            end=70+(endSectionNo-1)*25

            print end


        ###设置线条的xdata################
        self.xx = linspace(begin, end, 1024)
        self.mainframe.SpecFrame.panelFigure.lineSpec.set_xdata(self.xx)
        self.mainframe.SpecFrame.panelFigure.lineSpecBack.set_xdata(self.xx)
        
        ##设置显示范围（包括文本框和Label）####################
        self.mainframe.FreqMin=begin
        self.mainframe.FreqMax=end 
        self.mainframe.SpecFrame.panelFigure.Min_X.SetLabel(str(begin))
        self.mainframe.SpecFrame.panelFigure.Max_X.SetLabel(str(end))

        self.mainframe.SpecFrame.panelFigure.setSpLabel(begin,end)

                
    def DrawSpec(self,funcPara,yData):
        
        try:
            self.mainframe.SpecFrame.panelFigure.PowerSpectrum(funcPara,yData)
        except wx.PyDeadObjectError:
            pass 
    

    def DrawWater(self,yData):
        try:
            if(not self.mainframe.WaterFrame==None):
                self.mainframe.WaterFrame.WaterFall(yData)
            
        except wx.PyDeadObjectError:
            self.mainframe.WaterFrame=None
            pass 

    
    def ParseFFTList(self,SweepRange):
        # parseResult=[]
        FFTList=[]
        for recvFFT in SweepRange:
            #print 'No',recvFFT.CurSectionNo
            # FFTList=[]
            AllFreq=recvFFT.AllFreq
            ii=0
            for FFTData in AllFreq:
                HighFreq1=FFTData.HighFreq1dB
                LowFreq1=FFTData.LowFreq1dB
                HighFreq2=FFTData.HighFreq2dB
                LowFreq2=FFTData.LowFreq2dB
                if(HighFreq1>=8):
                    FFTFreq1=-(2**12-(HighFreq1<<8)-LowFreq1)/8.0
                else:
                    FFTFreq1=((HighFreq1<<8)+LowFreq1)/8.0
                if(HighFreq2>=8):
                    FFTFreq2=-(2**12-(HighFreq2<<8)-LowFreq2)/8.0
                else:
                    FFTFreq2=((HighFreq2<<8)+LowFreq2)/8.0
                if(recvFFT.CommonHeader.FunctionPara==0x51):
                    pass
                    # print ii*2,FFTFreq1
                    # print ii*2+1,FFTFreq2

                ii=ii+1
                FFTList.append(FFTFreq1)
                FFTList.append(FFTFreq2)
            # parseResult.append(FFTList)
        return FFTList
                
    def ExtractPoint(self,SweepRange):
        allFreq=self.ParseFFTList(SweepRange)
        #if(SweepRange[0].CommonHeader.FunctionPara==0x57):
            #for i in allFreq[0]:
              #  print i
           # print0
           # print 

        # index_s=0
        # index_e=0

        # if(self.mainframe.FreqMax<5995):
        #     freq_s=self.mainframe.FreqMin
        #     freq_e= self.mainframe.FreqMax
        #     index_s = int((freq_s-(70+(freq_s-70)/25*25))/25.0*1024)
        #     index_e = int((freq_e-(70+(freq_e-70)/25*25))/25.0*1024)

        # allFreq=allFreq[index_s:len(allFreq)-index_e]

        yData = []
        ExtractM = len(allFreq) / 1024
        Section = 1024

        for i in xrange(Section):
            Sum=0
            for j in xrange(ExtractM):
                Sum+=math.pow(10,(allFreq[j+i*ExtractM])/10.0)
            Sum=(math.log10(Sum*(10**10))-10)*10
            yData.append(round(Sum,2))


        return yData[0:1024]

    def ParseAb(self,recvAbList):
        AllAbFreq=recvAbList.AllAbFreq
        CurSectionNo=recvAbList.CurSectionNo
        funcPara=recvAbList.CommonHeader.FunctionPara
        AbNum=recvAbList.AbFreqNum

        # if AbNum==0:  ### 清空 如果有 ####
        #     if(not self.mainframe.SpecFrame.panelAbFreq.GetItem(0,1).GetText()==""):
        #         for i in range(10):
        #             self.mainframe.SpecFrame.panelAbFreq.SetStringItem(i,1,"")
        #             self.mainframe.SpecFrame.panelAbFreq.SetStringItem(i,2,"")
        f_list=[]
        db_list=[]

        for j in range(AbNum):
            HighFreqNo=AllAbFreq[j].HighFreqNo
            LowFreqNo=AllAbFreq[j].LowFreqNo
            HighdB=AllAbFreq[j].HighdB
            LowdB=AllAbFreq[j].LowdB
    
            FreqNo=(HighFreqNo<<8)+LowFreqNo
            if(funcPara==0x53):
                Freq=70+(CurSectionNo-1)*25+ float(FreqNo*25)/1024
            else:
                Freq=70+(CurSectionNo-1)*25+ float(FreqNo*800)/1024    
            
            if(HighdB>=8):
                dB=-(2**12-(HighdB<<8)-LowdB)/8.0
            else:
                dB=((HighdB<<8)+LowdB)/8.0

            f_list.append(Freq)
            db_list.append(dB)
            # self.mainframe.SpecFrame.panelAbFreq.SetStringItem(i,1,str('%0.2f'%Freq))
            # self.mainframe.SpecFrame.panelAbFreq.SetStringItem(i,2,str(dB))
            #
        return (f_list,db_list)

    def ShowAllAb(self):
        list_all_f=[]
        list_all_db=[]
        for recvAb in self.SweepRangeAb:
            if(not recvAb.AbFreqNum==0):
                f_list,db_list=self.ParseAb(recvAb)
                list_all_f.extend(f_list)
                list_all_db.extend(db_list)
        if(len(list_all_f)):
            for i in range(len(list_all_f)):
                self.mainframe.SpecFrame.panelAbFreq.SetStringItem(i, 1, str('%0.2f' % list_all_f[i]))
                self.mainframe.SpecFrame.panelAbFreq.SetStringItem(i,2,str(list_all_db[i]))

            for j in range(i,200,1):
                self.mainframe.SpecFrame.panelAbFreq.SetStringItem(j, 1, ' ')
                self.mainframe.SpecFrame.panelAbFreq.SetStringItem(j, 2,' ')
        else:
            if (not self.mainframe.SpecFrame.panelAbFreq.GetItem(itemId=0, col=1).GetText() == " "):
                for i in range(200):
                    if (not self.mainframe.SpecFrame.panelAbFreq.GetItem(itemId=i, col=1).GetText() == " "):
                        self.mainframe.SpecFrame.panelAbFreq.SetStringItem(i,1," ")
                        self.mainframe.SpecFrame.panelAbFreq.SetStringItem(i,2," ")

    def change_unit(self,xData,yData):
        yData_c = []
        for i in range(1024):
            yData_c.append(80 + 20 * math.log10(xData[i]) + yData[i])
        return yData_c

    def ShowToji(self,yData):
        try:
            if(not self.mainframe.TojiFrame==None):

                self.mainframe.TojiFrame.Tongji(self.xx,yData)
        except wx.PyDeadObjectError:
            self.mainframe.WaterFrame=None
            pass
