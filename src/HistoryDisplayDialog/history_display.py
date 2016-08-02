# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

from src.HistoryDisplayDialog.display_spec import  dialog_display_spec
from src.HistoryDisplayDialog.display_IQ import dialog_display_iq


###########################################################################
## Class MyDialog4
###########################################################################

class dialog_historydis ( wx.Dialog ):
    
    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"历史数据", pos = wx.DefaultPosition, size = wx.Size( 200 ,300 ), style = wx.DEFAULT_DIALOG_STYLE )

        self.SetFont(wx.Font(10, wx.ROMAN, wx.NORMAL, wx.LIGHT, underline=False, faceName=u"微软雅黑",
                             encoding=wx.FONTENCODING_DEFAULT))

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        gSizer4 = wx.GridSizer( 5, 1, 0, 0 )
        
        
        gSizer4.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        radio_historyChoices = [ u"历史功率谱数据", u"历史IQ数据" ]
        self.radio_history = wx.RadioBox( self, wx.ID_ANY, u"历史数据请求", wx.DefaultPosition, wx.Size( 150,-1 ), radio_historyChoices, 1, wx.RA_SPECIFY_COLS )
        self.radio_history.SetSelection( 0 )
        gSizer4.Add( self.radio_history, 0, wx.ALL, 5 )

        
        gSizer4.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.btn_ok = wx.Button( self, wx.ID_ANY, u"确定", wx.DefaultPosition, wx.DefaultSize, 0 )
        # gSizer4.Add( self.btn_ok, 0, wx.ALL, 5 )
        gSizer4.Add(self.btn_ok, 0, wx.ALIGN_CENTER, 5)
        
        self.SetSizer( gSizer4 )
        self.Layout()
        
        self.Centre( wx.BOTH )
        
        # Connect Events
        self.btn_ok.Bind( wx.EVT_BUTTON, self.btn_okOnButtonClick )
    
    def __del__( self ):
        pass
    
    
    # Virtual event handlers, overide them in your derived class
    def btn_okOnButtonClick( self, event ):
        if(self.radio_history.GetSelection()==0):
            dlg=dialog_display_spec(self)
            dlg.ShowModal()
            
            
        else:
            dlg=dialog_display_iq(self)
            dlg.ShowModal()
         
          
        event.Skip()
    
#     
# app=wx.App()
# MyDialog4(None).Show()
# app.MainLoop()

