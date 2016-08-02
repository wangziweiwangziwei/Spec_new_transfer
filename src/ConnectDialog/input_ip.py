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
## Class MyDialog1
###########################################################################

class MyDialog1 ( wx.Dialog ):

    def __init__( self, parent ):


        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"设置服务器连接参数", pos = wx.DefaultPosition, size = wx.Size( 336,231 ), style = wx.DEFAULT_DIALOG_STYLE )


        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        self.isValid=0

        fgSizer1 = wx.FlexGridSizer( 6, 4, 0, 0 )
        fgSizer1.SetFlexibleDirection( wx.BOTH )
        fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

        self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"监控服务器-", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        fgSizer1.Add( self.m_staticText1, 0, wx.ALL, 5 )


        fgSizer1.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )


        fgSizer1.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )


        fgSizer1.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"IP 地址:", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
        self.m_staticText2.Wrap( -1 )
        fgSizer1.Add( self.m_staticText2, 0, wx.ALL, 5 )

        self.ip_moni = wx.TextCtrl( self, wx.ID_ANY, u"27.17.8.142", wx.DefaultPosition, wx.Size( 100,-1 ), 0 )
        fgSizer1.Add( self.ip_moni, 0, wx.ALIGN_LEFT|wx.ALL, 5 )

        self.m_staticText3 = wx.StaticText( self, wx.ID_ANY, u"端口：", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText3.Wrap( -1 )
        fgSizer1.Add( self.m_staticText3, 0, wx.ALL, 5 )

        self.port_moni = wx.TextCtrl( self, wx.ID_ANY, u"9000", wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
        fgSizer1.Add( self.port_moni, 0, wx.ALL, 5 )

        self.m_staticText11 = wx.StaticText( self, wx.ID_ANY, u"监控服务器-", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText11.Wrap( -1 )
        fgSizer1.Add( self.m_staticText11, 0, wx.ALL, 5 )


        fgSizer1.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )


        fgSizer1.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )


        fgSizer1.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_staticText21 = wx.StaticText( self, wx.ID_ANY, u"IP 地址:", wx.DefaultPosition, wx.Size( 50,-1 ), 0 )
        self.m_staticText21.Wrap( -1 )
        fgSizer1.Add( self.m_staticText21, 0, wx.ALL, 5 )

        self.ip_file = wx.TextCtrl( self, wx.ID_ANY, u"27.17.8.142", wx.DefaultPosition, wx.Size( 100,-1 ), 0 )
        fgSizer1.Add( self.ip_file, 0, wx.ALL, 5 )

        self.m_staticText31 = wx.StaticText( self, wx.ID_ANY, u"端口：", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText31.Wrap( -1 )
        fgSizer1.Add( self.m_staticText31, 0, wx.ALL, 5 )

        self.port_file = wx.TextCtrl( self, wx.ID_ANY, u"9988", wx.DefaultPosition, wx.Size( 40,-1 ), 0 )
        fgSizer1.Add( self.port_file, 0, wx.ALL, 5 )


        fgSizer1.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )


        fgSizer1.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )


        fgSizer1.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )


        fgSizer1.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_button11 = wx.Button( self, wx.ID_ANY, u"确定", wx.DefaultPosition, wx.Size( 80,25 ), 0 )
        fgSizer1.Add( self.m_button11, 0, wx.ALL, 5 )


        self.SetSizer( fgSizer1 )
        self.Layout()

        self.Centre( wx.BOTH )

        # Connect Events
        self.m_button11.Bind( wx.EVT_BUTTON, self.m_button11OnButtonClick )

    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class
    def m_button11OnButtonClick( self, event ):
        self.isValid=1
        self.Close()



