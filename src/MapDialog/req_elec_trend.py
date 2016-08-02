# -*- coding: utf-8 -*- 
import wx

from src.Package.package import ReqElecTrend,FrameHeader,FrameTail,Time
from src.CommonUse.staticVar import staticVar
import time
class ReqElecTrendDialog(wx.Dialog):
    def __init__(self,parent):
        wx.Dialog.__init__(self,parent,-1,u"电磁分布态势数据请求",size=(400,500))

        self.SetFont(wx.Font(10, wx.ROMAN, wx.NORMAL, wx.LIGHT, underline=False, faceName=u"微软雅黑",
                             encoding=wx.FONTENCODING_DEFAULT))
        self.parent=parent
        
        
        ###############################
        self.tail=FrameTail(0,0,0xAA)
        
        self.id=staticVar.getid()
        self.lowid=self.id&0x00FF
        self.highid=self.id>>8
        
        self.List=staticVar.getCentreFreq()
        self.ListFreq=staticVar.getFreq()
        ##############################
        panel=wx.Panel(self,-1)
        
        self.FreqSection=wx.ComboBox(panel,-1,u"FM调频广播频段",choices=self.List)
        self.FreqSection.SetSelection(0)
        self.radioChoose=wx.RadioButton(panel,-1,u"选择频率")
        self.radioHand=wx.RadioButton(panel,-1,u"手动频率")
        self.CentreFreq=wx.TextCtrl(panel,-1,size=(80,25))
        self.BandWidth=wx.TextCtrl(panel,-1,size=(80,25))
        self.Radius=wx.TextCtrl(panel,-1,size=(80,25))
        self.FenBianLv=wx.TextCtrl(panel,-1,size=(80,25))
        self.RefreshIntv=wx.TextCtrl(panel,-1,size=(80,25))

        #############################################
        curTime = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        Year = int(curTime[0:4])
        Month = int(curTime[4:6])
        Day = int(curTime[6:8])
        Hour = int(curTime[8:10])
        Min = int(curTime[10:12]) + 2

        ###############################################

        self.StartTimeYear = wx.ComboBox(panel, -1, str(Year), choices=["2015", "2016", "2017", "2018"])
        self.StartTimeMonth = wx.ComboBox(panel, -1, str(Month),
                                          choices=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"])
        self.StartTimeDay = wx.TextCtrl(panel, -1, str(Day), size=(60, 25))
        self.StartTimeHour = wx.TextCtrl(panel, -1, str(Hour), size=(60, 25))
        self.StartTimeMinute = wx.TextCtrl(panel, -1, str(Min), size=(60, 25))

        self.EndTimeYear = wx.ComboBox(panel, -1, str(Year), choices=["2015", "2016", "2017", "2018"])
        self.EndTimeMonth = wx.ComboBox(panel, -1, str(Month),
                                        choices=["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"])
        self.EndTimeDay = wx.TextCtrl(panel, -1, str(Day), size=(60, 25))
        self.EndTimeHour = wx.TextCtrl(panel, -1, str(Hour), size=(60, 25))
        self.EndTimeMinute = wx.TextCtrl(panel, -1, str(Min), size=(60, 25))


        sizer=wx.BoxSizer(wx.VERTICAL)
        hBox=wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add((30,30))
        hBox.Add(self.radioChoose,0,wx.LEFT,20)
        hBox.Add(self.radioHand,0,wx.LEFT,20)
        sizer.Add(hBox)
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
        hBox1.Add(wx.StaticText(panel,-1,u"地理半径(km)",size=(100,25)),0,wx.LEFT,20)
        hBox1.Add(self.Radius,0,wx.LEFT,20)
        sizer.Add(hBox1)
        
        sizer.Add((10,10))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(wx.StaticText(panel,-1,u"经纬度分辨率",size=(100,25)),0,wx.LEFT,20)
        hBox1.Add(self.FenBianLv,0,wx.LEFT,20)
        sizer.Add(hBox1)

        sizer.Add((10,10))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(wx.StaticText(panel,-1,u"动态刷新间隔(Min)",size=(130,25)),0,wx.LEFT,20)
        hBox1.Add(self.RefreshIntv,0,wx.LEFT,20)
        sizer.Add(hBox1)

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
        
        self.CentreFreq.Enable(True)
        self.BandWidth.Enable(True)
        self.radioHand.SetValue(True)
        
        self.Layout()
        self.Centre( wx.BOTH )
        
        ##Events
        self.btn_ok.Bind(wx.EVT_BUTTON,self.OnbtnOK)
        self.Bind(wx.EVT_RADIOBUTTON, self.OnRadio)
        
    def OnRadio(self,event):
        if(self.radioChoose.GetValue()):
            self.FreqSection.Enable(True)
            self.BandWidth.Enable(False)
            self.CentreFreq.Enable(False)

        elif(self.radioHand.GetValue()):
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
            
    def OnbtnOK(self,event):
        reqElec=ReqElecTrend()
        reqElec.CommonHeader=FrameHeader(0x55,0xA2,self.lowid,self.highid)
        reqElec.CommonTail=self.tail
        if(self.radioChoose.GetValue()):
            centreFreq=int(self.ListFreq[self.FreqSection.GetSelection()][0])
            bandWidth=int(self.ListFreq[self.FreqSection.GetSelection()][1])

        else:
            centreFreq=int(self.CentreFreq.GetValue())
            bandWidth=int(self.BandWidth.GetValue())
        
        reqElec.HighCentreFreq=centreFreq>>8
        reqElec.LowCentreFreq=centreFreq&0x00FF
        reqElec.BandWidth=bandWidth
        reqElec.Radius=int(self.Radius.GetValue())
        fenBianLv=float(self.FenBianLv.GetValue())
        startTime=(int(self.StartTimeYear.GetValue()),int(self.StartTimeMonth.GetValue()),  \
                   int(self.StartTimeDay.GetValue()),int(self.StartTimeHour.GetValue()),    \
                   int(self.StartTimeMinute.GetValue())
                   )
        endTime=(int(self.EndTimeYear.GetValue()),int(self.EndTimeMonth.GetValue()),  \
                   int(self.EndTimeDay.GetValue()),int(self.EndTimeHour.GetValue()),    \
                   int(self.EndTimeMinute.GetValue())
                   )
       
        reqElec.FenBianLvInteger=int(fenBianLv)
        reqElec.FenBianLvFraction=int((fenBianLv-int(fenBianLv))*8)
        
        reqElec.RefreshIntv=int(self.RefreshIntv.GetValue())
        reqElec.StartTime=self.ByteToTime(startTime)
        reqElec.EndTime=self.ByteToTime(endTime)


        # if(staticVar.getSock()):
        #     staticVar.getSock().sendall(bytearray(reqElec))
        #     for i in  bytearray(reqElec):
        #         print i,

        self.parent.queueRequest.put(reqElec)

        self.Close()
    
        
        
        
