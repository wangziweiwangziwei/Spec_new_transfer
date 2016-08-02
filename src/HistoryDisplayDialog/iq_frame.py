# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
from src.HistoryDisplayDialog.iq_demod_param import dialog_demod
###########################################################################
## Class MyDialog1
###########################################################################

class display_iqframe ( wx.Dialog ):
    
    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"iq窗口显示", pos = wx.DefaultPosition, size = wx.Size( 272,364 ), style = wx.DEFAULT_DIALOG_STYLE )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        gSizer1 = wx.GridSizer( 8, 2, 0, 0 )
        
        self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"解调路径：", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        gSizer1.Add( self.m_staticText1, 0, wx.ALL, 5 )
        
        
        gSizer1.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.m_filePick = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.Size( 220,-1 ), wx.FLP_DEFAULT_STYLE )
        gSizer1.Add( self.m_filePick, 0, wx.ALL, 5 )
        
        
        gSizer1.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        
        gSizer1.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        
        gSizer1.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.m_check_wave = wx.CheckBox( self, wx.ID_ANY, u"波形图", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer1.Add( self.m_check_wave, 0, wx.ALL, 5 )
        
        self.m_check_spec = wx.CheckBox( self, wx.ID_ANY, u"功率谱", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer1.Add( self.m_check_spec, 0, wx.ALL, 5 )
        
        self.m_check_water = wx.CheckBox( self, wx.ID_ANY, u"瀑布图", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer1.Add( self.m_check_water, 0, wx.ALL, 5 )
        
        self.m_check_ccdf = wx.CheckBox( self, wx.ID_ANY, u"CCDF", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer1.Add( self.m_check_ccdf, 0, wx.ALL, 5 )
        
        self.m_check_constel = wx.CheckBox( self, wx.ID_ANY, u"星座图", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer1.Add( self.m_check_constel, 0, wx.ALL, 5 )
        
        self.m_check_eye = wx.CheckBox( self, wx.ID_ANY, u"眼图", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer1.Add( self.m_check_eye, 0, wx.ALL, 5 )
        
        self.btn_ok = wx.Button( self, wx.ID_ANY, u"确定", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer1.Add( self.btn_ok, 0, wx.ALL, 5 )
        
        self.m_button2 = wx.Button( self, wx.ID_ANY, u"取消", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer1.Add( self.m_button2, 0, wx.ALL, 5 )
        
        
        self.SetSizer( gSizer1 )
        self.Layout()
        
        self.Centre( wx.BOTH )
        
        # Connect Events
        self.btn_ok.Bind( wx.EVT_BUTTON, self.btn_okOnButtonClick )
    
    def __del__( self ):
        pass
    
    
    # Virtual event handlers, overide them in your derived class
    def btn_okOnButtonClick( self, event ):
       
        if(self.m_check_constel.GetValue() or self.m_check_eye.GetValue()):
            dlg=dialog_demod()
            dlg.ShowModal()
            event.Skip()
    

