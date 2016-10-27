# -*- coding: utf-8 -*- 

import wx
import wx.aui
import numpy

class Toji(wx.aui.AuiMDIChildFrame):
    def __init__(self,parent):
        wx.aui.AuiMDIChildFrame.__init__(self,parent,-1,title=u"统计结果显示                    ")
        self.parent=parent

        self.list_toji = wx.ListCtrl(self,-1,size=(870,410),style=wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES)
        self.list_toji.InsertColumn(0, u'序号',wx.LIST_FORMAT_CENTER)
        self.list_toji.InsertColumn(1, u'频率(MHz)',wx.LIST_FORMAT_CENTER)
        self.list_toji.InsertColumn(2, u'功率(dBuv/m)',wx.LIST_FORMAT_CENTER)
        self.list_toji.InsertColumn(3, u'最大值(dBuv/m)',wx.LIST_FORMAT_CENTER)
        self.list_toji.InsertColumn(4, u'最小值(dBuv/m)',wx.LIST_FORMAT_CENTER)
        self.list_toji.InsertColumn(5, u'平均值(dBuv/m)',wx.LIST_FORMAT_CENTER)
        self.list_toji.SetColumnWidth(0, 80)
        self.list_toji.SetColumnWidth(1, 150)
        self.list_toji.SetColumnWidth(2, 150)
        self.list_toji.SetColumnWidth(3, 150)
        self.list_toji.SetColumnWidth(4, 150)
        self.list_toji.SetColumnWidth(5, 150)        
        for i in range(1,1025):
            self.list_toji.InsertStringItem(i-1,str(i))    
        
        t_sizer = wx.GridSizer(1,1,0,0)    
        t_sizer.Add(self.list_toji,0,wx.EXPAND)
        self.SetSizer(t_sizer)

        self.Bind(wx.EVT_WINDOW_DESTROY,self.OnClose)

    def Tongji(self,xData,yData):

        for i in range(1024):
            self.list_toji.SetStringItem(i,1,str('%0.2f' % xData[i]))
            self.list_toji.SetStringItem(i,2,str(yData[i]))
        
        max_y = max(yData)
        min_y = min(yData)
        ave_y = numpy.average(yData)
        
        self.list_toji.SetStringItem(0,3,str(max_y))
        self.list_toji.SetStringItem(0,4,str(min_y))
        self.list_toji.SetStringItem(0,5,str('%0.2f' % ave_y))
        
    def OnClose(self,evt):
        self.parent.TojiFrame=None
        self.Close()                

        