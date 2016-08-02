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

class dialog_upload ( wx.Dialog ):
    
    def __init__( self, parent ):
        
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 272,248 ), style = wx.DEFAULT_DIALOG_STYLE )
        
        ####自定义变量######
        self.isValid=0
        
        
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        gSizer1 = wx.GridSizer( 6, 2, 0, 0 )
        
        
        gSizer1.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        
        gSizer1.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"上传扫频文件个数：", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )
        gSizer1.Add( self.m_staticText1, 0, wx.ALL, 5 )
        
        self.m_text_number = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer1.Add( self.m_text_number, 0, wx.ALL, 5 )
        
        self.m_radio_extract = wx.RadioButton( self, wx.ID_ANY, u"抽取上传    倍率：", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer1.Add( self.m_radio_extract, 0, wx.ALL, 5 )
        
        self.m_text_extract_m = wx.TextCtrl( self, wx.ID_ANY, u"1", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer1.Add( self.m_text_extract_m, 0, wx.ALL, 5 )
        
        self.m_radioBtn2 = wx.RadioButton( self, wx.ID_ANY, u"自动上传   门限: ", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer1.Add( self.m_radioBtn2, 0, wx.ALL, 5 )
        
        m_choice_change_thresChoices = [ u"10", u"20" ]
        self.m_choice_change_thres = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 110,-1 ), m_choice_change_thresChoices, 0 )
        self.m_choice_change_thres.SetSelection( 1 )
        gSizer1.Add( self.m_choice_change_thres, 0, wx.ALL, 5 )
        
        self.m_btn_ok = wx.Button( self, wx.ID_ANY, u"确定", wx.DefaultPosition, wx.Size( 80,25 ), 0 )
        gSizer1.Add( self.m_btn_ok, 0, wx.ALL, 5 )
        
        
        self.SetSizer( gSizer1 )
        self.Layout()
        
        self.Centre( wx.BOTH )
        
        # Connect Events
        self.m_radio_extract.Bind( wx.EVT_RADIOBUTTON, self.m_radio_extractOnRadioButton )
        self.m_radioBtn2.Bind( wx.EVT_RADIOBUTTON, self.m_radioBtn2OnRadioButton )
        self.m_btn_ok.Bind( wx.EVT_BUTTON, self.m_btn_okOnButtonClick )
    
    def __del__( self ):
        pass
    
    
    # Virtual event handlers, overide them in your derived class
    def m_radio_extractOnRadioButton( self, event ):
        self.m_text_extract_m.Enable(True)
        self.m_choice_change_thres.Enable(False)
        event.Skip()
    
    def m_radioBtn2OnRadioButton( self, event ):
        self.m_text_extract_m.Enable(False)
        self.m_choice_change_thres.Enable(True)
        event.Skip()
    
    
    def m_btn_okOnButtonClick( self, event ):
        self.isValid=1
        self.Destroy()
        event.Skip()
      


