# -*- coding: utf-8 -*- 

import wx
import powersptrLoc
import iqLoc
import powersptrSer
import iqSer
from src.HistoryDisplayDialog import display_spec,display_IQ

class SignalAnalysisDlg(wx.Dialog):
    
    def __init__(self,parent):
        
        wx.Dialog.__init__(self,parent,-1,u"信号分析",wx.DefaultPosition,wx.DefaultSize)

        ###################
        self.parent=parent

        self.choice_local=0

        self.dlg_iq_local=0
        self.dlg_spec_local=0
        self.dlg_iq_ser=0
        self.dlg_spec_ser=0

        ####################
        panel = wx.Panel(self)
        
        
        self.chooLbl = wx.StaticText(panel,-1,u"选择文件：")
        
        
        self.locFile = wx.RadioButton(panel,-1,u"本地数据分析：",wx.DefaultPosition,wx.DefaultSize)
        self.serFile = wx.RadioButton(panel,-1,u"服务器数据分析：",wx.DefaultPosition,wx.DefaultSize)
        
        self.filetypeList = [u"功率谱文件",u"IQ文件"]
        self.localData = wx.RadioBox(panel,-1,u"",wx.DefaultPosition,wx.DefaultSize,self.filetypeList,0,wx.RA_SPECIFY_ROWS)
        self.serverData = wx.RadioBox(panel,-1,u"",wx.DefaultPosition,wx.DefaultSize,self.filetypeList,0,wx.RA_SPECIFY_ROWS)
        
        self.okButton = wx.Button(panel,-1,u"确定",wx.DefaultPosition,wx.DefaultSize)
        self.cancleButton = wx.Button(panel,-1,u"取消",wx.DefaultPosition,wx.DefaultSize)
        
        self.localData.Enable(False)
        #self.serverData.Enable(False)
        
        
        sSizer = wx.FlexGridSizer(0,1,0,0)  
        sSizer.Add(self.chooLbl,0,wx.ALL,5)
        sSizer.Add(self.locFile,0,wx.ALL,5)
        sSizer.Add(self.localData,0,wx.ALIGN_CENTER|wx.ALIGN_TOP,5)
        sSizer.Add((10,10))
        sSizer.Add(wx.StaticLine(panel),0,wx.EXPAND,5)
        sSizer.Add(self.serFile,0,wx.ALL,5)
        sSizer.Add(self.serverData,0,wx.ALIGN_CENTER|wx.ALIGN_TOP,5)
        
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add(self.okButton,0,wx.ALL,5)
        btnSizer.Add(self.cancleButton,0,wx.ALL,5)
        sSizer.Add(btnSizer,0,wx.ALL,5)
        
        panel.SetSizer(sSizer)
        sSizer.Fit(self)
        sSizer.SetSizeHints(self)
        
        
        self.Bind(wx.EVT_RADIOBUTTON,self.OnlocFile,self.locFile)
        self.Bind(wx.EVT_RADIOBUTTON,self.OnserFile,self.serFile)
        self.Bind(wx.EVT_BUTTON,self.okClick,self.okButton)
     
    def OnlocFile(self,event):
        self.localData.Enable(True)
        self.choice_local=1
        self.serverData.Enable(False)
        #self.locText = event.GetEventObject().GetLabel()
        #print self.locText
        #event.Skip()
    
    def OnserFile(self,event):
        self.localData.Enable(False)
        self.serverData.Enable(True)
        self.choice_local=0
        #self.serText = event.GetEventObject().GetLabel()
        #event.Skip()
    
    def okClick(self,event):
        if(self.choice_local):
            if ( self.localData.GetSelection()==0 ):
                if(self.dlg_spec_local==0):
                    self.dlg_spec_local = powersptrLoc.PowerSptrLocDialog(self)
                self.dlg_spec_local.ShowModal()
            
            else:
                if(self.dlg_iq_local==0):
                    self.dlg_iq_local = iqLoc.IQLocDialog(self)
                self.dlg_iq_local.ShowModal()

        else:            
            if ( self.serverData.GetSelection()==0 ):
                if(self.dlg_spec_ser==0):
                    self.dlg_spec_ser = display_spec.dialog_display_spec(self)
                self.dlg_spec_ser.isValid=0
                self.dlg_spec_ser.ShowModal()
                if(self.dlg_spec_ser.isValid):
                    dlg = powersptrSer.PowerSptrSerDialog()
                    dlg.ShowModal()


                
            else:
                if(self.dlg_iq_ser==0):
                    self.dlg_iq_ser = display_IQ.dialog_display_iq(self)
                self.dlg_iq_ser.isValid=0
                self.dlg_iq_ser.ShowModal()

                if (self.dlg_iq_ser.isValid):
                    dlg = iqSer.IQSerDialog()
                    dlg.ShowModal()


            
        
            
        
    
# #if __name__ == '__main__':
# app = wx.App()
# app.MainLoop()
# locale=wx.Locale(wx.LANGUAGE_ENGLISH)
# dialog = SignalAnalysisDlg()
# dialog.ShowModal()
