# -*- coding: utf-8 -*- 

import wx

class PowerSptrSerDialog(wx.Dialog):
    
    def __init__(self):
        wx.Dialog.__init__(self,None,-1,u"服务器功率谱文件",wx.DefaultPosition,size=(200,350))
        panel = wx.Panel(self,-1)
        self.choice=0

        # locpathLbl = wx.StaticText(panel,-1,u"服务器文件路径选择：")
        # self.locpath = wx.TextCtrl(panel,-1,u"")
        # chooseBtn = wx.Button(panel,-1,u"选择")
        
        powLbl = wx.StaticText(panel,-1,u"功率谱文件图形显示：")
        powsptrDispl = wx.CheckBox(panel,-1,u"   功率谱图")
        waterfallDispl = wx.CheckBox(panel,-1,u"   瀑布图")
        listtableDispl = wx.CheckBox(panel,-1,u"   列表显示")
        statisticDispl = wx.CheckBox(panel,-1,u"   统计显示")
        displBtn = wx.Button(panel,-1,u"显示")
        
        img_spectrum = wx.Image('.//icons//spectrum.png',wx.BITMAP_TYPE_ANY)
        bmp_spectrum = wx.StaticBitmap(panel,-1,wx.BitmapFromImage(img_spectrum))

        img_waterfall = wx.Image('.//icons//waterfull.png',wx.BITMAP_TYPE_ANY)
        bmp_waterfall = wx.StaticBitmap(panel,-1,wx.BitmapFromImage(img_waterfall))
        
        img_list = wx.Image('.//icons//list.png',wx.BITMAP_TYPE_ANY)
        bmp_list = wx.StaticBitmap(panel,-1,wx.BitmapFromImage(img_list))
        
        img_stat = wx.Image('.//icons//statistics.png',wx.BITMAP_TYPE_ANY)
        bmp_stat = wx.StaticBitmap(panel,-1,wx.BitmapFromImage(img_stat))
        
        # pSizer = wx.BoxSizer(wx.VERTICAL)
        # pSizer.Add(locpathLbl,0,wx.ALL,5)
        # pSizer.Add(self.locpath,0,wx.ALL|wx.EXPAND,5)
        # pSizer.Add(chooseBtn,0,wx.ALIGN_CENTER,5)
        # pSizer.Add((10,10))
        # pSizer.Add(wx.StaticLine(panel),0,wx.EXPAND,5)
        
        iqdisSizer = wx.GridSizer(6,2,0,0)
        
        iqdisSizer.Add(powLbl,0,wx.ALL,5)
        iqdisSizer.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
         
        iqdisSizer.Add(bmp_spectrum,0,wx.ALIGN_CENTER,5)
        iqdisSizer.Add(bmp_waterfall,0,wx.ALIGN_CENTER,5)
        
        iqdisSizer.Add(powsptrDispl,0,wx.ALL,5)
        iqdisSizer.Add(waterfallDispl,0,wx.ALL,5)
        
        iqdisSizer.Add(bmp_list,0,wx.ALIGN_CENTER,5)
        iqdisSizer.Add(bmp_stat,0,wx.ALIGN_CENTER,5)
        
        iqdisSizer.Add(listtableDispl,0,wx.ALL,5)
        iqdisSizer.Add(statisticDispl,0,wx.ALL,5)

        iqdisSizer.Add(displBtn, 0, wx.ALL, 5)
        panel.SetSizer(iqdisSizer)

        self.Bind(wx.EVT_BUTTON,self.OnButtonClick,displBtn)
    def OnButtonClick(self,event):
        pass

        # btnSizer = wx.BoxSizer(wx.VERTICAL)
        # btnSizer.Add(displBtn,0,wx.ALL,5)
        
        # pSizer.Add(iqdisSizer,0,wx.ALL,5)
        # pSizer.Add(btnSizer,0,wx.ALIGN_CENTER,5)
        # panel.SetSizer(pSizer)
        #pSizer.Fit(self)
        #pSizer.SetSizeHints(self)
        
        # self.Bind(wx.EVT_BUTTON,self.chooseClick,chooseBtn)
        
    # def chooseClick(self,evt):
    #     self.dirLocalDlg = wx.FileDialog(None,u"服务器文件路径选择：",style=wx.MULTIPLE)
    #     if self.dirLocalDlg.ShowModal() == wx.ID_OK:
    #         for item in self.dirLocalDlg.GetPaths():
    #             self.locpath.AppendText('"')
    #             self.locpath.AppendText(item)
    #             self.locpath.AppendText('";')
        
        
#if __name__ == '__main__':          
#    app = wx.App()
#    app.MainLoop()
#    dialog = PowerSptrDialog()
#    dialog.ShowModal()
        
