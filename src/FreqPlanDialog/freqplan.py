# -*- coding: utf-8 -*- 
import wx
from src.CommonUse.staticVar import staticVar
from src.Package.package import *
class QueryFreqPlanDialog(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self,None,-1,u"国家无线电频率规划",size=(300,200))
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
        self.btn_ok=wx.Button(panel,-1,u"确定",size=(60,25))
        
        hBox1.Add(self.btn_ok,0,wx.LEFT,20)
        hBox1.Add(wx.Button(panel,wx.ID_CANCEL,u"取消",size=(60,25)),0,wx.LEFT,20)
        sizer.Add(hBox1)
        panel.SetSizer(sizer)

        self.btn_ok.Bind(wx.EVT_BUTTON,self.OnbtnOK)
        
    def OnbtnOK(self,event):
    
        freqStart=int(self.FreqStart.GetValue())
        freqEnd=int(self.FreqEnd.GetValue())
        highFreqStart=freqStart>>16
        midFreqStart=(freqStart&0x00FF00)>>8
        lowFreqStart=freqStart&0x0000FF
        
        highFreqEnd=freqEnd>>16
        midFreqEnd=(freqEnd&0x00FF00)>>8
        lowFreqEnd=freqEnd&0x0000FF
        header=FrameHeader(0x55,0xA7,staticVar.getid()&0x00FF,staticVar.getid()>>8)
        tail=FrameTail(0,0,0xAA)
        structObj=QueryFreqPlan(header,highFreqStart,midFreqStart,  \
                                lowFreqStart,highFreqEnd,midFreqEnd,lowFreqEnd,tail)
       
       
        if(staticVar.getSock()):
            staticVar.getSock().sendall(bytearray(structObj))
        self.Destroy()





