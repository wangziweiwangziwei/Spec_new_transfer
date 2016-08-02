# -*- coding: utf-8 -*- 
import wx
class dialog_demod(wx.Dialog):
    def __init__(self):
        wx.Dialog.__init__(self,None,-1,u"解调参数设置",size=(400,300))
        title=wx.StaticText(self,-1,u"Set",pos=(35,10))
        title.SetFont(wx.Font(wx.SystemSettings.GetFont(wx.SYS_ANSI_VAR_FONT).GetPointSize(),wx.FONTFAMILY_DEFAULT,wx.NORMAL,wx.FONTWEIGHT_BOLD))
        wx.StaticLine(self,-1,(0,30),(400,1),style=wx.LI_HORIZONTAL)
        
        wx.StaticText(self,-1,"RolloffFactor",(35,40),(100,25))
        wx.StaticText(self,-1,"Signal Rate(Fd)",(35,80),(100,25))
        wx.StaticText(self,-1,"Modulation Type",(35,120),(100,25))
        self.Text_R=wx.TextCtrl(self,-1,"0.5",(200,40),(100,25))
        self.Text_Fd=wx.TextCtrl(self,-1,"0.25",(200,80),(100,25))
        sampleListMod = ['AM','FM', 'PM', '2FSK', '4FSK', '2PSK', '8PSK', '16PSK', '16QAM','32QAM']
        self.ctrlChoice = wx.Choice(self, -1,pos=(200,120),size=(100,25),choices=sampleListMod)
        self.ctrlChoice.SetSelection(8)
        self.btn_ok=wx.Button(self,wx.ID_ANY,"OK",(120,180),(60,20))
        
        #EVENTS
        self.btn_ok.Bind(wx.EVT_BUTTON,self.OnBtnClick)
        
    def OnBtnClick(self,event):
        pass