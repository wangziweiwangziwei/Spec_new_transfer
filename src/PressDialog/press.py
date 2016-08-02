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

# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

from src.PressDialog.pressmode import dialog_pressmode
from src.CommonUse.staticVar import  staticVar
from src.Package.package import FrameHeader,FrameTail,PressFreqSet,PressParaSet, \
   CentreFreq,SendWeakSet,Query
from src.CommonUse.press_hand import press_hand
###########################################################################
## Class MyDialog2
###########################################################################

class dialog_press ( wx.Dialog ):
    
    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"压制发射", pos = wx.DefaultPosition, size = wx.Size( 392,382 ), style = wx.DEFAULT_DIALOG_STYLE )
        
        ###########################################
        self.T1=0
        self.T2=0
        self.T3=0
        self.T4=0
        
        self.press_mode=5
        
        
        self.id=staticVar.getid()
        self.lowid=self.id&0x00FF
        self.highid=self.id>>8
        self.tail=FrameTail(0,0,0xAA)
        self.outPoint=staticVar.outPoint

        #### show ######
        
        self.parent= parent  
             
        self.show_recv_set= self.parent.show_recv_set
        self.byte_to_package= self.parent.byte_to_package
         
            
        ###########################################
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        gSizer7 = wx.GridSizer( 1, 1, 0, 0 )
        
        self.m_notebook2 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_notebook2.SetFont(wx.Font(10, wx.ROMAN, wx.NORMAL, wx.LIGHT, underline=False, faceName=u"微软雅黑",
                                         encoding=wx.FONTENCODING_DEFAULT))

        self.m_panel7 = wx.Panel( self.m_notebook2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        
        
        gSizer8 = wx.GridSizer( 8, 2, 0, 0 )
        
        
        gSizer8.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        
        gSizer8.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.m_staticText3 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"压制设置", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText3.Wrap( -1 )
        gSizer8.Add( self.m_staticText3, 0, wx.ALL, 5 )
        
        m_press_setChoices = [ u"结束压制", u"单频点自动", u"单频点手动", u"双频点自动", u"双频点手动" ]
        self.m_press_set = wx.Choice( self.m_panel7, wx.ID_ANY, wx.DefaultPosition, wx.Size( 140,-1 ), m_press_setChoices, 0 )
        self.m_press_set.SetSelection( 0 )
        gSizer8.Add( self.m_press_set, 0, wx.ALL, 5 )
        
        self.m_staticText4 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"压制信号类型", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText4.Wrap( -1 )
        gSizer8.Add( self.m_staticText4, 0, wx.ALL, 5 )
        
        m_press_signaltypeChoices = [ u"单频正弦波信号", u"等幅多频信号", u"噪声调频信号", u"数字射频储存DRM信号" ]
        self.m_press_signaltype = wx.Choice( self.m_panel7, wx.ID_ANY, wx.DefaultPosition, wx.Size( 140,-1 ), m_press_signaltypeChoices, 0 )
        self.m_press_signaltype.SetSelection( 0 )
        gSizer8.Add( self.m_press_signaltype, 0, wx.ALL, 5 )
        
        self.m_staticText5 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"压制带宽", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText5.Wrap( -1 )
        gSizer8.Add( self.m_staticText5, 0, wx.ALL, 5 )
        
        m_press_bwChoices = [ u"单谱线（正弦波）", u"（等幅多边,噪声调频）", u"直接IQ调制发射（DRM）" ]
        self.m_press_bw = wx.Choice( self.m_panel7, wx.ID_ANY, wx.DefaultPosition, wx.Size( 140,-1 ), m_press_bwChoices, 0 )
        self.m_press_bw.SetSelection( 0 )
        gSizer8.Add( self.m_press_bw, 0, wx.ALL, 5 )
        
        self.m_staticText6 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"压制频率1（MHz）", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText6.Wrap( -1 )
        gSizer8.Add( self.m_staticText6, 0, wx.ALL, 5 )
        
        self.m_freq1 = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer8.Add( self.m_freq1, 0, wx.ALL, 5 )
        
        self.m_staticText7 = wx.StaticText( self.m_panel7, wx.ID_ANY, u"压制频率2（MHz）", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText7.Wrap( -1 )
        gSizer8.Add( self.m_staticText7, 0, wx.ALL, 5 )
        
        self.m_freq2 = wx.TextCtrl( self.m_panel7, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer8.Add( self.m_freq2, 0, wx.ALL, 5 )
        
        self.btn_press_set = wx.Button( self.m_panel7, wx.ID_ANY, u"设置", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer8.Add( self.btn_press_set, 0, wx.ALL, 5 )
        
        self.btn_press_cancel = wx.Button( self.m_panel7, wx.ID_ANY, u"取消", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer8.Add( self.btn_press_cancel, 0, wx.ALL, 5 )
        
        
        self.m_panel7.SetSizer( gSizer8 )
        self.m_panel7.Layout()
        gSizer8.Fit( self.m_panel7 )
        self.m_notebook2.AddPage( self.m_panel7, u"压制设置", False )
        self.m_panel8 = wx.Panel( self.m_notebook2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        gSizer4 = wx.GridSizer( 6, 2, 0, 0 )
        
        
        gSizer4.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        
        gSizer4.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.m_staticText71 = wx.StaticText( self.m_panel8, wx.ID_ANY, u"压制发射衰减（dB）", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText71.Wrap( -1 )
        gSizer4.Add( self.m_staticText71, 0, wx.ALL, 5 )
        
        self.m_slider_weak = wx.Slider( self.m_panel8, wx.ID_ANY, 0, 0, 89, wx.DefaultPosition, wx.Size( 150,-1 ), wx.SL_HORIZONTAL|wx.SL_LABELS|wx.SL_SELRANGE )
        gSizer4.Add( self.m_slider_weak, 0, wx.ALL, 5 )
        
        self.btn_param_set = wx.Button( self.m_panel8, wx.ID_ANY, u"设置", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer4.Add( self.btn_param_set, 0, wx.ALL, 5 )
        
        self.m_button7 = wx.Button( self.m_panel8, wx.ID_ANY, u"取消", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer4.Add( self.m_button7, 0, wx.ALL, 5 )
        
        
        self.m_panel8.SetSizer( gSizer4 )
        self.m_panel8.Layout()
        gSizer4.Fit( self.m_panel8 )
        self.m_notebook2.AddPage( self.m_panel8, u"参数设置", True )
        self.m_panel9 = wx.Panel( self.m_notebook2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        gSizer71 = wx.GridSizer( 7, 1, 0, 0 )
        
        
        Choices = [ u"压制发射衰减", u"压制中心频率", u"压制模式查询" ]
        self.radio_pressquery= wx.RadioBox( self.m_panel9, wx.ID_ANY, u"查询项", wx.DefaultPosition, wx.Size( 120,140 ),
        Choices, 1, wx.RA_SPECIFY_COLS )
        self.radio_pressquery.SetSelection( 2 )
        gSizer71.Add( self.radio_pressquery, 0, wx.ALL, 5 )
        
        
        gSizer71.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        
        gSizer71.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        
        gSizer71.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.btn_press_query = wx.Button( self.m_panel9, wx.ID_ANY, u"查询", wx.DefaultPosition, wx.DefaultSize, 0 )
        # gSizer71.Add( self.btn_press_query, 0, wx.ALL, 5 )

        gSizer71.Add(self.btn_press_query, 0, wx.ALIGN_BOTTOM | wx.ALIGN_CENTER, 5)

        self.m_panel9.SetSizer( gSizer71 )
        self.m_panel9.Layout()
        gSizer71.Fit( self.m_panel9 )
        self.m_notebook2.AddPage( self.m_panel9, u"查询", False )
        
        gSizer7.Add( self.m_notebook2, 1, wx.EXPAND |wx.ALL, 5 )
        
        
        self.SetSizer( gSizer7 )
        self.Layout()
        
        self.Centre( wx.BOTH )
        # Connect Events
        self.m_press_set.Bind( wx.EVT_CHOICE, self.m_press_setOnChoice )  
        
        self.btn_press_set.Bind( wx.EVT_BUTTON, self.btn_press_setOnChoice)
        self.btn_param_set.Bind( wx.EVT_BUTTON, self.btn_param_setOnChoice)
        self.btn_press_query.Bind( wx.EVT_BUTTON, self.btn_press_queryOnChoice)
    def __del__( self ):
        pass
    
    
    # Virtual event handlers, overide them in your derived class
    def m_press_setOnChoice( self, event ):
        
        
        index=self.m_press_set.GetSelection()
        if(index<5):
            self.press_mode=index 
      
            if(index==1 or index==2):
                dlg=dialog_pressmode(self)
                dlg.m_text_T3.Enable(False)
                dlg.m_text_T4.Enable(False)
                dlg.ShowModal()
                t1=dlg.m_text_T1.GetValue()
                t2=dlg.m_text_T2.GetValue()
                if(t1 and t2):
                    self.T1=int(t1)
                    self.T2=int(t2)
                
                
                    
            elif(index==3 or index==4):
                dlg=dialog_pressmode(self)
                dlg.ShowModal()
                t1=dlg.m_text_T1.GetValue()
                t2=dlg.m_text_T2.GetValue()
                t3=dlg.m_text_T3.GetValue()
                t4=dlg.m_text_T4.GetValue()
                if(t1 and t2 and t3 and t4):
                    self.T1=int(t1)
                    self.T2=int(t2)
                    self.T3=int(t3)
                    self.T4=int(t4)
                
            else:
                pass
            
        
        event.Skip()
    
    def btn_press_setOnChoice(self,event):
    
        ###压制参数设置#################
        
        pressSet=PressParaSet()   
        
        pressSet.PressMode=self.press_mode
        pressSet.CommonHeader=FrameHeader(0x55,0x08,self.highid,self.lowid)
        pressSet.PressSignal=int(self.m_press_signaltype.GetSelection())+1
        pressSet.PressSignalBandWidth=int(self.m_press_bw.GetSelection())+1
        pressSet.CommonTail=self.tail
        if(self.press_mode<5):
            pressSet.HighT1=self.T1>>8
            pressSet.LowT1=self.T1&0x00FF
            pressSet.HighT2=self.T2>>8
            pressSet.LowT2= self.T2&0x00FF
            
            PressFreq1=float(self.m_freq1.GetValue())
        
            if(self.press_mode>2):
                pressSet.HighT3=self.T3>>8
                pressSet.LowT3=self.T3&0x00FF
                pressSet.HighT4=self.T4>>8
                pressSet.LowT4=self.T4&0x00FF 
                
                PressFreq2=float(self.m_freq2.GetValue())

        self.outPoint.write(bytearray(pressSet))

        ################# show ########################
        
        self.show_recv_set.ShowPressPara(pressSet)

        ##### 压制中心频率设置  ###########
        
        
        
        if(self.press_mode<5):
            
            pressFreqSet=PressFreqSet()
            pressFreqSet.CommonHeader=FrameHeader(0x55,0x03,self.highid,self.lowid)
            pressFreqSet.CommonTail=self.tail
            
            array1=self.FreqToByte(PressFreq1)
            pressFreqSet.PressNum=1
            pressFreqSet.FreqArray[0]=CentreFreq(array1[0],array1[1],array1[2],array1[3])   
            
            if(self.press_mode>2):
                array2=self.FreqToByte(PressFreq2)
                pressFreqSet.PressNum=2
                pressFreqSet.FreqArray[1]=CentreFreq(array2[0],array2[1],array2[2],array2[3])
            
            self.outPoint.write(bytearray(pressFreqSet))
            ##############  show  #####################
            self.show_recv_set.ShowPressFreq(pressFreqSet)
            
            if(self.press_mode==2 or self.press_mode==4):
                press_hand.set_press_hand(1)
                press_hand.set_press_set(pressSet)
                press_hand.set_press_freq(pressFreqSet)
            else:
                press_hand.set_press_hand(0)
        
        else:
            press_hand.set_press_hand(0)
                
                
                
    

        
    def FreqToByte(self,freq):
        freqInt=int(freq)
        freqFloat=freq-freqInt
        freqF=int(freqFloat*2**10)
        highFreqInt=freqInt>>6
        lowFreqInt=freqInt&0x003F
        highFreqFrac=freqF>>8
        lowFreqFrac=freqF&0x0FF
        return (highFreqInt,highFreqFrac,lowFreqInt,lowFreqFrac)    
        
        
    def btn_param_setOnChoice(self,event):
        
        SendWeak=SendWeakSet()
        SendWeak.CommonHeader=FrameHeader(0x55,0x05,self.highid,self.lowid)
        SendWeak.SendWeak=int(self.m_slider_weak.GetValue())
        SendWeak.CommonTail=self.tail
        self.outPoint.write(bytearray(SendWeak))
        
    def btn_press_queryOnChoice(self,event):
        index=self.radio_pressquery.GetSelection()
        
        if(index==0):
            self.QuerySend(0x15)
            
            li=self.byte_to_package.ReceiveRecv()
            obj=self.byte_to_package.ByteToSendWeak(li)
            self.show_recv_set.ShowSendWeak(obj)
            
        elif(index==1):
            self.QuerySend(0x13)
            
            li=self.byte_to_package.ReceiveRecv()
            obj=self.byte_to_package.ByteToPressFreq(li)
            self.show_recv_set.ShowPressFreq(obj,0)
        else:
            self.QuerySend(0x18)
            
            li=self.byte_to_package.ReceiveRecv()
            obj=self.byte_to_package.ByteToPressPara(li)
            self.show_recv_set.ShowPressPara(obj)
            

        event.Skip()

    def QuerySend(self,funcPara):
        query=Query()
        query.CommonHeader=FrameHeader(0x55,funcPara,self.lowid,self.highid)
        query.CommonTail=self.tail
        self.outPoint.write(bytearray(query))   

#     
# app=wx.App()
# Press(None).Show()
# app.MainLoop()
