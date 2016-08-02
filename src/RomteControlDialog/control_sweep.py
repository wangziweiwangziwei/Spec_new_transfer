# -*- coding: utf-8 -*- 
import wx
class ChangeAnotherSweep(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self,None,-1,u"改变另一终端扫频参数",size=(430,600))
        
        panel=wx.Panel(self,-1)
        sizer=wx.BoxSizer(wx.VERTICAL)
        sampleList = ['3','10','20','25','30','40']
        self.ApointID=wx.TextCtrl(panel,-1,size=(80,25))
        self.AdaptThres = wx.ComboBox(panel, -1,value='20',size=(100,30),choices=sampleList)
        self.StaticThres = wx.TextCtrl(panel, -1, "",size=(100,25))
        self.AdaptThres.SetSelection(0)

        self.sliderGain = wx.Slider(panel,-1, 7,-1, 73,(20,20),(220, -1),wx.SL_AUTOTICKS | wx.SL_HORIZONTAL | wx.SL_LABELS)
        self.textM=wx.TextCtrl(panel,-1,"63",size=(60,25))
        self.ChangeThres=wx.ComboBox(panel,-1,"10",choices=["10","20"],size=(100,25))
        
        self.ChangeThres.SetSelection(0)
        self.RadioBoxTrans=wx.RadioBox(panel,-1,choices=[u"手动传输",u"不定时自动传输",u"抽取定时自动传输"])
        self.RadioBoxSweep=wx.RadioBox(panel,-1,choices=[u"全频带",u"指定频段",u"多频段"])
        self.RadioBoxThres=wx.RadioBox(panel,-1,choices=[u"自适应门限",u"固定门限"])
        self.RadioBoxSweep.SetSelection(0)
        self.RadioBoxTrans.SetSelection(0)
        self.RadioBoxThres.SetSelection(0)

        self.Check1=wx.CheckBox(panel,-1)
        self.FreqStart1=wx.TextCtrl(panel,-1,size=(60,25))
        self.FreqEnd1=wx.TextCtrl(panel,-1,size=(60,25))

        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(wx.StaticText(panel,-1,u"指定终端设备ID："),0,wx.TOP|wx.LEFT,20)
        hBox1.Add(self.ApointID,0,wx.LEFT|wx.ALIGN_BOTTOM,10)
        sizer.Add(hBox1)
        
        sizer.Add((10,10))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(wx.StaticText(panel,-1,u"扫频模式选择: ",size=(120,25)),0,wx.LEFT,20)
        hBox1.Add(self.RadioBoxSweep,0,wx.LEFT|wx.ALIGN_TOP,20)
        sizer.Add(hBox1)
        sizer.Add((10,10))
        sizer.Add(wx.StaticText(panel,-1,u"传输方式选择: ",size=(120,25)),0,wx.LEFT,20)
        sizer.Add(self.RadioBoxTrans,0,wx.LEFT,20)
        sizer.Add((10,10))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(wx.StaticText(panel,-1,u"检测门限类型: ",size=(120,25)),0,wx.LEFT,20)
        hBox1.Add(self.RadioBoxThres,0,wx.LEFT|wx.ALIGN_TOP,20)
        sizer.Add(hBox1)
        
        
        sizer.Add((10,10))
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(wx.StaticText(panel,-1,u"抽取倍率M(1-63)"),0,wx.LEFT,20)
        hBox1.Add(self.textM,0,wx.LEFT,10)
        sizer.Add(hBox1)

        sizer.Add((10,10))
        hBox2=wx.BoxSizer(wx.HORIZONTAL)          
        hBox2.Add(wx.StaticText(panel,-1,u"数据变化门限(dB)",size=(100,25)),0,wx.LEFT,20)
        hBox2.Add(self.ChangeThres,0,wx.LEFT|wx.ALIGN_BOTTOM,10)
        sizer.Add(hBox2)

        sizer.Add((10,10))
        hBox2=wx.BoxSizer(wx.HORIZONTAL)          
        hBox2.Add(wx.StaticText(panel,-1,u"接收增益(dB)",size=(100,25)),0,wx.LEFT,20)
        hBox2.Add(self.sliderGain,0,wx.LEFT|wx.ALIGN_BOTTOM,10)
        sizer.Add(hBox2)
        
        sizer.Add((10,10))
        hBox2=wx.BoxSizer(wx.HORIZONTAL)          
        hBox2.Add(wx.StaticText(panel,-1,u"自适应门限(dB)",size=(100,25)),0,wx.LEFT,20)
        hBox2.Add(self.AdaptThres,0,wx.LEFT|wx.ALIGN_BOTTOM,10)
        sizer.Add(hBox2)

        sizer.Add((10,10))
        hBox2=wx.BoxSizer(wx.HORIZONTAL)          
        hBox2.Add(wx.StaticText(panel,-1,u"固定门限(dB)",size=(100,25)),0,wx.LEFT,20)
        hBox2.Add(self.StaticThres,0,wx.LEFT|wx.ALIGN_BOTTOM,10)
        sizer.Add(hBox2)

        sizer.Add((20,10))
        sizer.Add(wx.StaticText(panel,-1,u"指定频率范围(MHz): ",size=(150,25)),0,wx.LEFT,20)
        hBox3=wx.BoxSizer(wx.HORIZONTAL)   
        hBox3.Add(self.Check1,0,wx.LEFT|wx.ALIGN_BOTTOM,20)       
        hBox3.Add(self.FreqStart1,0,wx.LEFT|wx.ALIGN_BOTTOM,20)
        hBox3.Add(wx.StaticText(panel,-1,u"——"),0,wx.LEFT|wx.RIGHT|wx.ALIGN_BOTTOM,10)
        hBox3.Add(self.FreqEnd1,0,wx.ALIGN_BOTTOM,20)
        sizer.Add(hBox3)
        sizer.Add((20,10))
    
        hBox1=wx.BoxSizer(wx.HORIZONTAL)
        hBox1.Add(wx.Button(panel,wx.ID_ANY,"OK",size=(60,25)),0,wx.LEFT,20)
        hBox1.Add(wx.Button(panel,wx.ID_ANY,"CANCEL",size=(60,25)),0,wx.LEFT,20)
        sizer.Add(hBox1)
        panel.SetSizer(sizer)
        self.Bind(wx.EVT_RADIOBOX, self.OnRadio)
        self.textM.Enable(False)
        self.StaticThres.Enable(False)
       
        self.Center()
      

     

    def OnRadio(self,event):
        if(self.RadioBoxTrans.GetSelection()==2):
            self.textM.Enable(True)
        else:
            self.textM.Enable(False)
        if(self.RadioBoxThres.GetSelection()==0):
            self.AdaptThres.Enable(True)
            self.StaticThres.Enable(False)
        else:
            self.AdaptThres.Enable(False)
            self.StaticThres.Enable(True)

  