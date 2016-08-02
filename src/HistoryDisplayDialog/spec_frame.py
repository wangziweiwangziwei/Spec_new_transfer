# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MyDialog2
###########################################################################

class display_specframe ( wx.Dialog ):
    
    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"spec显示窗口", pos = wx.DefaultPosition, size = wx.Size( 241,282 ), style = wx.DEFAULT_DIALOG_STYLE )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        gSizer2 = wx.GridSizer( 6, 2, 0, 0 )
        
        self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"显示路径选择：", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )
        gSizer2.Add( self.m_staticText2, 0, wx.ALL, 5 )
        
        
        gSizer2.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.m_filePick = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a file", u"*.*", wx.DefaultPosition, wx.DefaultSize, wx.FLP_DEFAULT_STYLE )
        gSizer2.Add( self.m_filePick, 0, wx.ALL, 5 )
        
        
        gSizer2.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.m_check_spec = wx.CheckBox( self, wx.ID_ANY, u"  功率谱图", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer2.Add( self.m_check_spec, 0, wx.ALL, 5 )
        
        
        gSizer2.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.m_check_water = wx.CheckBox( self, wx.ID_ANY, u"   瀑布图", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer2.Add( self.m_check_water, 0, wx.ALL, 5 )
        
        
        gSizer2.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.m_btn_ok = wx.Button( self, wx.ID_ANY, u"确定", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer2.Add( self.m_btn_ok, 0, wx.ALL, 5 )
        
        
        self.SetSizer( gSizer2 )
        self.Layout()
        
        self.Centre( wx.BOTH )
        
        # Connect Events
        self.m_btn_ok.Bind( wx.EVT_BUTTON, self.m_btn_okOnButtonClick )
    
    def __del__( self ):
        pass
    
    
    # Virtual event handlers, overide them in your derived class
    def m_btn_okOnButtonClick( self, event ):
        event.Skip()
    

