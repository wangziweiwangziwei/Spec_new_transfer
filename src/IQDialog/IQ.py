# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc


from src.Wave.IQWave import WaveIQ

from src.Package.package import IQParaSet,IQFreqSet, \
FrameHeader,FrameTail,Hour5bit,CentreFreq,Query,RecvGainSet

from src.CommonUse.staticVar import  staticVar
import time 
from src.Thread import thread_recv_iq
###########################################################################
## Class MyDialog1
###########################################################################

class dialog_IQ ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"定频接收", pos = wx.DefaultPosition, size = wx.Size( 387,392 ), style = wx.DEFAULT_DIALOG_STYLE )

        ##############################
        self.id=staticVar.getid()
        self.lowid=self.id&0x00FF
        self.highid=self.id>>8
        self.tail=FrameTail(0,0,0xAA)
        self.outPoint=staticVar.outPoint

        ###############################
        self.parent=parent
        #### show #########
        self.show_recv_set=self.parent.show_recv_set
        self.byte_to_package=self.parent.byte_to_package



        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        gSizer1 = wx.GridSizer( 1, 1, 0, 0 )

        self.m_notebook1 = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )

        self.m_notebook1.SetFont(wx.Font(10, wx.ROMAN, wx.NORMAL, wx.LIGHT, underline=False, faceName=u"微软雅黑",
                                         encoding=wx.FONTENCODING_DEFAULT))

        self.m_panel1 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        gSizer2 = wx.GridSizer( 9, 3, 0, 0 )


        # gSizer2.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        #
        #
        # gSizer2.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        #
        #
        # gSizer2.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_check_freq1 = wx.CheckBox( self.m_panel1, wx.ID_ANY, u"第一个中心频率", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer2.Add( self.m_check_freq1, 0, wx.ALL, 5 )

        self.m_text_freq1 = wx.TextCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer2.Add( self.m_text_freq1, 0, wx.ALL, 5 )

        self.m_staticText6 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"MHz", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText6.Wrap( -1 )
        gSizer2.Add( self.m_staticText6, 0, wx.ALL, 5 )

        self.m_check_freq2 = wx.CheckBox( self.m_panel1, wx.ID_ANY, u"第二个中心频率", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer2.Add( self.m_check_freq2, 0, wx.ALL, 5 )

        self.m_text_freq2 = wx.TextCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer2.Add( self.m_text_freq2, 0, wx.ALL, 5 )

        self.m_staticText7 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"MHz", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText7.Wrap( -1 )
        gSizer2.Add( self.m_staticText7, 0, wx.ALL, 5 )

        self.m_check_freq3 = wx.CheckBox( self.m_panel1, wx.ID_ANY, u"第三个中心频率", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer2.Add( self.m_check_freq3, 0, wx.ALL, 5 )

        self.m_text_freq3 = wx.TextCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer2.Add( self.m_text_freq3, 0, wx.ALL, 5 )

        self.m_staticText8 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"MHz", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText8.Wrap( -1 )
        gSizer2.Add( self.m_staticText8, 0, wx.ALL, 5 )

        self.m_staticText11 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"IQ 带宽/数据率", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText11.Wrap( -1 )
        gSizer2.Add( self.m_staticText11, 0, wx.ALL, 5 )

        m_choice_bwChoices = [ u"5", u"2.5", u"1.25", u"0.625", u"0.125" ]
        self.m_choice_bw = wx.Choice( self.m_panel1, wx.ID_ANY, wx.DefaultPosition, wx.Size( 110,-1 ), m_choice_bwChoices, 0 )
        self.m_choice_bw.SetSelection( 0 )
        gSizer2.Add( self.m_choice_bw, 0, wx.ALL, 5 )

        self.m_staticText12 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"MHz", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText12.Wrap( -1 )
        gSizer2.Add( self.m_staticText12, 0, wx.ALL, 5 )

        self.m_staticText13 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"上传数据块个数", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText13.Wrap( -1 )
        gSizer2.Add( self.m_staticText13, 0, wx.ALL, 5 )

        self.m_text_up_num = wx.TextCtrl( self.m_panel1, wx.ID_ANY, u"1", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer2.Add( self.m_text_up_num, 0, wx.ALL, 5 )

        self.m_staticText14 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"(<=256)", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText14.Wrap( -1 )
        gSizer2.Add( self.m_staticText14, 0, wx.ALL, 5 )

        self.m_staticText15 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"  延时时间", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText15.Wrap( -1 )
        gSizer2.Add( self.m_staticText15, 0, wx.ALL, 5 )

        self.m_text_dtime = wx.TextCtrl( self.m_panel1, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer2.Add( self.m_text_dtime, 0, wx.ALL, 5 )

        self.m_staticText16 = wx.StaticText( self.m_panel1, wx.ID_ANY, u"s", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText16.Wrap( -1 )
        gSizer2.Add( self.m_staticText16, 0, wx.ALL, 5 )

        self.m_staticText19 = wx.StaticText(self.m_panel1, wx.ID_ANY, u"接收增益（dB）", wx.DefaultPosition, wx.DefaultSize,
                                            0)
        self.m_staticText19.Wrap(-1)
        gSizer2.Add(self.m_staticText19, 0, wx.ALIGN_CENTER | wx.ALIGN_RIGHT | wx.ALIGN_TOP | wx.ALL, 5)

        self.m_slider_gain = wx.Slider(self.m_panel1, wx.ID_ANY, 7, -1, 73, wx.Point(-1, -1), wx.Size(150, 20),
                                       wx.SL_HORIZONTAL | wx.SL_LABELS | wx.SL_SELRANGE)
        gSizer2.Add(self.m_slider_gain, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        gSizer2.AddSpacer((0, 0), 1, wx.EXPAND, 5)

        gSizer2.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )


        gSizer2.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )


        gSizer2.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_btn_set = wx.Button( self.m_panel1, wx.ID_ANY, u"确定", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer2.Add( self.m_btn_set, 0, wx.ALL, 5 )

        self.m_btn_cancel = wx.Button( self.m_panel1, wx.ID_ANY, u"取消", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer2.Add( self.m_btn_cancel, 0, wx.ALL, 5 )

        self.m_panel1.SetSizer( gSizer2 )
        self.m_panel1.Layout()
        gSizer2.Fit( self.m_panel1 )
        self.m_notebook1.AddPage( self.m_panel1, u"定频接收参数", False )
        # self.m_panel2 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.Size( 200,-1 ), wx.TAB_TRAVERSAL )
        # gSizer4 = wx.GridSizer( 2, 2, 0, 0 )
        #


        # self.btn_ok_param = wx.Button( self.m_panel2, wx.ID_ANY, u"确定", wx.DefaultPosition, wx.DefaultSize, 0 )
        # gSizer4.Add( self.btn_ok_param, 0, wx.ALIGN_CENTER|wx.ALL, 5 )
        #
        # self.btn_cancel_param = wx.Button( self.m_panel2, wx.ID_ANY, u"取消", wx.DefaultPosition, wx.DefaultSize, 0 )
        # gSizer4.Add( self.btn_cancel_param, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


        # self.m_panel2.SetSizer( gSizer4 )
        # self.m_panel2.Layout()
        # self.m_notebook1.AddPage( self.m_panel2, u"参数设置", False )
        # self.m_panel3 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        # gSizer5 = wx.GridSizer( 8, 2, 0, 0 )
        #
        # gSizer5.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        # gSizer5.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        #
        # self.m_check_wave = wx.CheckBox( self.m_panel3, wx.ID_ANY, u"波形图", wx.DefaultPosition, wx.DefaultSize, 0 )
        # gSizer5.Add( self.m_check_wave, 0, wx.ALL, 5 )
        #
        #
        #
        # self.m_check_spec = wx.CheckBox( self.m_panel3, wx.ID_ANY, u"功率谱", wx.DefaultPosition, wx.DefaultSize, 0 )
        # gSizer5.Add( self.m_check_spec, 0, wx.ALL, 5 )
        #
        # self.m_check_water = wx.CheckBox( self.m_panel3, wx.ID_ANY, u"瀑布图", wx.DefaultPosition, wx.DefaultSize, 0 )
        # gSizer5.Add( self.m_check_water, 0, wx.ALL, 5 )
        #
        # self.m_check_CCDF = wx.CheckBox( self.m_panel3, wx.ID_ANY, u"CCDF", wx.DefaultPosition, wx.DefaultSize, 0 )
        # gSizer5.Add( self.m_check_CCDF, 0, wx.ALL, 5 )
        #
        #
        # self.m_check_eye = wx.CheckBox( self.m_panel3, wx.ID_ANY, u"眼图", wx.DefaultPosition, wx.DefaultSize, 0 )
        # gSizer5.Add( self.m_check_eye, 0, wx.ALL, 5 )
        #
        # self.m_check_constel = wx.CheckBox( self.m_panel3, wx.ID_ANY, u"星座图", wx.DefaultPosition, wx.DefaultSize, 0 )
        # gSizer5.Add( self.m_check_constel, 0, wx.ALL, 5 )
        #
        #
        #
        # self.btn_display = wx.Button( self.m_panel3, wx.ID_ANY, u"确定", wx.DefaultPosition, wx.DefaultSize, 0 )
        # gSizer5.Add( self.btn_display, 0, wx.ALL, 5 )
        #
        # self.btn_display_cancel = wx.Button( self.m_panel3, wx.ID_ANY, u"取消", wx.DefaultPosition, wx.DefaultSize, 0 )
        # gSizer5.Add( self.btn_display_cancel, 0, wx.ALL, 5 )
        #
        #
        # self.m_panel3.SetSizer( gSizer5 )
        # self.m_panel3.Layout()
        # gSizer5.Fit( self.m_panel3 )
        # self.m_notebook1.AddPage( self.m_panel3, u"窗口显示", False )
        self.m_panel4 = wx.Panel( self.m_notebook1, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        gSizer6 = wx.GridSizer( 5, 1, 0, 0 )


        gSizer6.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )

        m_radio_chooseChoices = [ u"定频中心频率", u"定频带宽",u"定频上传数据块个数" ]
        self.m_radio_choose = wx.RadioBox( self.m_panel4, wx.ID_ANY, u"查询项", wx.DefaultPosition, wx.DefaultSize, m_radio_chooseChoices, 1, wx.RA_SPECIFY_COLS )
        self.m_radio_choose.SetSelection( 0 )
        gSizer6.Add( self.m_radio_choose, 0, wx.ALL, 5 )


        gSizer6.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )

        self.m_btn_query = wx.Button( self.m_panel4, wx.ID_ANY, u"查询", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer6.Add( self.m_btn_query, 0, wx.ALL, 5 )


        self.m_panel4.SetSizer( gSizer6 )
        self.m_panel4.Layout()
        gSizer6.Fit( self.m_panel4 )
        self.m_notebook1.AddPage( self.m_panel4, u"查询", True )

        gSizer1.Add( self.m_notebook1, 1, wx.EXPAND |wx.ALL, 5 )


        self.SetSizer( gSizer1 )
        self.Layout()

        self.Centre( wx.BOTH )

        #Events
        self.m_btn_set.Bind( wx.EVT_BUTTON, self.m_btn_setOnButtonClick )
        # self.btn_ok_param.Bind(wx.EVT_BUTTON, self.btn_ok_paramOnButtonClick)
        # self.btn_display.Bind(wx.EVT_BUTTON, self.btn_displayOnButtonClick)
        self.m_btn_query.Bind(wx.EVT_BUTTON,self.m_btn_queryOnButtonClick)
    def __del__( self ):
        pass

    def m_btn_setOnButtonClick(self,event):

        ################# 增益设置 ####################

        Gain=int(self.m_slider_gain.GetValue())
        if(Gain!=staticVar.getRecvGain()):

            header=FrameHeader(0x55,0x04,self.lowid, self.highid)
            gainSet= RecvGainSet()
            gainSet.CommonHeader=header
            gainSet.RecvGain=Gain+3
            gainSet.CommonTail=self.tail
            self.outPoint.write(bytearray(gainSet))
            staticVar.setRecvGain(Gain)
            
        ##################################
        self.parent.start_local_iq=1
        ###########   定频参数设置     ##########
        iqPara=IQParaSet()
        bandWidth=int(self.m_choice_bw.GetSelection())
        uploadNum=int(self.m_text_up_num.GetValue())
        delayTime=int(self.m_text_dtime.GetValue())

        curTime=time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))

        iqPara.CommonHeader=FrameHeader(0x55,0x07,self.highid,self.lowid)
        iqPara.CommonTail=self.tail
        iqPara.BandWidth=bandWidth+1
        iqPara.DataRate=bandWidth+1
        iqPara.UploadNum=uploadNum
        Year=int(curTime[0:4])
        Month=int(curTime[4:6])
        Day=int(curTime[6:8])
        Hour=int(curTime[8:10])
        Min=int(curTime[10:12])
        Second=int(curTime[12:14])+delayTime
        if(Second>=60):
            Min+=1
            Second-=60
        #######  转UTC 格式 ########
        Hour-=8

        HourStruct=Hour5bit(Hour,0)

        ############################
        iqPara.Time.HighYear=Year>>4
        iqPara.Time.LowYear=Year&0x00F
        iqPara.Time.Month=Month
        iqPara.Time.Day=Day
        iqPara.Time.HighHour=HourStruct.Hour>>2
        iqPara.Time.LowHour=HourStruct.Hour&0x03
        iqPara.Time.Minute=Min
        iqPara.Time.Second=Second
        self.outPoint.write(bytearray(iqPara))


        ########### 定频中心频率设置 ############

        listfreq=[]
        if(self.m_check_freq1.GetValue()):
            freq1=int(self.m_text_freq1.GetValue())
            listfreq.append(freq1)

        if(self.m_check_freq2.GetValue()):
            freq2=int(self.m_text_freq2.GetValue())
            listfreq.append(freq2)
        if(self.m_check_freq3.GetValue()):
            freq3=int(self.m_text_freq3.GetValue())
            listfreq.append(freq3)

        iqFreq=IQFreqSet()
        iqFreq.CommonHeader=FrameHeader(0x55,0x02,self.highid,self.lowid)
        iqFreq.CommonTail=self.tail
        iqFreq.FreqNum=len(listfreq)


        for i in xrange(len(listfreq)):
            array=self.FreqToByte(listfreq[i])
            iqFreq.FreqArray[i]=CentreFreq(array[0],array[1],array[2],array[3])


        self.outPoint.write(bytearray(iqFreq))


        for i in  bytearray(iqPara):
            print i,
            print
        for i in bytearray(iqFreq):
            print i,






        ################# show ########################

        # self.show_recv_set.ShowIQPara(iqPara)
        # self.show_recv_set.ShowIQCentreFreq(iqFreq)


        self.Close()
        ######################### 开启iq 接收线程 #################
        time.sleep(delayTime-1)

        thread=thread_recv_iq.ReceiveIQThread(self.parent)

        thread.start()


    def FreqToByte(self,freq):
        freqInt=int(freq)
        freqFloat=freq-freqInt
        freqF=int(freqFloat*2**10)
        highFreqInt=freqInt>>6
        lowFreqInt=freqInt&0x003F
        highFreqFrac=freqF>>8
        lowFreqFrac=freqF&0x0FF
        return (highFreqInt,highFreqFrac,lowFreqInt,lowFreqFrac)


    # def btn_ok_paramOnButtonClick(self,event):



    # def btn_displayOnButtonClick(self,event):
    #     if(self.m_check_wave.GetValue()):
    #         self.parent.WaveFrame=WaveIQ(self.parent,u"定频波形图                ")
    #         self.parent.WaveFrame.Activate()
    #         self.Destroy()
# 		if(self.m_check_constel.GetValue() or self.m_check_eye.GetValue()):
# 			dlg=dialog_demod()
# 			dlg.ShowModal()

    def m_btn_queryOnButtonClick(self,event):
        index=self.m_radio_choose.GetSelection()

        if(index==0):
            self.QuerySend(0x12)

            li=self.byte_to_package.ReceiveRecv()
            obj=self.byte_to_package.ByteToIQFreq(li)
            self.show_recv_set.ShowIQCentreFreq(obj,0)

        else:
            self.QuerySend(0x17)

            li=self.byte_to_package.ReceiveRecv()
            obj=self.byte_to_package.ByteToIQPara(li)
            self.show_recv_set.ShowIQPara(obj)


        event.Skip()

    def QuerySend(self,funcPara):
        query=Query()
        query.CommonHeader=FrameHeader(0x55,funcPara,self.lowid,self.highid)
        query.CommonTail=self.tail
        self.outPoint.write(bytearray(query))
# 
# app=wx.App()
# dialog_IQ(None).Show()
# app.MainLoop()
