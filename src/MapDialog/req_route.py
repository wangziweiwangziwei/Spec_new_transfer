# -*- coding: utf-8 -*- 
from src.Package.package import ReqElecPath,FrameHeader,FrameTail,Time
from src.CommonUse.staticVar import staticVar
from src.Thread.thread_route_map import InsertRouteThread

import time 
import  wx
class ReqElecPathDialog(wx.Dialog):
    def __init__(self,parent):
        wx.Dialog.__init__(self,None,-1,u"电磁路径分布数据请求",size=(400,650))

        self.SetFont(wx.Font(10, wx.ROMAN, wx.NORMAL, wx.LIGHT, underline=False, faceName=u"微软雅黑",
                             encoding=wx.FONTENCODING_DEFAULT))

        panel=wx.Panel(self,-1)
        
        ###############################
        self.parent=parent 
        self.tail=FrameTail(0,0,0xAA)
        
        self.id=staticVar.getid()
        self.lowid=self.id&0x00FF
        self.highid=self.id>>8
        
        self.List=staticVar.getCentreFreq()
        self.ListFreq=staticVar.getFreq()
        ###############################################
        self.radioBox1=wx.RadioBox(panel,-1,choices=[u"本地获取",u"中心站获取"],style=wx.RA_VERTICAL)
        self.radioBox2=wx.RadioBox(panel,-1,choices=[u"显示历史分布",u"显示实时分布"],style=wx.RA_VERTICAL)
        self.radioBox3=wx.RadioBox(panel,-1,choices=[u"选择频率",u"手动频率"])
        self.radioBox4=wx.RadioBox(panel,-1,choices=[u"YES",u"NO"])
        
        self.radioBox1.SetSelection(1)
        self.radioBox2.SetSelection(1)
        self.radioBox3.SetSelection(1)
        self.radioBox4.SetSelection(1)
        self.FreqSection=wx.ComboBox(panel,-1,u"FM调频广播频段",choices=self.List)
        self.FreqSection.SetSelection(0)
        self.CentreFreq=wx.TextCtrl(panel,-1,size=(80,25))
        self.BandWidth=wx.TextCtrl(panel,-1,size=(80,25))
        
        #############################################
        curTime=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
        Year=int(curTime[0:4])
        Month=int(curTime[4:6])
        Day=int(curTime[6:8])
        Hour=int(curTime[8:10])
        Min=int(curTime[10:12])+2
        
        
        ###############################################

        self.StartTimeYear=wx.ComboBox(panel,-1,str(Year),choices=["2015","2016","2017","2018"])
        self.StartTimeMonth=wx.ComboBox(panel,-1,str(Month),choices=["1","2","3","4","5","6","7","8","9","10","11","12"])
        self.StartTimeDay=wx.TextCtrl(panel,-1,str(Day),size=(60,25))
        self.StartTimeHour=wx.TextCtrl(panel,-1,str(Hour),size=(60,25))
        self.StartTimeMinute=wx.TextCtrl(panel,-1,str(Min),size=(60,25))

        self.EndTimeYear=wx.ComboBox(panel,-1,str(Year),choices=["2015","2016","2017","2018"])
        self.EndTimeMonth=wx.ComboBox(panel,-1,str(Month),choices=["1","2","3","4","5","6","7","8","9","10","11","12"])
        self.EndTimeDay=wx.TextCtrl(panel,-1,str(Day),size=(60,25))
        self.EndTimeHour=wx.TextCtrl(panel,-1,str(Hour),size=(60,25))
        self.EndTimeMinute=wx.TextCtrl(panel,-1,str(Min),size=(60,25))


        sizer=wx.BoxSizer(wx.VERTICAL)
        sizer.Add((15,15))
        sizer.Add(self.radioBox3,0,wx.LEFT,20)
        sizer.Add(self.FreqSection,0,wx.LEFT|wx.TOP,20)

        sizer.Add((10,10))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(wx.StaticText(panel,-1,u"中心频率(MHz)",size=(100,25)),0,wx.LEFT,20)
        hBox1.Add(self.CentreFreq,0,wx.LEFT,20)
        sizer.Add(hBox1)
        
        sizer.Add((10,10))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(wx.StaticText(panel,-1,u"带宽(MHz)",size=(100,25)),0,wx.LEFT,20)
        hBox1.Add(self.BandWidth,0,wx.LEFT,20)
        sizer.Add(hBox1)

        sizer.Add((10,10))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(wx.StaticText(panel,-1,u"分布数据来源：",size=(100,25)),0,wx.LEFT|wx.ALIGN_TOP,20)
        hBox1.Add(self.radioBox1,0,wx.LEFT|wx.ALIGN_TOP,20)
        sizer.Add(hBox1)
        
        sizer.Add((10,10))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(wx.StaticText(panel,-1,u"T-POA定位：",size=(100,25)),0,wx.LEFT|wx.ALIGN_TOP,20)
        hBox1.Add(self.radioBox4,0,wx.LEFT|wx.ALIGN_TOP,20)
        sizer.Add(hBox1)
        
        sizer.Add((10,10))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(wx.StaticText(panel,-1,u"显示数据来源：",size=(100,25)),0,wx.LEFT|wx.ALIGN_TOP,20)
        hBox1.Add(self.radioBox2,0,wx.LEFT|wx.ALIGN_TOP,20)
        sizer.Add(hBox1)
        
        sizer.Add((10,10))
        sizer.Add(wx.StaticText(panel,-1,u"起始时间(年-月-日-时-分)：",size=(160,25)),0,wx.LEFT,20)
        sizer.Add((10,10))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(self.StartTimeYear,0,wx.LEFT,20)
        hBox1.Add(wx.StaticText(panel,-1,"-"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,5)
        hBox1.Add(self.StartTimeMonth,0)
        hBox1.Add(wx.StaticText(panel,-1,"-"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,5)
        hBox1.Add(self.StartTimeDay,0)
        hBox1.Add(wx.StaticText(panel,-1,"-"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,5)
        hBox1.Add(self.StartTimeHour,0)
        hBox1.Add(wx.StaticText(panel,-1,"-"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,5)
        hBox1.Add(self.StartTimeMinute,0)
        sizer.Add(hBox1)

        sizer.Add(wx.StaticText(panel,-1,u"终止时间(年-月-日-时-分)：",size=(160,25)),0,wx.LEFT,20)
        sizer.Add((10,10))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(self.EndTimeYear,0,wx.LEFT,20)
        hBox1.Add(wx.StaticText(panel,-1,"-"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,5)
        hBox1.Add(self.EndTimeMonth,0)
        hBox1.Add(wx.StaticText(panel,-1,"-"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,5)
        hBox1.Add(self.EndTimeDay,0)
        hBox1.Add(wx.StaticText(panel,-1,"-"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,5)
        hBox1.Add(self.EndTimeHour,0)
        hBox1.Add(wx.StaticText(panel,-1,"-"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,5)
        hBox1.Add(self.EndTimeMinute,0)
        sizer.Add(hBox1)
        sizer.Add((30,30))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        self.btn_ok=wx.Button(panel,-1,"OK",size=(60,25))
        
        hBox1.Add(self.btn_ok,0,wx.LEFT,20)
        hBox1.Add(wx.Button(panel,wx.ID_CANCEL,"CANCEL",size=(60,25)),0,wx.LEFT,20)
        sizer.Add(hBox1)
        panel.SetSizer(sizer)
        
        
        self.Layout()
        
        self.Centre( wx.BOTH )
        
        #Events
        self.Bind(wx.EVT_RADIOBOX, self.OnRadio,self.radioBox3)
        self.btn_ok.Bind(wx.EVT_BUTTON, self.OnbtnOk)
        self.FreqSection.Enable(False)
        self.CentreFreq.Enable(True)
        self.BandWidth.Enable(True)
        
        
    def ByteToTime(self,time):
        Obj=Time()
        Obj.HighYear=time[0]>>4
        Obj.LowYear=time[0]&0x00F
        Obj.Month=time[1]
        Obj.Day=time[2]
        Obj.HighHour=time[3]>>2
        Obj.LowHour=time[3]&0x03
        Obj.Minute=time[4]
        
        return Obj        
            

    def OnRadio(self,event):
        if(self.radioBox3.GetSelection()==0):
            self.FreqSection.Enable(True)
            self.BandWidth.Enable(False)
            self.CentreFreq.Enable(False)

        elif(self.radioBox3.GetSelection()==1):
            self.FreqSection.Enable(False)
            self.CentreFreq.Enable(True)
            self.BandWidth.Enable(True)
            
    def OnbtnOk(self,event):

        if(self.radioBox1.GetSelection()):
            reqElec=ReqElecPath()
            reqElec.CommonHeader=FrameHeader(0x55,0xA3,self.lowid,self.highid)
            reqElec.CommonTail=self.tail
        
            reqElec.DataSource=15
            
            if(self.radioBox3.GetSelection()==0):
                centreFreq=self.ListFreq[self.FreqSection.GetSelection()][0]
                bandWidth=self.ListFreq[self.FreqSection.GetSelection()][1]
            else:
                centreFreq=int(self.CentreFreq.GetValue())
                bandWidth=int(self.BandWidth.GetValue())
            
            if(self.radioBox4.GetSelection()==0):
                reqElec.TPOA=0xFF
                
            reqElec.HighCentreFreq=centreFreq>>8
            reqElec.LowCentreFreq=centreFreq&0x00FF
            reqElec.BandWidth=bandWidth
    
            startTime=(int(self.StartTimeYear.GetValue()),int(self.StartTimeMonth.GetValue()),  \
                       int(self.StartTimeDay.GetValue()),int(self.StartTimeHour.GetValue()),    \
                       int(self.StartTimeMinute.GetValue())
                       )
            endTime=(int(self.EndTimeYear.GetValue()),int(self.EndTimeMonth.GetValue()),  \
                       int(self.EndTimeDay.GetValue()),int(self.EndTimeHour.GetValue()),    \
                       int(self.EndTimeMinute.GetValue())
                       )
            
            reqElec.StartTime=self.ByteToTime(startTime)
            reqElec.EndTime=self.ByteToTime(endTime)
            #
            # if(staticVar.getSock()):
            #     staticVar.getSock().sendall(bytearray(reqElec))

            self.parent.queueRequest.put(reqElec)
            
        else:
            if(self.parent.thread_route_map==0):
                self.parent.thread_route_map=InsertRouteThread(self.parent)
                self.parent.thread_route_map.start()
            else:
                self.parent.thread_route_map.event.set()
            
        self.Close()
    
    
        
        
        
        
        
        
