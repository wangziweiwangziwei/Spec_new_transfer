# -*- coding: utf-8 -*- 
import wx

class ChangeAnotherIQ(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self,None,-1,u"改变另一终端定频参数",size=(350,500))
        wx.StaticText(self,-1,u"频率个数",pos=(20,20))
        wx.StaticLine(self,-1,pos=(20,40),size=(220,2),style=wx.LI_HORIZONTAL)

        sampleList=[u"1个",u"2个",u"3个"]
        self.radioBox= wx.RadioBox(self, -1,pos=(20,50),size=(100,30),choices=sampleList)
        self.radioBox.SetSelection(0)

        wx.StaticText(self,-1,u"频率值 (MHz)",pos=(20,120))
        wx.StaticLine(self,-1,pos=(20,140),size=(220,2),style=wx.LI_HORIZONTAL)

        self.textFreq1=wx.TextCtrl(self,-1,"",(20,160),(60,25))
        self.textFreq2=wx.TextCtrl(self,-1,"",(100,160),(60,25))
        self.textFreq3=wx.TextCtrl(self, -1,"",(180,160),(60,25))

        self.textFreq2.Enable(False)
        self.textFreq3.Enable(False)
        self.Bind(wx.EVT_RADIOBOX,self.OnRadio,self.radioBox)
        
        wx.StaticText(self,-1,u"指定终端设备ID：" ,(30,200))
        self.ApointID=wx.TextCtrl(self,-1,"1",(200,200),(100,25))
        
        wx.StaticText(self,-1,u"带宽/数据率 (MHz/Msps):",pos=(30,240))
        sampleList = ['5/5','2.5/2.5','1/1','0.5/0/5','0.1/0/1']
        self.BandWidth = wx.ComboBox(self, -1,'5/5',pos=(200,240),size=(100,30),choices=sampleList)
        self.BandWidth.SetSelection(0)
        wx.StaticText(self,-1,u"上传数据块个数(1-256) : ",(30,280))
        self.textUploadNum=wx.TextCtrl(self,-1,"1",(200,280),(100,25))
        
        wx.StaticText(self,-1,u"延时时间(s): ",(30,320))
        self.textDelay=wx.TextCtrl(self,-1,"",(200,320),(100,25))
        
        wx.StaticBox(self, -1, u'接受增益(dB)', (30, 360), size=(240, 60))
        self.sliderGain = wx.Slider(self,-1, 7,-1, 73, (20, 380), (220, -1), \
                                    wx.SL_AUTOTICKS | wx.SL_HORIZONTAL | wx.SL_LABELS)
        
        wx.Button(self,wx.ID_ANY,u"确定",size=(60,20),pos=(20,440))
        wx.Button(self,wx.ID_ANY,u"取消",(100,440),(60,20))
        
    def OnRadio(self,event):
        switch=self.radioBox.GetSelection()
        if(switch==0):
            self.textFreq2.Enable(False)
            self.textFreq3.Enable(False)
        elif(switch==1):
            self.textFreq2.Enable(True)
            self.textFreq3.Enable(False)
        elif(switch==2):
            self.textFreq2.Enable(True)
            self.textFreq3.Enable(True)
        else:
            pass 
        
        