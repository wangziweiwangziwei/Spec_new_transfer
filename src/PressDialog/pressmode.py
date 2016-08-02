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
## Class dialog_pressmode
###########################################################################

class dialog_pressmode ( wx.Dialog ):
    
    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"压制模式设置", pos = wx.DefaultPosition, size = wx.Size( 387,325 ), style = wx.DEFAULT_DIALOG_STYLE )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        gSizer1 = wx.GridSizer( 8, 2, 0, 0 )
        
        
        gSizer1.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        
        gSizer1.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"压制总时间T1（ms）", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )
        gSizer1.Add( self.m_staticText2, 0, wx.ALL, 5 )
        
        self.m_text_T1 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer1.Add( self.m_text_T1, 0, wx.ALL, 5 )
        
        self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"压制后等待时间T2（ms）", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText3.Wrap( -1 )
        gSizer1.Add( self.m_staticText3, 0, wx.ALL, 5 )
        
        self.m_text_T2 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer1.Add( self.m_text_T2, 0, wx.ALL, 5 )
        
        self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"单次循环压制频点时间T3（ms）", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText4.Wrap( -1 )
        gSizer1.Add( self.m_staticText4, 0, wx.ALL, 5 )
        
        self.m_text_T3 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer1.Add( self.m_text_T3, 0, wx.ALL, 5 )
        
        self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"单次循环压制频点时间T4（ms）", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText5.Wrap( -1 )
        gSizer1.Add( self.m_staticText5, 0, wx.ALL, 5 )
        
        self.m_text_T4 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer1.Add( self.m_text_T4, 0, wx.ALL, 5 )
        
        self.btn_time_set = wx.Button( self, wx.ID_ANY, u"设置", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer1.Add( self.btn_time_set, 0, wx.ALL, 5 )
        
        self.btn_time_cancel = wx.Button( self, wx.ID_ANY, u"取消", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer1.Add( self.btn_time_cancel, 0, wx.ALL, 5 )
        
        
        self.SetSizer( gSizer1 )
        self.Layout()
        
        self.Centre( wx.BOTH )
        
        # Connect Events
        self.btn_time_set.Bind( wx.EVT_BUTTON, self.btn_time_setOnButtonClick )
        self.btn_time_cancel.Bind( wx.EVT_BUTTON, self.btn_time_cancelOnButtonClick )
    
    def __del__( self ):
        pass
    
    
    # Virtual event handlers, overide them in your derived class
    def btn_time_setOnButtonClick( self, event ):
        self.Destroy()
        event.Skip()
    
    def btn_time_cancelOnButtonClick( self, event ):
        self.Destroy()
        event.Skip()
    



#     
# app=wx.App()
# dialog_pressmode(None).Show()
# app.MainLoop()

