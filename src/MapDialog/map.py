# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
from src.MapDialog import req_ab, req_elec_trend, req_stationPro, req_curPro,req_port_pro
from src.MapDialog import req_route
from src.Map.BaiduMap import Map
import os 
###########################################################################
## Class mapdialog
###########################################################################

class dialog_map ( wx.Dialog ):
    
    def __init__( self, parent ):
        
        ############################
        

        self.parent=parent

        self.req_elec_trend=0
        self.req_ab=0
        self.req_route= 0
        self.req_curPro=0


        font_map = wx.Font(10, wx.ROMAN, wx.NORMAL, wx.LIGHT, underline=False, faceName=u"微软雅黑",
                           encoding=wx.FONTENCODING_DEFAULT)


        #############################
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"地图服务", pos = wx.DefaultPosition, size = wx.Size( 487,322 ), style = wx.DEFAULT_DIALOG_STYLE )
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        gSizer2 = wx.GridSizer( 6, 3, 0, 0 )
        
        
        gSizer2.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        
        gSizer2.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        
        gSizer2.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.check_elec_distribute = wx.CheckBox( self, wx.ID_ANY, u"电磁分布态势服务", wx.DefaultPosition, wx.DefaultSize, 0 )
        
        gSizer2.Add( self.check_elec_distribute, 0, wx.ALL, 5 )
        
        self.check_elec_distribute_1 = wx.CheckBox( self, wx.ID_ANY, u"曲面插值分布态势", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer2.Add( self.check_elec_distribute_1, 0, wx.ALL, 5 )
        
        gSizer2.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        
        self.check_route = wx.CheckBox( self, wx.ID_ANY, u"电磁分布路径服务", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer2.Add( self.check_route, 0, wx.ALL, 5 )
        
    
        self.check_ab = wx.CheckBox( self, wx.ID_ANY, u"异常频点定位请求", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer2.Add( self.check_ab, 0, wx.ALL, 5 )
        
        gSizer2.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.check_allstation = wx.CheckBox( self, wx.ID_ANY, u"全部台站记录属性", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer2.Add( self.check_allstation, 0, wx.ALL, 5 )
        
        self.check_regiPro = wx.CheckBox( self, wx.ID_ANY, u"指定频率范围登记属性", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer2.Add( self.check_regiPro, 0, wx.ALL, 5 )
        
        self.check_curPro = wx.CheckBox( self, wx.ID_ANY, u"登记台站当前属性", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer2.Add( self.check_curPro, 0, wx.ALL, 5 )
        
        self.check_onlineport = wx.CheckBox( self, wx.ID_ANY, u"在网终端查询", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer2.Add( self.check_onlineport, 0, wx.ALL, 5 )
        
        self.check_allport = wx.CheckBox( self, wx.ID_ANY, u"全部注册终端查询", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer2.Add( self.check_allport, 0, wx.ALL, 5 )

        self.check_elec_distribute.SetFont(font_map)
        self.check_elec_distribute_1.SetFont(font_map)
        self.check_ab.SetFont(font_map)
        self.check_route.SetFont(font_map)
        self.check_allstation.SetFont(font_map)
        self.check_regiPro.SetFont(font_map)
        self.check_curPro.SetFont(font_map)
        self.check_onlineport.SetFont(font_map)
        self.check_allport.SetFont(font_map)


        gSizer2.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        self.btn_map_ok = wx.Button( self, wx.ID_ANY, u"确定", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer2.Add( self.btn_map_ok, 0, wx.ALL, 5 )
        
        self.btn_map_cancel = wx.Button( self, wx.ID_ANY, u"取消", wx.DefaultPosition, wx.DefaultSize, 0 )
        gSizer2.Add( self.btn_map_cancel, 0, wx.ALL, 5 )
        
        
        self.SetSizer( gSizer2 )
        self.Layout()
        
        self.Centre( wx.BOTH )
        
        # Connect Events
        self.btn_map_ok.Bind( wx.EVT_BUTTON, self.btn_map_okOnButtonClick )
        self.btn_map_cancel.Bind( wx.EVT_BUTTON, self.btn_map_cancelOnButtonClick )
    
    def __del__( self ):
        pass
    
    
    # Virtual event handlers, overide them in your derived class
    def btn_map_okOnButtonClick( self, event ):
      
      
         
        ####开地图#######
       
            
         
            #
        if(not isinstance(self.parent.MapFrame, Map)):
            self.parent.MapFrame=Map(self.parent)
            self.parent.MapFrame.Activate()
               
                    
            
            
        ################
        if(self.check_route.GetValue()):
            if(self.req_route==0):
                self.req_route=req_route.ReqElecPathDialog(self.parent)
            self.req_route.ShowModal()
        
        else:
            if(not self.parent.thread_route_map==0):
                self.parent.thread_route_map.stop()
            
            if(self.check_elec_distribute.GetValue()):
                if(self.req_elec_trend==0):
                    self.req_elec_trend=req_elec_trend.ReqElecTrendDialog(self.parent)
                self.req_elec_trend.ShowModal()
            
            ####曲面插值######
            elif(self.check_elec_distribute_1.GetValue()):

                dlg=req_elec_trend.ReqElecTrendDialog(self.parent)
                dlg.ShowModal()
                
            elif(self.check_ab.GetValue()):
                if(self.req_ab==0):
                    self.req_ab=req_ab.ReqAbFreqDialog(self.parent)
                self.req_ab.ShowModal()

            elif(self.check_allstation.GetValue()):
                dlg=req_stationPro.QueryStationProDialog(self.parent,0xA8)
                dlg.ShowModal()
            elif(self.check_regiPro.GetValue()):
                dlg=req_stationPro.QueryStationProDialog(self.parent,0xA5)
                dlg.ShowModal()
            elif(self.check_curPro.GetValue()):
                if(self.req_curPro==0):
                    self.req_curPro=req_curPro.QueryCurStationProDialog(self.parent)
                self.req_curPro.ShowModal()
            elif(self.check_onlineport.GetValue()):
                req_port_pro.QueryPort.query_port(self.parent,0xA9)
            elif(self.check_allport.GetValue()):
                req_port_pro.QueryPort.query_port(self.parent,0xAA)
        
        event.Skip()

    def btn_map_cancelOnButtonClick( self, event ):
        event.Skip()
    

#     
# app=wx.App()
# mapdialog(None).Show()
# app.MainLoop()
