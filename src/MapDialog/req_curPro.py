# -*- coding: utf-8 -*- 
import wx
from src.Package.package import QueryCurStationPro,FrameHeader,FrameTail
from src.CommonUse.staticVar import staticVar

class QueryCurStationProDialog(wx.Dialog):
    def __init__(self,parent):
        wx.Dialog.__init__(self,parent,-1,u"登记台站当前属性查询",size=(500,500))

        self.SetFont(wx.Font(10, wx.ROMAN, wx.NORMAL, wx.LIGHT, underline=False, faceName=u"微软雅黑",
                             encoding=wx.FONTENCODING_DEFAULT))

        #########################################

        self.parent = parent

        self.tail=FrameTail(0,0,0xAA)
        
        self.id=staticVar.getid()
        self.lowid=self.id&0x00FF
        self.highid=self.id>>8
        
        
        ###############################################
        
        panel=wx.Panel(self,-1)
        self.StationID=wx.TextCtrl(panel,-1,size=(80,25))
        sizer=wx.BoxSizer(wx.VERTICAL)
        sizer.Add((20,30))
        hBox3=wx.BoxSizer(wx.HORIZONTAL)     
        hBox3.Add(wx.StaticText(panel,-1,u"指定台站识别码: ",size=(100,25)),0,wx.LEFT,20)
        hBox3.Add(self.StationID,0,wx.LEFT|wx.ALIGN_BOTTOM,20)
        sizer.Add(hBox3)
        sizer.Add((20,20))
   
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

        sizer.Add((20,20))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        self.btn_ok=wx.Button(panel,-1,"OK",size=(60,25))
        
        hBox1.Add(self.btn_ok,0,wx.LEFT,20)
        hBox1.Add(wx.Button(panel,wx.ID_CANCEL,"CANCEL",size=(60,25)),0,wx.LEFT,20)
        sizer.Add(hBox1)
        panel.SetSizer(sizer)
        
        self.Layout()
        
        self.Centre( wx.BOTH )
        
        #Events
        self.btn_ok.Bind(wx.EVT_BUTTON, self.OnbtnOk)
    
    def OnbtnOk(self,event):
        
        ID=int(self.StationID.GetValue())
        curStationPro=QueryCurStationPro()
        curStationPro.CommonHeader=FrameHeader(0x55,0xA6,staticVar.getid()&0x00FF,staticVar.getid()>>8)
        curStationPro.CommonTail=FrameTail(0,0,0xAA)
        curStationPro.Identifier_h=ID>>16
        curStationPro.Identifier_m=(ID&0x00FF00)>>8
        curStationPro.Identifier_l=ID&0x0000FF
        
        if(self.radioBox.GetSelection()):
            curStationPro.LocateWay=0x0F
        centreFreq=float(self.CentreFreq.GetValue())  
        bandWidth=int(self.BandWidth.GetSelection())+1  
        centreFreq_I=int(centreFreq)
        centreFreq_F=int((centreFreq-int(centreFreq))*2**10)
        curStationPro.Param.HighCentreFreqInteger=centreFreq_I>>6
        curStationPro.Param.LowCentreFreqInteger=centreFreq_I&0x003F
        curStationPro.Param.HighCentreFreqFraction=centreFreq_F>>8
        curStationPro.Param.LowCentreFreqFraction=centreFreq_F&0x0FF
        curStationPro.Param.UploadNum=int(self.UploadNum.GetValue())
        curStationPro.Param.DataRate=bandWidth
        curStationPro.Param.BandWidth=bandWidth
        
        startTime=(int(self.StartTimeYear.GetValue()),int(self.StartTimeMonth.GetValue()),  \
                   int(self.StartTimeDay.GetValue()),int(self.StartTimeHour.GetValue()),    \
                   int(self.StartTimeMinute.GetValue()),int(self.StartTimeSecond.GetValue()))
                   
        
       
        curStationPro.Time.HighYear=startTime[0]>>4
        curStationPro.Time.LowYear=startTime[0]&0x00F
        curStationPro.Time.Month=startTime[1]
        curStationPro.Time.Day=startTime[2]
        curStationPro.Time.HighHour=startTime[3]>>2
        curStationPro.Time.LowHour=startTime[3]&0x03
        curStationPro.Time.Minute=startTime[4]
        curStationPro.Time.Second=startTime[5]

        #
        # if(staticVar.getSock()):
        #     staticVar.getSock().sendall(bytearray(curStationPro))

        self.parent.queueRequest.put(curStationPro)

        self.Close()

        
        
        
        
        
        
        


