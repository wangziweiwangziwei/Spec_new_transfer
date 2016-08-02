# -*- coding: utf-8 -*- 
import wx
class ChangeAnotherPress(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self,None,-1,u"改变另一终端压制参数",size=(400,550))
        sampleList=[u"手动",u"自动",u"不压制"]
        self.radioBox= wx.RadioBox(self, -1,label=u"压制模式",pos=(20,15), \
                                   size=(100,30),choices=sampleList)
        self.radioBox.SetSelection(2)
        
        sampleList=[u"单频点",u"双频点"]
        self.radioFreq= wx.RadioBox(self, -1,label=u"压制个数",pos=(20,70), \
                                    size=(100,30),choices=sampleList)
        self.radioFreq.SetSelection(0)
        
        wx.StaticText(self,-1,u"压制信号类型：",pos=(20,130))
        sampleList = [u'单频正弦',u'等幅多频',u'噪声调频',u'数字射频']
        self.combox = wx.ComboBox(self, -1,u'单频正弦',pos=(150,130),size=(80,30), \
                                  choices=sampleList)
        
        self.combox.SetSelection(0)
        wx.StaticText(self,-1,u"压制时间 (ms): ",(20,170),(100,25))
        wx.StaticText(self,-1,u"等待时间 (ms): ",(20,200),(100,25))
        wx.StaticText(self,-1,u"压制总时间 (ms)",(20,230),(100,25))
        
        self.textPressTime1=wx.TextCtrl(self,-1,"",(150,170),(80,25))
        self.textPressTime2=wx.TextCtrl(self, -1,"",(250,170),(80,25))

        self.textPressWait=wx.TextCtrl(self,-1,"",(150,200),(80,25))
        self.textPressTotal=wx.TextCtrl(self, -1,"",(150,230),(80,25))
        
        wx.StaticText(self,-1,u"频点频率 1(MHz): ",(20,270),(100,25))
        wx.StaticText(self,-1,u"频点频率 2(MHz): ",(20,310),(100,25))
        self.textPressFreq1=wx.TextCtrl(self,-1,"",(150,270),(80,25))
        self.textPressFreq2=wx.TextCtrl(self,-1,"",(150,310),(80,25))
        
        wx.StaticText(self,-1,u"指定终端设备ID: ",(20,350),(100,25))
        self.ApointID=wx.TextCtrl(self,-1,"",(150,350),(80,25))
        
        wx.StaticBox(self, -1, u'发射衰减(dB)', (10, 390), size=(240, 60))
        self.sliderWeak = wx.Slider(self,-1, 7,-1, 73, (20, 410), (220, -1), \
                                    wx.SL_AUTOTICKS | wx.SL_HORIZONTAL | wx.SL_LABELS)
        wx.Button(self,wx.ID_ANY,"OK",(20,470),(60,20))
        wx.Button(self,wx.ID_ANY,"CANCEL",(120,470),(60,20))
        
        self.Bind(wx.EVT_RADIOBOX,self.OnRadio,self.radioFreq)
        self.textPressTime2.Enable(False)
        self.textPressTotal.Enable(False)
       
        self.textPressFreq2.Enable(False)
            
    def OnRadio(self,event):
        if(self.radioFreq.GetSelection()==0):
            self.textPressTime2.Enable(False)
            self.textPressTotal.Enable(False)
            self.textPressFreq2.Enable(False)
        else:
            self.textPressTime2.Enable(True)
            self.textPressTotal.Enable(True)    
            self.textPressFreq2.Enable(True)
        
            