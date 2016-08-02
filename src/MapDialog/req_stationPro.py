# -*- coding: utf-8 -*- 
import wx

from src.Package.package import QueryStationPro,FrameHeader,FrameTail
from src.CommonUse.staticVar import staticVar

class QueryStationProDialog(wx.Dialog):
    def __init__(self,parent,func):
        wx.Dialog.__init__(self,parent,-1,u"台站登记属性查询",size=(300,200))

        self.SetFont(wx.Font(10, wx.ROMAN, wx.NORMAL, wx.LIGHT, underline=False, faceName=u"微软雅黑",
                             encoding=wx.FONTENCODING_DEFAULT))

        ###############################
        self.parent=parent

        self.tail=FrameTail(0,0,0xAA)
        
        self.id=staticVar.getid()
        self.lowid=self.id&0x00FF
        self.highid=self.id>>8
        self.func=func
        
        ###############################################
        
        
        
        panel=wx.Panel(self,-1)
        sizer=wx.BoxSizer(wx.VERTICAL)
        self.FreqStart=wx.TextCtrl(panel,-1,size=(60,25))
        self.FreqEnd=wx.TextCtrl(panel,-1,size=(60,25))

        sizer.Add((20,15))
        sizer.Add(wx.StaticText(panel,-1,u"台站指定频率范围(MHz): ",size=(150,25)),0,wx.LEFT,20)
        sizer.Add((20,10))
        hBox3=wx.BoxSizer(wx.HORIZONTAL)          
        hBox3.Add(self.FreqStart,0,wx.LEFT|wx.ALIGN_BOTTOM,20)
        hBox3.Add(wx.StaticText(panel,-1,u"——"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,10)
        hBox3.Add(self.FreqEnd,0,wx.ALIGN_BOTTOM,20)
        sizer.Add(hBox3)
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
        freqStart=int(self.FreqStart.GetValue())
        freqEnd=int(self.FreqEnd.GetValue())
        stationPro=QueryStationPro()
        stationPro.CommonHeader=FrameHeader(0x55,self.func,self.lowid,self.highid)
        stationPro.CommonTail=self.tail
        stationPro.HighFreqStart=freqStart>>8
        stationPro.LowFreqStart=freqStart&0x00FF
        stationPro.HighFreqEnd=freqEnd>>8
        stationPro.LowFreqEnd=freqEnd&0x00FF

        self.parent.queueRequest.put(stationPro)

        # if(staticVar.getSock()):
        #     staticVar.getSock().sendall(bytearray(stationPro))


        self.Close()
        
        
        
        
        
        
        
        
    