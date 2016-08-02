# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

from src.RomteControlDialog import control_IQ, control_press,control_sweep
###########################################################################
## Class remoteControl
###########################################################################

class dialog_remoteCtrl ( wx.Dialog ):
    
    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"远程控制", pos = wx.DefaultPosition, size = wx.Size( 249,297 ), style = wx.DEFAULT_DIALOG_STYLE )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        gSizer3 = wx.GridSizer( 6, 1, 0, 0 )
        
        
        gSizer3.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        radio_remote_controlChoices = [ u"扫频接收控制", u"定频接收控制", u"压制发射控制" ]
        self.radio_remote_control = wx.RadioBox( self, wx.ID_ANY, u"远程控制", wx.DefaultPosition, wx.Size( 150,-1 ), radio_remote_controlChoices, 1, wx.RA_SPECIFY_COLS )
        self.radio_remote_control.SetSelection( 2 )
        gSizer3.Add( self.radio_remote_control, 0, wx.ALL, 5 )
        
        
        gSizer3.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        
        gSizer3.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.btn_remote_ctrl = wx.Button( self, wx.ID_ANY, u"确定", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer3.Add( self.btn_remote_ctrl, 0, wx.ALL, 5 )
        
        
        self.SetSizer( gSizer3 )
        self.Layout()
        
        self.Centre( wx.BOTH )
        
        # Connect Events
        self.btn_remote_ctrl.Bind( wx.EVT_BUTTON, self.btn_remote_ctrlOnButtonClick )
    
    def __del__( self ):
        pass
    
    
    # Virtual event handlers, overide them in your derived class
    def btn_remote_ctrlOnButtonClick( self, event ):
        index=self.radio_remote_control.GetSelection()
        if(index==0):
            dlg=control_sweep.ChangeAnotherSweep()
            dlg.ShowModal()
        elif(index==1):
            dlg=control_IQ.ChangeAnotherIQ()
            dlg.ShowModal()
        else:
            dlg=control_press.ChangeAnotherPress()
            dlg.ShowModal()
        event.Skip()
    


    
    

#     
# app=wx.App()
# remoteControl(None).Show()
# app.MainLoop()