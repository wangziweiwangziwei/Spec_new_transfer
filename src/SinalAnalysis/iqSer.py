# -*- coding: utf-8 -*- 

import wx

class IQSerDialog(wx.Dialog):
    
    def __init__(self):
        wx.Dialog.__init__(self,None,-1,u"服务器IQ文件",wx.DefaultPosition,size=(340,340))
        panel = wx.Panel(self,-1)
        #
        # locpathLbl = wx.StaticText(panel,-1,u"服务器文件路径选择：")
        # self.locpath = wx.TextCtrl(panel,-1,u"")
        # chooseBtn = wx.Button(panel,-1,u"选择")
        #
        powLbl = wx.StaticText(panel,-1,u"IQ文件图形显示：")
        waveDispl = wx.CheckBox(panel,-1,u"   波形图")
        spDispl = wx.CheckBox(panel,-1,u"   功率谱")
        waterDispl = wx.CheckBox(panel,-1,u"   瀑布图")
        ccdfDispl = wx.CheckBox(panel,-1,u"    CCDF")
        eyeDispl = wx.CheckBox(panel,-1,u"    眼图")
        conDispl = wx.CheckBox(panel,-1,u"   星座图")
        displBtn = wx.Button(panel,-1,u"显示")
        
        img_waveform = wx.Image('./icons//waveform.png',wx.BITMAP_TYPE_ANY)
        bmp_waveform = wx.StaticBitmap(panel,-1,wx.BitmapFromImage(img_waveform))
        
        img_spectrum = wx.Image('./icons//spectrum.png',wx.BITMAP_TYPE_ANY)
        bmp_spectrum = wx.StaticBitmap(panel,-1,wx.BitmapFromImage(img_spectrum))
        
        img_waterfall = wx.Image('./icons//waterfull.png',wx.BITMAP_TYPE_ANY)
        bmp_waterfall = wx.StaticBitmap(panel,-1,wx.BitmapFromImage(img_waterfall))
        
        img_ccdf = wx.Image('./icons//ccdf.png',wx.BITMAP_TYPE_ANY)
        bmp_ccdf = wx.StaticBitmap(panel,-1,wx.BitmapFromImage(img_ccdf))
        
        img_eye = wx.Image('./icons//eye.png',wx.BITMAP_TYPE_ANY)
        bmp_eye = wx.StaticBitmap(panel,-1,wx.BitmapFromImage(img_eye))
        
        img_constellation = wx.Image('./icons//constellation.png',wx.BITMAP_TYPE_ANY)
        bmp_constellation = wx.StaticBitmap(panel,-1,wx.BitmapFromImage(img_constellation))
        
        # pSizer = wx.BoxSizer(wx.VERTICAL)
        # pSizer.Add(locpathLbl,0,wx.ALL,5)
        # pSizer.Add(self.locpath,0,wx.ALL|wx.EXPAND,5)
        # pSizer.Add(chooseBtn,0,wx.ALIGN_CENTER,5)
        # pSizer.Add((10,10))
        # pSizer.Add(wx.StaticLine(panel),0,wx.EXPAND,5)
        #
        
        iqdisSizer = wx.GridSizer(6,3,0,0)
        
        iqdisSizer.Add(powLbl,0,wx.ALL,5)
        iqdisSizer.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        iqdisSizer.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        iqdisSizer.Add(bmp_waveform,0,wx.ALIGN_CENTER,5)
        iqdisSizer.Add(bmp_spectrum,0,wx.ALIGN_CENTER,5)
        iqdisSizer.Add(bmp_waterfall,0,wx.ALIGN_CENTER,5)
        
        iqdisSizer.Add(waveDispl,0,wx.ALL,5)
        iqdisSizer.Add(spDispl,0,wx.ALL,5)
        iqdisSizer.Add(waterDispl,0,wx.ALL,5)
        
        iqdisSizer.Add(bmp_ccdf,0,wx.ALIGN_CENTER,5)
        iqdisSizer.Add(bmp_eye,0,wx.ALIGN_CENTER,5)
        iqdisSizer.Add(bmp_constellation,0,wx.ALIGN_CENTER,5)
        
        iqdisSizer.Add(ccdfDispl,0,wx.ALL,5)
        iqdisSizer.Add(eyeDispl,0,wx.ALL,5)
        iqdisSizer.Add(conDispl,0,wx.ALL,5)

        iqdisSizer.Add(displBtn, 0, wx.ALL, 5)
        panel.SetSizer(iqdisSizer)

        # btnSizer = wx.BoxSizer(wx.VERTICAL)
        # btnSizer.Add(displBtn,0,wx.ALL,5)
        #
        # pSizer.Add(iqdisSizer,0,wx.ALL,5)
        # pSizer.Add(btnSizer,0,wx.ALIGN_CENTER,5)
        # panel.SetSizer(pSizer)
        #pSizer.Fit(self)
        #pSizer.SetSizeHints(self)

        self.Bind(wx.EVT_BUTTON, self.OnButtonClick, displBtn)

    def OnButtonClick(self, event):
        pass
    #
    # def chooseClick(self,evt):
    #     self.dirLocalDlg = wx.FileDialog(None,u"服务器文件路径选择：",style=wx.MULTIPLE)
    #     if self.dirLocalDlg.ShowModal() == wx.ID_OK:
    #         for item in self.dirLocalDlg.GetPaths():
    #             self.locpath.AppendText('"')
    #             self.locpath.AppendText(item)
    #             self.locpath.AppendText('";')
    #
        
#if __name__ == '__main__':          
#    app = wx.App()
#    app.MainLoop()
#    dialog = PowerSptrDialog()
#    dialog.ShowModal()
        
