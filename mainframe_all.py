# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################
import LoadFirm
import webbrowser
import wx
import wx.xrc
import wx.aui
import matplotlib
import Queue
import os
import time
import sys
import struct
import threading
from src.PressDialog.press import dialog_press
from src.PressDialog.pressmode import dialog_pressmode
from src.SweepDialog.sweep import dialog_sweep
from src.SinalAnalysis.signalAnalysis import SignalAnalysisDlg
from src.IQDialog.IQ import dialog_IQ
from src.MapDialog.map import dialog_map
from src.ConnectDialog import  input_ip
from src.RomteControlDialog.remote_control import dialog_remoteCtrl
from src.HistoryDisplayDialog.history_display import dialog_historydis
from src.FreqPlanDialog.freqplan import QueryFreqPlanDialog
from src.Spectrum import Spectrum_1
from src.CommonUse.staticVar import staticVar
from src.CommonUse.show_recv_and_set import ShowRecvAndSet
from src.CommonUse.byte_2_package import ByteToPackage
from src.CommonUse.connect import ServerCommunication

from src.CommonUse import configfpga
from src.CommonUse.timer import Timer

from src.DataBase import CreateAllTable

from src.Package.package import FrameHeader,FrameTail,ConnectServer,LonLatAltitude, Query,RecvGainSet

from threading import Thread
from src.Thread.thread_upload import SendFileThread
from src.Thread.thread_station import ReceiveServerData
from src.Thread.thread_recvfft import ReceiveFFTThread

###########################################################################
## Class MyFrame1
###########################################################################
from src.Package.logg import Log

class MainFrame ( wx.aui.AuiMDIParentFrame ):

    def __init__( self, parent ):
        wx.aui.AuiMDIParentFrame.__init__ ( self, parent, -1, title = wx.EmptyString,
        pos = wx.DefaultPosition, size = wx.Size( 887,545 ),
        style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        ''' 首先加载硬件的东西 '''

        # #################################

        staticVar.setid(41)  # 初始化id

        ############### hard wave config ######################
        value=0

        
        value = LoadFirm.load_firmware(r"D:\SlaveFifoSync5Bit.img")

        if (value == 1):
            raise Exception('can not load firm wave ')

        staticVar.initPort()  # 初始化硬件 端口

        # ############################################

        Log.init()  #日志初始化

        bmp = wx.Image(".//icons//title.jpg", wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        wx.SplashScreen(bmp, wx.SPLASH_CENTER_ON_SCREEN | wx.SPLASH_TIMEOUT,2000, None, -1)
        wx.Yield()

        #######################################
        matplotlib.rcParams["figure.facecolor"] = '#F2F5FA'
        matplotlib.rcParams["axes.facecolor"] = '0'
        matplotlib.rcParams["ytick.color"] = '0'
        matplotlib.rcParams["xtick.color"] = '0'
        matplotlib.rcParams["grid.color"] = 'w'
        matplotlib.rcParams["text.color"] = 'w'
        matplotlib.rcParams["figure.edgecolor"]="0"
        matplotlib.rcParams["xtick.labelsize"]=12
        matplotlib.rcParams["ytick.labelsize"]=12
        matplotlib.rcParams["axes.labelsize"]=14
        matplotlib.rcParams["grid.linestyle"]="-"
        matplotlib.rcParams["grid.linewidth"]=0.5
        matplotlib.rcParams["grid.color"]='#707070'

        #######################################
#         os.chdir("./apache-tomcat-7.0.68//bin//")
        os.chdir("./apache-tomcat-7.0.68//bin//")

        os.system("startup.bat")
        dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
        os.chdir(dirname)
        ########### 初始化变量  #################
        self.start_local_iq=0

        ########### 方便重连 的ip ##########
        self.ip_moni='27.17.8.142'
        self.ip_file='27.17.8.142'
        self.port_moni=9000
        self.port_file=9988



        self.frame_count=0    #打开的窗口数量#

        self.FreqMin=70
        self.FreqMax=5995

        self.tail=FrameTail(0,0,0xAA)
        #### 窗口################
        self.SpecFrame=Spectrum_1.Spec(self,1)
        self.SpecFrame.Activate()

        self.WaterFrame=None
        self.WaveFrame=None

        self.MapFrame=None
        self.TojiFrame = None

        self.HistorySpecFrame = None

        self.serverCom=ServerCommunication() #实例化服务器连接对象

        ########## 用于显示的  ############

        self.show_recv_set=ShowRecvAndSet(self)
        self.byte_to_package=ByteToPackage()

        self.GPS_list=[0]*9  ##记录GPS 查询信息，发送给服务器



        ####上传的队列############
        self.queueFFTUpload=Queue.Queue(maxsize=20)
        self.queueAbUpload=Queue.Queue(maxsize=20)
        self.queueIQUpload=Queue.Queue(maxsize=20)

        self.queueRequest=Queue.Queue(maxsize=20)


        # self.queuePoa=Queue.Queue(maxsize=20)
        # self.queueTdoa=Queue.Queue(maxsize=20)


        ###本地存储的队列#############
        self.queueFFTLocalSave=Queue.Queue()
        self.queueAbLocalSave=Queue.Queue()

        ### 画地图所使用的队列 （FFT的经纬度打包放进去）#########

        self.queueRouteMap=Queue.Queue()

        ## 窗口对象，以后就不创建了 ####
        self.dlg_sweep = 0
        self.dlg_connect = 0
        self.dlg_iq = 0
        self.dlg_press = 0
        self.dlg_map=0

        self.dlg_signal_fenxi=0




        ###### 创建数据表 #############
        if(not os.path.isfile( "C:\\DataBase\\PortSRF.db" )):
            os.mkdir(r'C:/DataBase/')
        CreateAllTable.create_all_table()
        if(not os.path.exists("./LocalData//Tdoa//")):
            os.makedirs('./LocalData//Tdoa//')
        if(not os.path.exists("./LocalData//Poa//")):
            os.makedirs('./LocalData//Poa//')





        ##### thread 管理 #########
        self.thread_recvfft=0

        self.thread_station=0
        self.thread_route_map=0
        
        '''
        if (configfpga.get_fx3_status()[0] == 0x04):
            pass
        else:
            configfpga.load_fpga('d:/top_sao.bit')

            wx.MessageBox('Config  OK!',
                          'Alert', wx.ICON_EXCLAMATION | wx.STAY_ON_TOP)
         '''            


        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )

        self.m_toolBar1 = self.CreateToolBar( wx.TB_HORIZONTAL|wx.TB_TEXT, wx.ID_ANY )
        self.m_toolBar1.SetFont(wx.Font(8, wx.ROMAN, wx.NORMAL, wx.LIGHT, underline=False, faceName=u"华文细黑 常规",
                                        encoding=wx.FONTENCODING_DEFAULT))

        self.m_start_hw = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"连接硬件", wx.Bitmap( ".//icons//pci.jpg", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"给硬件发送的命令，开启USB连接", wx.EmptyString, None )
        self.m_toolBar1.AddSeparator()

        self.m_toolBar1.AddSeparator()
        self.m_toolBar1.AddSeparator()

        self.m_connect = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"连接服务器", wx.Bitmap( ".//icons//server_connect.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"连接服务器以便发送服务请求", wx.EmptyString, None )

        self.m_toolBar1.AddSeparator()

        self.m_toolBar1.AddSeparator()
        self.m_toolBar1.AddSeparator()

        self.m_tool_sweep = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"扫频接收 ", wx.Bitmap( ".//icons//spectrum.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"设置扫频范围，扫频参数，查询工作状态", wx.EmptyString, None )

        self.m_toolBar1.AddSeparator()

        self.m_toolBar1.AddSeparator()
        self.m_toolBar1.AddSeparator()

        self.m_tool_iq = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"定频接收  ", wx.Bitmap( ".//icons//link_a.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"开启本地定频，查询工作状态", wx.EmptyString, None )

        self.m_toolBar1.AddSeparator()

        self.m_toolBar1.AddSeparator()
        self.m_toolBar1.AddSeparator()

        self.m_tool_press = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"压制发射", wx.Bitmap( ".//icons//pro24.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"启动压制命令，压制异常频点", wx.EmptyString, None )

        self.m_toolBar1.AddSeparator()

        self.m_toolBar1.AddSeparator()

        self.m_tool_map = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"地图服务", wx.Bitmap( ".//icons//map3.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"进行地图相关的服务请求设置，并查看地图结果显示", wx.EmptyString, None )

        self.m_toolBar1.AddSeparator()

        self.m_toolBar1.AddSeparator()
        self.m_toolBar1.AddSeparator()

        self.m_tool_freqplan = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"查询频率规划", wx.Bitmap( ".//icons//find1.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"查询具体频段的国家无线电频率规划信息", wx.EmptyString, None )

        self.m_toolBar1.AddSeparator()

        self.m_toolBar1.AddSeparator()
        self.m_toolBar1.AddSeparator()

        self.m_tool_remoteCtrl = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"远程控制", wx.Bitmap( ".//icons//remote.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"设置指定ID的远程终端的扫频参数，定频参数，或者压制参数", wx.EmptyString, None )

        self.m_toolBar1.AddSeparator()

        self.m_toolBar1.AddSeparator()
        self.m_toolBar1.AddSeparator()

        self.m_tool_replay = self.m_toolBar1.AddLabelTool( wx.ID_ANY, u"信号分析", wx.Bitmap( ".//icons//oscilloscope2.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, U"对本地数据文件或者历史数据进行信号分析", wx.EmptyString, None )

        self.m_toolBar1.AddSeparator()

        self.m_toolBar1.AddSeparator()
        self.m_toolBar1.AddSeparator()

        self.m_tool_help= self.m_toolBar1.AddLabelTool(wx.ID_ANY,u"帮助文档", wx.Bitmap( ".//icons//help1.png", wx.BITMAP_TYPE_ANY ) , wx.NullBitmap, wx.ITEM_NORMAL, u" 帮助文档，使用说明", wx.EmptyString, None)

        self.m_toolBar1.Realize()


        self.Centre( wx.BOTH )

        # Connect Events
        self.Bind(wx.EVT_CLOSE,self.OnDoClose)
        self.Bind( wx.EVT_TOOL, self.m_start_hwOnToolClicked, id = self.m_start_hw.GetId() )
        self.Bind( wx.EVT_TOOL, self.m_connectOnToolClicked, id = self.m_connect.GetId() )
        self.Bind( wx.EVT_TOOL, self.m_tool_sweepOnToolClicked, id = self.m_tool_sweep.GetId() )
        self.Bind( wx.EVT_TOOL, self.m_tool_iqOnToolClicked, id = self.m_tool_iq.GetId() )
        self.Bind( wx.EVT_TOOL, self.m_tool_pressOnToolClicked, id = self.m_tool_press.GetId() )
        self.Bind( wx.EVT_TOOL, self.m_tool_mapOnToolClicked, id = self.m_tool_map.GetId() )
        self.Bind( wx.EVT_TOOL, self.m_tool_freqplanOnToolClicked, id = self.m_tool_freqplan.GetId() )
        self.Bind( wx.EVT_TOOL, self.m_tool_remoteCtrlOnToolClicked, id = self.m_tool_remoteCtrl.GetId() )
        self.Bind( wx.EVT_TOOL, self.m_tool_replayOnToolClicked, id = self.m_tool_replay.GetId() )
        self.Bind(wx.EVT_TOOL, self.m_tool_helpOnToolClicked, id=self.m_tool_help.GetId())
    def __del__( self ):
        pass


    # Virtual event handlers, overide them in your derived class

    def hello(self):

        staticVar.getSock().sendall(struct.pack("!B", 0x55))
        staticVar.getSock().sendall(struct.pack("!B", 0x66))
        if(self.count_heart<=staticVar.count_heat_beat):
            self.count_heart=staticVar.count_heat_beat
        else:
            raise Exception('Conection ##### Stop')
            staticVar.sock=0
            staticVar.sockFile=0

            self.thread_station.input1=[]

            while (1):
                try:
                    self.serverCom.ConnectToServer(9000)
                    staticVar.sock = self.serverCom.sock
                    self.thread_station.input1.append(staticVar.sock)
                except Exception:
                    wx.MessageBox('Connect To Monitor Server Failure!',
                                  'Alert', wx.ICON_EXCLAMATION | wx.STAY_ON_TOP)


                try:
                    self.serverCom.ConnectToServer(9988)
                    staticVar.sockFile = self.serverCom.sockFile
                    self.thread_station.input1.append(staticVar.sockFile)
                    break
                except Exception:
                    wx.MessageBox('Connect To File Server Failure!',
                                  'Alert', wx.ICON_INFORMATION | wx.STAY_ON_TOP)
                time.sleep(5)



        self.timer = threading.Timer(15, self.hello, [])
        self.timer.start()


    def ConnectCore(self,ip1,port1,ip2,port2):
        flag_sock=0
        flag_sockFile=0
        count=0
        while(count<50):
            if(staticVar.sock==0 and flag_sock==0):
                try:
                    self.serverCom.ConnectToServerMoni(ip1,port1)
                    staticVar.sock=self.serverCom.sock
                    flag_sock=1
                except Exception,e:
                    print e
                    (ErrorType, ErrorValue, ErrorTB) = sys.exc_info()
                    wx.MessageBox('Connect To File Server Failure!\n' +
                                  str(ErrorValue[0]) + ' ' + str(ErrorValue[1]),
                                  'Alert', wx.ICON_INFORMATION | wx.STAY_ON_TOP)




            if(staticVar.sockFile==0 and flag_sockFile==0):
                try:
                    self.serverCom.ConnectToServerFile(ip2,port2)
                    staticVar.sockFile=self.serverCom.sockFile
                    flag_sockFile=1
                except Exception:
                    (ErrorType, ErrorValue, ErrorTB) = sys.exc_info()
                    wx.MessageBox('Connect To File Server Failure!\n'+
                                  str(ErrorValue[0])+' '+str(ErrorValue[1]),
                               'Alert', wx.ICON_INFORMATION | wx.STAY_ON_TOP)

            if(flag_sock and flag_sockFile):
                break
            else:
                count+=1
                time.sleep(5)



        connect=ConnectServer()

        connect.CommonHeader=FrameHeader(0x55,0xA1,staticVar.getid()&0x00FF,staticVar.getid()>>8)
        connect.CommonTail=self.tail

        if(self.GPS_list[0]==0 and self.GPS_list[1]==0 and self.GPS_list[2]==0):
            #临时加的测试
            self.GPS_list=[0]*9
            #############################

            Lon=114.4202
            Lat=30.5100
            Alti=35
            Lon_fen=0.4202*60
            Lat_fen=0.51*60
            Lon_fen_I=int(Lon_fen)
            Lon_fen_f=int((Lon_fen-int(Lon_fen))*1000)
            Lat_fen_I=int(Lat_fen)
            Lat_fen_f=int((Lat_fen-int(Lat_fen))*1000)


            self.GPS_list[1]=114
            self.GPS_list[2]=(Lon_fen_I<<2)+(Lon_fen_f>>8)
            self.GPS_list[3]=Lon_fen_f&0x00FF
            self.GPS_list[4]=30
            self.GPS_list[5]=(Lat_fen_I<<2)+(Lat_fen_f>>8)
            self.GPS_list[6]=Lat_fen_f&0x00FF
            self.GPS_list[8]=35

        list =self.GPS_list

        connect.LonLatAlti=LonLatAltitude(list[0],list[1],list[2],list[3],list[4]>>7,list[4]&0x7F,
                                          list[5],list[6],list[7]>>7,list[7]&0x7F,list[8])
        self.serverCom.SendQueryData(connect)


        self.thread_station=ReceiveServerData(self)
        self.thread_station.setDaemon(True)
        self.thread_station.start()



        #
        # self.timer = threading.Timer(15, self.hello, [])
        # self.timer.start()





    def QuerySend(self,funcPara):
        query=Query()
        query.CommonHeader=FrameHeader(0x55,funcPara,staticVar.getid()&0x00FF,staticVar.getid()>>8)
        query.CommonTail=self.tail
        staticVar.outPoint.write(bytearray(query))


    def m_start_hwOnToolClicked( self, event ):
        self.m_start_hw.Enable(False)
        ##usb way ####
        access_way = RecvGainSet()
        access_way.CommonHeader=FrameHeader(0x55,0x09,staticVar.getid()&0x00FF,staticVar.getid()>>8)
        access_way.CommonTail = self.tail
        access_way.RecvGain=3
        staticVar.outPoint.write(bytearray(access_way))


        ''' send query '''
        self.QuerySend(0x1C)
        self.GPS_list = self.byte_to_package.ReceiveRecv()
        if(self.GPS_list):
            obj = self.byte_to_package.ByteToWorkMode(self.GPS_list)
            self.show_recv_set.ShowIsConnect(obj)

            list_p=[]
            for i in range(6,15):
                list_p.append(self.GPS_list[i])

            self.GPS_list=list_p

        else:
            self.GPS_list=[0]*9


        self.thread_recvfft=ReceiveFFTThread(self)
        self.thread_recvfft.setDaemon(True)
        self.thread_recvfft.start()

    def m_connectOnToolClicked( self, event ):
        self.m_connect.Enable(False)
        if(self.dlg_connect==0):
            self.dlg_connect=input_ip.MyDialog1(self)
            self.dlg_connect.isValid=0
        self.dlg_connect.ShowModal()
        if(self.dlg_connect.isValid):
            ip_moni=self.dlg_connect.ip_file.GetValue()
            ip_file=self.dlg_connect.ip_file.GetValue()
            port_moni=int(self.dlg_connect.port_moni.GetValue())
            port_file=int(self.dlg_connect.port_file.GetValue())

            self.ip_moni=ip_moni
            self.ip_file=ip_file
            self.port_moni=port_moni
            self.port_file=port_file



        Thread(target=self.ConnectCore,args=(self.ip_moni,self.port_moni,self.ip_file,self.port_file)).start()
        event.Skip()



    def m_tool_sweepOnToolClicked( self, event ):
        if(self.dlg_sweep==0):
            self.dlg_sweep=dialog_sweep(self)
        self.dlg_sweep.ShowModal()
        event.Skip()

    def m_tool_iqOnToolClicked( self, event ):
        if(self.dlg_iq==0):
            self.dlg_iq=dialog_IQ(self)
        self.dlg_iq.ShowModal()
        event.Skip()

    def m_tool_pressOnToolClicked( self, event ):
        if(self.dlg_press==0):
            self.dlg_press=dialog_press(self)
        self.dlg_press.ShowModal()

        event.Skip()

    def m_tool_mapOnToolClicked( self, event ):
        if(self.dlg_map==0):
            self.dlg_map=dialog_map(self)
        self.dlg_map.ShowModal()
        event.Skip()

    def m_tool_freqplanOnToolClicked( self, event ):
        dlg=QueryFreqPlanDialog()
        dlg.ShowModal()
        event.Skip()

    def m_tool_remoteCtrlOnToolClicked( self, event ):
        dlg=dialog_remoteCtrl(self)
        dlg.ShowModal()
        event.Skip()

    def m_tool_replayOnToolClicked( self, event ):
        if(self.dlg_signal_fenxi==0):
            self.dlg_signal_fenxi=SignalAnalysisDlg(self)
        self.dlg_signal_fenxi.ShowModal()
        event.Skip()

#     def OnNewChild(self, evt):
#         self.count += 1
#         child = ChildFrame(self, self.count)
#         child.Activate()
#
    def m_tool_helpOnToolClicked(self,event):


        url = 'file:///C:/Spec_for_new_transfer/help.html'
        webbrowser.open(url)
    


    def OnDoClose(self, evt):
        # Close all ChildFrames first else Python crashes
        print 'Close all window '
        dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
        os.chdir(dirname)
#         os.chdir("./apache-tomcat-7.0.68//bin//")
        os.chdir("./apache-tomcat-7.0.68//bin//")

        os.system("shutdown.bat")
        if(not self.thread_route_map==0):
            if(self.thread_route_map.event.isSet()):
                self.thread_route_map.stop()

        if(not self.thread_route_map==0):
            self.thread_route_map.conn.close()

        '''
        flag1=0
        flag2=0
        flag3=0

        while(1):
            if(not self.thread_recvfft==0):
                self.thread_recvfft.stop()
            else:
                flag1=1
            if(not self.thread_upload==0):
                self.thread_upload.stop()
            else:
                flag2=1
            if(not self.thread_station==0):
                self.thread_station.stop()
            else:
                flag3=1

            time.sleep(0.5)
            if(not flag1):
                if(not self.thread_recvfft.isAlive()):
                    flag1=1
            if(not flag2):
                if(not self.thread_upload.isAlive()):
                    flag2=1
            if(not flag3):
                if(not self.thread_station.isAlive()):
                    flag3=1
            if(flag1 and flag2 and flag3):
                break
                '''


        for m in self.GetChildren():
            if isinstance(m, wx.aui.AuiMDIClientWindow):
                for k in m.GetChildren():
                    k.Close()
        # self.Close()
        sys.exit(0)
        


app=wx.App()
app.locale=wx.Locale(wx.LANGUAGE_ENGLISH)
MainFrame(None).Show()
app.MainLoop()

