# -*- coding: utf-8 -*- 
import wx
from src.Package.package import ReqAbFreq,FrameHeader,FrameTail
from src.CommonUse.staticVar import staticVar

class ReqAbFreqDialog(wx.Dialog):
    def __init__(self,parent):
        wx.Dialog.__init__(self,parent,-1,u"异常频点定位数据请求",size=(450,400))

        self.SetFont(wx.Font(10, wx.ROMAN, wx.NORMAL, wx.LIGHT, underline=False, faceName=u"微软雅黑",
                             encoding=wx.FONTENCODING_DEFAULT))

        ###############################

        self.parent=parent
        self.tail=FrameTail(0,0,0xAA)
        
        self.id=staticVar.getid()
        self.lowid=self.id&0x00FF
        self.highid=self.id>>8
        
        
        ###############################################
       
       
       
       
        panel=wx.Panel(self,-1)
        self.CentreFreq=wx.TextCtrl(panel,-1,size=(80,25))
        self.UploadNum=wx.TextCtrl(panel,-1,"1",size=(80,25))
        self.radioBox=wx.RadioBox(panel,-1,choices=["POA","POA/TDOA"])
        self.radioBox.SetSelection(0)
        sampleList = ['5/5','2.5/2.5','1/1','0.5/0/5','0.1/0/1']
        self.BandWidth = wx.ComboBox(panel, -1,'5/5',size=(80,30),choices=sampleList)
        self.BandWidth.SetSelection(0)
        self.StartTimeYear=wx.ComboBox(panel,-1,"2015",choices=["2015","2016","2017","2018"])
        self.StartTimeMonth=wx.ComboBox(panel,-1,"12",choices=["1","2","3","4","5","6","7","8","9","10","11","12"])
        self.StartTimeDay=wx.TextCtrl(panel,-1,"1",size=(60,25))
        self.StartTimeHour=wx.TextCtrl(panel,-1,"0",size=(60,25))
        self.StartTimeMinute=wx.TextCtrl(panel,-1,"0",size=(60,25))
        self.StartTimeSecond=wx.TextCtrl(panel,-1,"0",size=(60,25)) 
        self.StartTimeYear.SetSelection(0)
        self.StartTimeMonth.SetSelection(11)

        sizer=wx.BoxSizer(wx.VERTICAL)
        sizer.Add((15,15))
        sizer.Add(wx.StaticText(panel,-1,u"几何定位方法",size=(120,25)),0,wx.LEFT,20)
        sizer.Add(self.radioBox,0,wx.LEFT,20)

        sizer.Add((10,10))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(wx.StaticText(panel,-1,u"中心频率(MHz)",size=(160,25)),0,wx.LEFT,20)
        hBox1.Add(self.CentreFreq,0,wx.LEFT,20)
        sizer.Add(hBox1)

        sizer.Add((10,10))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(wx.StaticText(panel,-1,u"带宽/数据率 (MHz/Msps):",size=(160,25)),0,wx.LEFT,20)
        hBox1.Add(self.BandWidth,0,wx.LEFT,20)
        sizer.Add(hBox1)

        sizer.Add((10,10))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(wx.StaticText(panel,-1,u"上传数据块个数(1-256):",size=(160,25)),0,wx.LEFT,20)
        hBox1.Add(self.UploadNum,0,wx.LEFT,20)
        sizer.Add(hBox1)

        sizer.Add((10,10))
        sizer.Add(wx.StaticText(panel,-1,u"采集起始时间(年-月-日-时-分-秒)："),0,wx.LEFT,20)
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
        hBox1.Add(wx.StaticText(panel,-1,"-"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,5)
        hBox1.Add(self.StartTimeSecond,0)
        sizer.Add(hBox1)

        sizer.Add((30,30))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        self.btn_ok=wx.Button(panel,-1,"OK",size=(60,25))
        
        hBox1.Add(self.btn_ok,0,wx.LEFT,20)
        hBox1.Add(wx.Button(panel,wx.ID_ANY,"CANCEL",size=(60,25)),0,wx.LEFT,20)
        sizer.Add(hBox1)
        panel.SetSizer(sizer)
        
        self.Layout()
        
        self.Centre( wx.BOTH )
        
        #Events
        self.btn_ok.Bind(wx.EVT_BUTTON, self.OnbtnOk)
    
    def OnbtnOk(self,event):
        reqAb=ReqAbFreq()
        reqAb.CommonHeader=FrameHeader(0x55,0xA4,self.lowid,self.highid)
        reqAb.CommonTail=self.tail
        if(self.radioBox.GetSelection()):
            reqAb.LocateWay=0x0F
        centreFreq=float(self.CentreFreq.GetValue())  
        bandWidth=int(self.BandWidth.GetSelection())+1  
        centreFreq_I=int(centreFreq)
        centreFreq_F=int((centreFreq-int(centreFreq))*2**10)
        reqAb.Param.HighCentreFreqInteger=centreFreq_I>>6
        reqAb.Param.LowCentreFreqInteger=centreFreq_I&0x003F
        reqAb.Param.HighCentreFreqFraction=centreFreq_F>>8
        reqAb.Param.LowCentreFreqFraction=centreFreq_F&0x0FF
        reqAb.Param.UploadNum=int(self.UploadNum.GetValue())
        reqAb.Param.DataRate=bandWidth
        reqAb.Param.BandWidth=bandWidth
        
        startTime=(int(self.StartTimeYear.GetValue()),int(self.StartTimeMonth.GetValue()),  \
                   int(self.StartTimeDay.GetValue()),int(self.StartTimeHour.GetValue()),    \
                   int(self.StartTimeMinute.GetValue()),int(self.StartTimeSecond.GetValue()))
                   
        
       
        reqAb.Time.HighYear=startTime[0]>>4
        reqAb.Time.LowYear=startTime[0]&0x00F
        reqAb.Time.Month=startTime[1]
        reqAb.Time.Day=startTime[2]
        reqAb.Time.HighHour=startTime[3]>>2
        reqAb.Time.LowHour=startTime[3]&0x03
        reqAb.Time.Minute=startTime[4]
        reqAb.Time.Second=startTime[5]
        
        # if(staticVar.getSock()):
        #     staticVar.getSock().sendall(bytearray(reqAb))

        self.parent.queueRequest.put(reqAb)

    
        self.Close()
        
        

