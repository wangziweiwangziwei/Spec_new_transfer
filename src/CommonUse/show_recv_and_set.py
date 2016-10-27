#coding=utf-8
class ShowRecvAndSet():
    def __init__(self,mainframe):
        self.sampleList = [u"超短套筒天线",u"超短螺旋天线",u"单鞭螺旋天线",u"平面双锥天线",u"AH-8000",u"AH-7000", \
                  u"TQJ-1000",u"国人对数",u"汇讯通对数",u"BTA-BicoLog",u"LX-520",u"LX-840",u"LX-1080"]
        
        self.SpecFrame=mainframe.SpecFrame
    def DisplayResponse(self,recvData):
        functionPara=recvData.CommonHeader.FunctionPara
        if(functionPara==0x21):     
            self.ShowSweepRange(recvData)
        elif(functionPara==0x22):
            self.ShowIQCentreFreq(recvData)
        elif(functionPara==0x23):
            self.ShowPressFreq(recvData)
        elif(functionPara==0x24):
            self.ShowRecvGain(recvData)
        elif(functionPara==0x25):
            self.ShowSendWeak(recvData)
        elif(functionPara==0x26):
            self.ShowTestGate(recvData)
        elif(functionPara==0x27):
            self.ShowIQPara(recvData) 
        elif(functionPara==0x28):
            self.ShowPressPara(recvData)
        elif(functionPara==0x29):
            self.ShowAccessWay(recvData)
        elif(functionPara==0x2A):
            self.ShowTransferOpen(recvData)
        elif(functionPara==0x2B):
            self.ShowTransferClose(recvData)
        elif(functionPara==0x2C):
            self.ShowIsConnect(recvData)
        elif(functionPara==0x2D):
            self.ShowCorrGain(recvData)
        elif(functionPara==0x2E):
            self.ShowAntGain(recvData)
        else:
            pass
    def ShowCorrGain(self,recvQueryData):
        AntType=(recvQueryData.AntType[0]<<8)+(recvQueryData.AntType[1])
        AntTypeString=self.sampleList[AntType-1]
        
        FreqArray=recvQueryData.Freq
        FreqStart=[0,0,0]
        FreqEnd=[0,0,0]
        CorrValue=[]
        for i in range(3):
            FreqStart[i]=(FreqArray[i*4]<<8)+FreqArray[i*4+1]
            FreqEnd[i]=(FreqArray[i*4+2]<<8)+FreqArray[i*4+3]
        
        for data in recvQueryData.CorrValue:
            CorrValue.append(data)
         
        dictFreq={
        u'硬件型号':AntTypeString,
        u"StartFreq1(MHz)": str('%0.2f'%FreqStart[0]),
        u"StartFreq2(MHz)": str('%0.2f'%FreqStart[1]),
        u"StartFreq3(MHz)": str('%0.2f'%FreqStart[2]),
        u"EndFreq1(MHz)": str('%0.2f'%FreqEnd[0]),
        u"EndFreq2(MHz)": str('%0.2f'%FreqEnd[1]),
        u"EndFreq3(MHz)": str('%0.2f'%FreqEnd[2])
        }
        for i in xrange(237):
            dictFreq["CorrGain"+str(i+1)]=str(CorrValue[i])
        self.Show(244,u"GainCorrect",dictFreq)
        
    def ShowAntGain(self,recvQueryData):
        self.ShowCorrGain(recvQueryData)
    def ShowSweepRange(self,recvQueryData):
        i=0
        while(i<45):
            self.SpecFrame.panelQuery.SetStringItem(i,0,'')
            self.SpecFrame.panelQuery.SetStringItem(i,1,'')
            self.SpecFrame.panelQuery.SetStringItem(i,2,'')
            i=i+1
        SweepRecvMode=u"指定频段"
        if(recvQueryData.SweepRecvMode==1):
            SweepRecvMode=u"全频段"
        elif(recvQueryData.SweepRecvMode==2):
            SweepRecvMode=u"指定频段"
        elif(recvQueryData.SweepRecvMode==3):
            SweepRecvMode=u"多频段"

        begin = 70 + (recvQueryData.StartSectionNo - 1) * 25 + \
                ((recvQueryData.HighStartFreq << 8) + (recvQueryData.LowStartFreq)) * 25.0 / 1024
        end = 70 + (recvQueryData.EndSectionNo - 1) * 25 + \
              ((recvQueryData.HighEndFreq << 8) + (recvQueryData.LowEndFreq)) * 25.0 / 1024


        list_p=[(u"扫频模式",SweepRecvMode),
                (u"起始频率",str(int(round(begin)))),
                (u"终止频率",str(int(round(end))))
                   ]
        for i in range(3):

            self.SpecFrame.panelQuery.SetStringItem(i,0,u"扫频")
            self.SpecFrame.panelQuery.SetStringItem(i,1,list_p[i][0])
            self.SpecFrame.panelQuery.SetStringItem(i,2,list_p[i][1])

        # if(recvQueryData.SweepRecvMode==3):
        #     self.ShowMutiSweep(8,u"扫频",dictSweep)
        # else:
        #     self.Show(8,u"扫频",dictSweep)
    def ShowMutiSweep(self,lendict,string,dic):
        CurNo=int(dic[u"当前频段序号"])
        keys=dic.keys()
        for i in range(lendict):
            self.SpecFrame.panelQuery.SetStringItem(i+9*(CurNo-1) ,0,string)
            self.SpecFrame.panelQuery.SetStringItem(i+9*(CurNo-1) ,1,keys[i])
            self.SpecFrame.panelQuery.SetStringItem(i+9*(CurNo-1) ,2,dic[keys[i]])


    def ShowIQCentreFreq(self,recvQueryData,len=10):
        FreqArray=recvQueryData.FreqArray
        Freq=[0,0,0]
        for i in range(3):
            Freq[i]=(FreqArray[i].HighFreqInteger<<6)+FreqArray[i].LowFreqInteger  \
             +float((FreqArray[i].HighFreqFraction<<8)+FreqArray[i].LowFreqFraction)/2**10

        dictIQFreq={
        u"定频频点个数":str(recvQueryData.FreqNum),
        u"频率值1(MHz)": str('%0.2f'%Freq[0]),
        u"频率值2(MHz)": str('%0.2f'%Freq[1]),
        u"频率值3(MHz)": str('%0.2f'%Freq[2])
        }
        self.ShowBelow(4,u"定频",dictIQFreq,len)


    def ShowIQPara(self,recvQueryData):
        DataRate=recvQueryData.DataRate
        if(DataRate==0x01):DataRate=5
        elif(DataRate==0x02): DataRate=2.5
        elif(DataRate==0x03):DataRate=1
        elif(DataRate==0x04):DataRate=0.5
        elif(DataRate==0x05): DataRate=0.1

        Time=recvQueryData.Time
        dictIQPara={
        u"数据率(MHz)": str(DataRate),
        u"数据块个数": str(recvQueryData.UploadNum),
        u"定频时间" : str((Time.HighYear<<4)+Time.LowYear)+'.'+ \
                  str(Time.Month)+'.'+str(Time.Day)+'.'+ \
                  str((Time.HighHour<<2)+Time.LowHour)+'.'+str(Time.Minute)+'.'+str(Time.Second)

        }
        self.Show(3,u"定频",dictIQPara)


    def ShowPressFreq(self,recvQueryData,len=10): #len 表示第几行显示
        FreqArray=recvQueryData.FreqArray
        Freq=[0,0]
        for i in range(2):
            Freq[i]=(FreqArray[i].HighFreqInteger<<6)+FreqArray[i].LowFreqInteger   \
             +float((FreqArray[i].HighFreqFraction<<8)+FreqArray[i].LowFreqFraction)/2**10
          
        dictPressFreq={
        u"定频频点个数":str(recvQueryData.PressNum),
        u"频率值1(MHz)": str('%0.2f'%Freq[0]),
        u"频率值2(MHz)": str('%0.2f'%Freq[1])
        }
        self.ShowBelow(3,u"压制",dictPressFreq,len)

    def ShowPressPara(self,recvQueryData):
        PressMode=recvQueryData.PressMode
        PressSignal=recvQueryData.PressSignal
        
        T1=(recvQueryData.HighT1<<8)+recvQueryData.LowT1
        T2=(recvQueryData.HighT2<<8)+recvQueryData.LowT2
        T3=(recvQueryData.HighT3<<8)+recvQueryData.LowT3
        T4=(recvQueryData.HighT4<<8)+recvQueryData.LowT4

        mapPressMode={1:u"单频点自动",2:u"单频点手动",3:u"双频点自动",4:u"双频点手动",5:u"不压制"}
        mapPressSignal={1:u"单频正弦" ,2:u"等幅多频" ,3:u"噪声低频",4:u"DRM信号"}

        Mode=mapPressMode[PressMode]
        Signal=mapPressSignal[PressSignal]

        dictPressPara={
        u"压制模式":Mode,
        u"信号类型":Signal,
        u"T1":str(T1),
        u"T2":str(T2),
        u"T3":str(T3),
        u"T4":str(T4)
        }
        self.Show(6,u"压制",dictPressPara)

    def ShowRecvGain(self,recvQueryData):
        i = 0
        while (i < 45):
            self.SpecFrame.panelQuery.SetStringItem(i, 0, '')
            self.SpecFrame.panelQuery.SetStringItem(i, 1, '')
            self.SpecFrame.panelQuery.SetStringItem(i, 2, '')
            i = i + 1

        recvGain=recvQueryData.RecvGain-3
        self.SpecFrame.panelQuery.SetStringItem(0,1,u"接收增益(dB)")
        self.SpecFrame.panelQuery.SetStringItem(0,2,str(recvGain))

    def ShowSendWeak(self,recvQueryData):
        i = 0
        while (i < 45):
            self.SpecFrame.panelQuery.SetStringItem(i, 0, '')
            self.SpecFrame.panelQuery.SetStringItem(i, 1, '')
            self.SpecFrame.panelQuery.SetStringItem(i, 2, '')
            i = i + 1

        sendWeak=recvQueryData.SendWeak 
        self.SpecFrame.panelQuery.SetStringItem(0,1,u"发射衰减(dB)")
        self.SpecFrame.panelQuery.SetStringItem(0,2,str(sendWeak))
    def ShowTestGate(self,recvQueryData):
        mapAdapt={
        0:3,1:10,2:20,3:25,4:30,5:40
        }

        i = 0
        while (i < 45):
            self.SpecFrame.panelQuery.SetStringItem(i, 0, '')
            self.SpecFrame.panelQuery.SetStringItem(i, 1, '')
            self.SpecFrame.panelQuery.SetStringItem(i, 2, '')
            i = i + 1

        if(recvQueryData.ThresMode==0):
            AdaptThres=mapAdapt[recvQueryData.AdaptThres]
            self.SpecFrame.panelQuery.SetStringItem(0,1,u"自适应门限")
            self.SpecFrame.panelQuery.SetStringItem(0,2,str(AdaptThres))

        else:
            FixedThres=(recvQueryData.HighFixedThres<<8)+recvQueryData.LowFixedThres
            self.SpecFrame.panelQuery.SetStringItem(0,1,u"固定门限")
            self.SpecFrame.panelQuery.SetStringItem(0,2,str(FixedThres))

    def ShowIsConnect(self,recvQueryData):
        if(recvQueryData.IsConnect==0x0F):
            IsConnect=u"在网"
        else:
            IsConnect=u"不在网"
        mapTerminalType={0:u"专业用户终端",1:u"普通用户终端",2:u"专业查询终端",3:u"普通查询终端"}
        TerminalType=mapTerminalType[recvQueryData.TerminalType]
        LonLatClass=recvQueryData.LonLatAlti
        fen=(LonLatClass.HighLonFraction >> 2) +float(((LonLatClass.HighLonFraction&0x03)<<8)+ LonLatClass.LowLonFraction)/1000
        Lon=LonLatClass.LonInteger+float(fen)/60

        fen = (LonLatClass.HighLatFraction >> 2) + float(((LonLatClass.HighLatFraction & 0x03)<<8) + LonLatClass.LowLatFraction) / 1000
        Lat = LonLatClass.LatInteger + float(fen) / 60
        Altitude=(LonLatClass.HighAltitude<<8)+LonLatClass.LowAltitude

        if(LonLatClass.LonFlag==0):
            LonFlag=u"东经"
        else:
            LonFlag=u"西经"
        if(LonLatClass.LatFlag==0):
            LatFlag=u"北纬"
        else:
            LatFlag=u"南纬"
        if(LonLatClass.AltitudeFlag==0):
            AltitudeFlag=u'海平面上'
        else:
            AltitudeFlag=u'海平面下'

        dictIsConnect={
        u"在网标志":IsConnect,
        u"终端类型":TerminalType,
        u"经度标志":LonFlag,
        u"经度":str('%0.7f'%Lon),
        u"纬度标志":LatFlag,
        u"纬度":str('%0.7f'%Lat),
        u"高度标志":AltitudeFlag,
        u"高度":str(Altitude)
        }
        self.Show(8,u"终端状态",dictIsConnect)

    def ShowAccessWay(self,recvQueryData):
        AccessWay=recvQueryData.AccessWay
        if(AccessWay==1):AccessWay='WiFi'
        elif(AccessWay==2):AccessWay='BlueTooth'
        elif(AccessWay==3):AccessWay='USB'
        self.SpecFrame.panelQuery.SetStringItem(0,1,u"硬件接入方式")
        self.SpecFrame.panelQuery.SetStringItem(0,2,AccessWay)
        
    def ShowTransferOpen(self,recvQueryData):
        self.SpecFrame.panelQuery.SetStringItem(0,0,u"硬件传输开启")
    def ShowTransferClose(self,recvQueryData):
        self.SpecFrame.panelQuery.SetStringItem(0,0,u"硬件传输关闭")
    
    def Show(self,lendict,string,dic):
        i=0
        while(i<45):
            self.SpecFrame.panelQuery.SetStringItem(i,0,'')
            self.SpecFrame.panelQuery.SetStringItem(i,1,'')
            self.SpecFrame.panelQuery.SetStringItem(i,2,'')
            i=i+1
    
        keys=dic.keys()
        for i in range(lendict):
            self.SpecFrame.panelQuery.SetStringItem(i,0,string)
            self.SpecFrame.panelQuery.SetStringItem(i,1,keys[i])
            self.SpecFrame.panelQuery.SetStringItem(i,2,dic[keys[i]])
            
    def ShowBelow(self,lendict,string,dic,len=10):
        
        keys=dic.keys()
        for i in range(lendict):
            self.SpecFrame.panelQuery.SetStringItem(len+i,0,string)
            self.SpecFrame.panelQuery.SetStringItem(len+i,1,keys[i])
            self.SpecFrame.panelQuery.SetStringItem(len+i,2,dic[keys[i]])
            
            
                
            
