# -*- coding: utf-8 -*- 
import wx
from src.Package.package import ReqData,FrameHeader,FrameTail,Time 
from src.CommonUse.staticVar import staticVar


class dialog_display_iq(wx.Dialog):
    def __init__(self,parent):
        wx.Dialog.__init__(self,parent,-1,u"指定终端IQ数据查询",size=(400,350))
        self.parent=parent
        self.isValid=0
        
        panel=wx.Panel(self,-1)
        self.ApointID=wx.TextCtrl(panel,-1,size=(80,25))
        self.StartTimeYear=wx.ComboBox(panel,-1,"2015",choices=["2015","2016","2017","2018"])
        self.StartTimeMonth=wx.ComboBox(panel,-1,"12",choices=["1","2","3","4","5","6","7","8","9","10","11","12"])
        self.StartTimeDay=wx.TextCtrl(panel,-1,"1",size=(60,25))
        self.StartTimeHour=wx.TextCtrl(panel,-1,"0",size=(60,25))
        self.StartTimeMinute=wx.TextCtrl(panel,-1,"0",size=(60,25))

        self.EndTimeYear=wx.ComboBox(panel,-1,"2015",choices=["2015","2016","2017","2018"])
        self.EndTimeMonth=wx.ComboBox(panel,-1,"12",choices=["1","2","3","4","5","6","7","8","9","10","11","12"])
        self.EndTimeDay=wx.TextCtrl(panel,-1,"1",size=(60,25))
        self.EndTimeHour=wx.TextCtrl(panel,-1,"0",size=(60,25))
        self.EndTimeMinute=wx.TextCtrl(panel,-1,"0",size=(60,25))

        self.StartTimeYear.SetSelection(0)
        self.StartTimeMonth.SetSelection(11)
        self.EndTimeYear.SetSelection(0)
        self.EndTimeMonth.SetSelection(11)
        
        sizer=wx.BoxSizer(wx.VERTICAL)
        sizer.Add((10,30))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(wx.StaticText(panel,-1,u"指定设备ID:",size=(100,25)),0,wx.LEFT,20)
        hBox1.Add(self.ApointID,0,wx.LEFT,20)
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

        sizer.Add((10,10))
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
        self.btn_ok=wx.Button(panel,wx.ID_ANY,"OK",size=(60,25))
        hBox1.Add(self.btn_ok,0,wx.LEFT,20)
        hBox1.Add(wx.Button(panel,wx.ID_ANY,"CANCEL",size=(60,25)),0,wx.LEFT,20)
        sizer.Add(hBox1)
        panel.SetSizer(sizer)

        #Events
        self.btn_ok.Bind(wx.EVT_BUTTON, self.OnBtnClick)
        
    def OnBtnClick(self,event):
        self.isValid=1

        self.HistoryDataQuery(0xAC)
        self.Close()
        # self.parent.Close()
    
    def HistoryDataQuery(self,functionPara):
        Obj=ReqData()
        
        startTime=(int(self.StartTimeYear.GetValue()),int(self.StartTimeMonth.GetValue()),
                   int(self.StartTimeDay.GetValue()),int(self.StartTimeHour.GetValue()),
                   int(self.StartTimeMinute.GetValue())
                   )
        endTime=(int(self.EndTimeYear.GetValue()),int(self.EndTimeMonth.GetValue()),
                   int(self.EndTimeDay.GetValue()),int(self.EndTimeHour.GetValue()),
                   int(self.EndTimeMinute.GetValue())
                   )
        apointID=int(self.ApointID.GetValue())
        
        Obj.CommonHeader=FrameHeader(0x55,functionPara,staticVar.getid()&0x00FF,staticVar.getid()>>8)
        Obj.CommonTail=FrameTail(0,0,0xAA)
        Obj.ApointID_h=apointID>>8
        Obj.ApointID_l=apointID&0x00FF
        Obj.StartTime=self.ByteToTime(startTime)
        Obj.EndTime=self.ByteToTime(endTime)
        
        if(staticVar.getSock()):
            staticVar.getSock().sendall(bytearray(Obj))
    
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

            


            
