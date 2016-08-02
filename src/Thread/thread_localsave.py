# -*- coding: utf-8 -*-
import threading 
import time 
from src.Package.package import *

import struct 
from src.CommonUse.staticVar import staticVar
from src.CommonUse.staticFileUpMode import staticFileUp

import os

################ Spec LocalSave  ####################
class LocalSaveThread(threading.Thread): 
    def __init__(self,mainframe ,
                 queueFFTLocalSave,queueAbLocalSave):
        threading.Thread.__init__(self)
        self.event = threading.Event()  
        self.event.set()
        
        self.queueFFTLocalSave=queueFFTLocalSave

        self.queueAbLocalSave=queueAbLocalSave
        self.SpecFrame=mainframe.SpecFrame
        self.WaveFrame=mainframe.WaveFrame
             
        self.SpecList=[]

        
        self.Second=0
        self.countFFT=0

        self.count=1  ##用来计数一秒钟发了多少个功率谱文件
        
        self.dir_spec_origin=""
        self.dir_spec=""      ##存储文件路径

        
        self.startTrans=0

        self.count=0

        ##########################
        if(not os.path.exists("./LocalData//Spec//")):
            os.makedirs('./LocalData//Spec//')




        ##############################
    def stop(self):
        self.event.clear()
    def run(self):
        while(1):
            self.event.wait()
          
            self.SaveSpec()
    

#             print 'queueAbLocalSave.len',self.queueAbLocalSave.qsize()
#             print 'queue FFT',self.queueFFTLocalSave.qsize()
            time.sleep(0.5)
        
    def SaveSpec(self):
        #################  获取窗口值  #################
        self.dir_spec_origin=self.SpecFrame.panelFigure.getDownloadDir()
        #print self.dir_spec_origin
        ##########################################
        
        
        if(not self.dir_spec_origin==""):
            t=os.path.exists(self.dir_spec_origin)
            print t
            if(not os.path.exists(self.dir_spec_origin)):
                os.makedirs(self.dir_spec_origin+'\\Spec\\')
                # os.makedirs(self.dir_spec_origin+'\\IQ\\')
                print 'make dir'
            
            self.dir_spec=self.dir_spec_origin+'\\Spec\\'
            
        else:
            self.dir_spec=".\LocalData\\Spec\\"
            

### 在队列加到一定的时候,如果改变了传输方式要马上改过来
        flag_for_extract=0
        flag_for_auto=0
        self.fileUploadMode=staticFileUp.getUploadMode()
        
        if(self.fileUploadMode):    
            self.extractM=staticFileUp.getExtractM()
            self.changeThres=staticFileUp.getChangeThres()
            
        
        while((not self.queueAbLocalSave.empty()) and (not self.queueFFTLocalSave.empty())):
            if(self.fileUploadMode==0):
                ListSpec=self.queueFFTLocalSave.get()
                ListAb=self.queueAbLocalSave.get()
                self.FFTParse(ListSpec, ListAb)
                
            elif(self.fileUploadMode==2): ##抽取自动
               
                while((not self.queueAbLocalSave.empty()) and (not self.queueFFTLocalSave.empty())):
                    if(staticFileUp.getUploadMode()==2):
                        ListSpec=self.queueFFTLocalSave.get()
                        ListAb=self.queueAbLocalSave.get()
                    else:
                        flag_for_extract=1
                        break 
                    self.count+=1
                    if(self.count==self.extractM):
                        print 'start to save extract----------------'
                        self.count=0
                        self.FFTParse(ListSpec,ListAb)
                if(flag_for_extract):
                    self.count=0
                    break
                        
            elif(self.fileUploadMode==1):  ##功率谱是否变化
                while((not self.queueAbLocalSave.empty()) and (not self.queueFFTLocalSave.empty())):
                    if(staticFileUp.getUploadMode()==1):
                        ListSpec=self.queueFFTLocalSave.get()
                        ListAb=self.queueAbLocalSave.get()
                    else:
                        flag_for_auto=1
                        break
                    flag=0
                    for recvFFT in ListSpec:
                        changeFlag=recvFFT.SpecChangeFlag
                        if(changeFlag==14 or changeFlag==15):
                            flag=1
                            break
                    if(flag==1):
                        print 'start to save for change_flag>>>>>>>>>>>>>>>  '
                        self.FFTParse(ListSpec,ListAb)
                
                if(flag_for_auto):
                    break
                
                    
            
    
    def FFTParse(self,ListSpec,ListAb):    
        for i in range(len(ListSpec)):   
            recvFFT=ListSpec[i]
            recvAbList=ListAb[i]
           
            TotalNum=recvFFT.SweepSectionTotalNum         
            blockFFT=FFTBlock(recvFFT.CurSectionNo,recvFFT.AllFreq)
            blockAb=AbListBlock(recvAbList.CurSectionNo,recvAbList.AbFreqNum,recvAbList.AllAbFreq)
            self.SpecList.append(blockFFT)
            self.SpecList.append(blockAb)
        
        head=SpecUploadHeader(0x00,recvFFT.LonLatAlti,recvFFT.SweepRecvMode, \
        recvFFT.FileUploadMode,staticFileUp.getChangeThres(),staticFileUp.getExtractM(),TotalNum)
            

        ###组合功率谱文件####
        '''
        Time=recvFFT.Time_
        CommonHeader=recvFFT.CommonHeader
        ID=(CommonHeader.HighDeviceID<<8)+CommonHeader.LowDeviceID
        Year=(Time.HighYear<<4)+Time.LowYear
        Month=Time.Month
        Day=Time.Day
        Hour=(Time.HighHour<<2)+Time.LowHour
        Minute=Time.Minute
        Second=Time.Second
        '''

        curTime=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
        Year=int(curTime[0:4])
        Month=int(curTime[4:6])
        Day=int(curTime[6:8])
        Hour=int(curTime[8:10])
        Minute=int(curTime[10:12])
        Second=int(curTime[12:14])
        

        
        ID=staticVar.getid()
        
        if(self.startTrans==0):
            self.Second=Second 
            self.startTrans=1  
        if((self.startTrans==1) and (self.Second!=Second)):
            self.count=1
            self.Second=Second
        fileName=str(Year)+"-"+str(Month)+"-"+str(Day)+  \
                 "-"+str(Hour)+"-"+str(Minute)+"-"+str(Second)+"-"+str(self.count)+'-'+str(ID)
                 
        if(recvFFT.CommonHeader.FunctionPara==0x51):
            fileName+='-fine.pwr'
        else:
            fileName+='-coarse.pwr'
            
        

        fileNameLen=len(fileName)
        fileContentLen=sizeof(head)+(sizeof(blockFFT)+sizeof(blockAb))*TotalNum+2

        print fileName
        print fileNameLen
        print fileContentLen
       
        ##########SaveToLocal#####################
#         fid=open(".\LocalData\\"+ fileName,'wb+')
        fid=open(self.dir_spec+fileName,'wb+')
        fid.write(bytearray(head))
        for i in xrange(len(self.SpecList)/2):
            fid.write(bytearray(self.SpecList[2*i]))
        fid.write(struct.pack("!B",0xFF))
        for i in xrange(len(self.SpecList)/2):
            fid.write(bytearray(self.SpecList[2*i+1])) 
        fid.write(struct.pack("!B",0x00))
        fid.close()
        #########################################
        self.SpecList=[]
        
        self.count+=1
        self.countFFT+=1
        print 'self.countFFT',self.countFFT
            

            
            
            
        
        
                
        
        
        




            



            
