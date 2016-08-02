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
## Class dialog_freqblock
###########################################################################

class dialog_freqblock ( wx.Dialog ):
    
    def __init__( self, parent ):
        ##### 这个变量是记录按了确定还是直接关闭了窗口########
        self.isValid=0
        
        #############
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"指定频段", pos = wx.DefaultPosition, size = wx.Size( 308,227 ), style = wx.DEFAULT_DIALOG_STYLE )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        gSizer5 = wx.GridSizer( 5, 2, 0, 0 )
        
        self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"指定频段频率范围", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText5.Wrap( -1 )
        gSizer5.Add( self.m_staticText5, 0, wx.ALL, 5 )
        
        
        gSizer5.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, u"起始频率（MHz）", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText7.Wrap( -1 )
        gSizer5.Add( self.m_staticText7, 0, wx.ALL, 5 )
        
        self.text_freq_start = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer5.Add( self.text_freq_start, 0, wx.ALL, 5 )
        
        self.m_staticText8 = wx.StaticText( self, wx.ID_ANY, u"终止频率（MHz）", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText8.Wrap( -1 )
        gSizer5.Add( self.m_staticText8, 0, wx.ALL, 5 )
        
        self.text_freq_end = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer5.Add( self.text_freq_end, 0, wx.ALL, 5 )
        
        self.btn_ok = wx.Button( self, wx.ID_ANY, u"确定", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer5.Add( self.btn_ok, 0, wx.ALL, 5 )
        
        
        self.SetSizer( gSizer5 )
        self.Layout()
        
        self.Centre( wx.BOTH )
        
        #Events
        
        self.btn_ok.Bind( wx.EVT_BUTTON, self.btn_okOnButtonClick )
        
    
    def __del__( self ):
        pass
    
    def btn_okOnButtonClick(self,event):
        
        self.isValid=1
        self.Destroy()
        
        
        
        
        
        
        
        

