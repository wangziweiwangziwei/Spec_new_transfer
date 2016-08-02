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

class dialog_download ( wx.Dialog ):
    
    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"请选择本地保存路径", pos = wx.DefaultPosition, size = wx.Size( 288,186 ), style = wx.DEFAULT_DIALOG_STYLE )
        
        
        #######################
        
        self.isValid=0
        ##########################
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        gSizer1 = wx.GridSizer( 3, 2, 0, 0 )
        
        self.m_dirPick = wx.DirPickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.Size( 260,-1 ), wx.DIRP_DEFAULT_STYLE )
        gSizer1.Add( self.m_dirPick, 0, wx.ALL, 5 )
        
        
        gSizer1.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.m_btn_ok = wx.Button( self, wx.ID_ANY, u"确定", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer1.Add( self.m_btn_ok, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        
        
        self.SetSizer( gSizer1 )
        self.Layout()
        
        self.Centre( wx.BOTH )
        
        # Connect Events
        self.m_btn_ok.Bind( wx.EVT_BUTTON, self.m_btn_okOnButtonClick )
    
    def __del__( self ):
        pass
    
    
   
    # Virtual event handlers, overide them in your derived class
    def m_btn_okOnButtonClick( self, event ):
        self.isValid=1
        self.Destroy()
        
    

