# -*- coding: utf-8 -*-

import wx

class dialog_freqyewu( wx.Dialog ):

    def __init__(self,parent):
        self.isValid=0
        wx.Dialog.__init__(self,parent,-1,u"指定频段",pos = wx.DefaultPosition,size = (710,480))

        self.freq_li = wx.ListCtrl(self,-1,size=(710,410),style=wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES)
        self.freq_li.InsertColumn(0, u'序号',wx.LIST_FORMAT_CENTER)
        self.freq_li.InsertColumn(1, u'起始频率(MHz)',wx.LIST_FORMAT_CENTER)
        self.freq_li.InsertColumn(2, u'终止频率(MHz)',wx.LIST_FORMAT_CENTER)
        self.freq_li.InsertColumn(3, u'业务属性',wx.LIST_FORMAT_CENTER)
        self.freq_li.SetColumnWidth(0, 80)
        self.freq_li.SetColumnWidth(1, 100)
        self.freq_li.SetColumnWidth(2, 100)
        self.freq_li.SetColumnWidth(3, 400)

        self.start_freq = 0
        self.end_freq = 0

        for i in range(1,30):
            self.freq_li.InsertStringItem(i-1,str(i))

        start_li = ['30','50','87','108','156','167','223','335','406','470','566','798','960','1215','1429','1525','1710','2200','2300','2500','2690','3300','4200','4400','5000','5250','5470','5650','5850']
        end_li = ['50','87','108','137','167','223','335','400','470','566','798','960','1215','1429','1525','1710','2200','2300','2500','2690','3300','4200','4400','5000','5250','5470','5650','5850','6700']
        busi_li = [u"固定，移动，广播",u"固定，移动，广播，无线电定位，航空无线电导航，业余",u"广播",u"航空无线电导航，航空移动",u"水上移动，固定，移动",u"广播，空间操作",u"固定，移动，航空移动，无线电定位",u"固定，移动，卫星移动",u"固定，移动，航空无线电导航，无线电定位",u"广播，空间操作",u"固定，移动，广播，无线电导航与定位，射电天文",u"固定，移动，广播",u"航空无线电导航，卫星无线电导航",u"卫星，航空，导航，定位",u"固定，移动，广播，卫星广播",u"空间操作，卫星移动，固定，移动",u"移动，卫星移动，空间操作",u"空间操作和研究",u"固定，移动，卫星移动，无线电定位",u"移动，卫星固定，广播",u"卫星地球探测，射电天文，导航，定位",u"固定，卫星固定，无线电定位",u"航空无线电导航",u"固定，移动，射电天文",u"卫星航空移动，导航，固定，移动",u"卫星地球探测，定位，空间研究",u"水上无线电导航，地球探测，移动，定位",u"无线电定位，移动，固定",u"固定，移动，卫星固定，无线电定位"]


        for i in range(1,30):
            self.freq_li.SetStringItem(i-1,1,start_li[i-1])
            self.freq_li.SetStringItem(i-1,2,end_li[i-1])
            self.freq_li.SetStringItem(i-1,3,busi_li[i-1])

        self.btn_ok = wx.Button(self,-1,u"确定")
        self.btn_can = wx.Button(self,-1,u"取消")

        m_sizer = wx.BoxSizer(wx.VERTICAL)
        m_sizer.Add(self.freq_li,0,wx.ALL)

        btn_sizer = wx.GridSizer(1,6,0,0)
        btn_sizer.AddSpacer((0,0),1,wx.EXPAND,5)
        btn_sizer.AddSpacer((0,0),1,wx.EXPAND,5)
        btn_sizer.AddSpacer((0,0),1,wx.EXPAND,5)
        btn_sizer.AddSpacer((0,0),1,wx.EXPAND,5)
        btn_sizer.Add(self.btn_ok,0,wx.ALL|wx.RIGHT,5)
        btn_sizer.Add(self.btn_can,0,wx.ALL|wx.RIGHT,5)

        m_sizer.Add(btn_sizer,0,wx.ALL)
        self.SetSizer(m_sizer)

        self.Centre( wx.BOTH )

        self.btn_ok.Bind( wx.EVT_BUTTON,self.btn_okOnButtonClick)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnItemSelected,self.freq_li)


    def __del__( self ):
        pass

    def btn_okOnButtonClick(self,evt):

        self.isValid=1
        self.Destroy()

    def OnItemSelected(self,evt):
        item = evt.GetIndex()
        print item
        self.start_freq = self.freq_li.GetItem(item,1).Text
        self.end_freq = self.freq_li.GetItem(item,2).Text


# app = wx.App()
# dlg = dialog_freqblock()
# dlg.ShowModal()
# app.MainLoop()




