# -*- coding: utf-8 -*-
import wx
import math
# from numpy import sin,cos,pi
from src.Wave import IQWave
from threading import Thread
# import time

class IQLocDialog(wx.Dialog):
    
    def __init__(self,parent):
        wx.Dialog.__init__(self,parent,-1,u"本地IQ文件",wx.DefaultPosition,size=(340,340))
        panel = wx.Panel(self,-1)
        self.parent=parent
        locpathLbl = wx.StaticText(panel,-1,u"本地文件路径选择：")
        self.locpath = wx.TextCtrl(panel,-1,u"")
        chooseBtn = wx.Button(panel,-1,u"选择")
        
        powLbl = wx.StaticText(panel,-1,u"IQ文件图形显示：")
        self.waveDispl = wx.CheckBox(panel,-1,u"   波形图")
        spDispl = wx.CheckBox(panel,-1,u"   功率谱")
        waterDispl = wx.CheckBox(panel,-1,u"   瀑布图")
        ccdfDispl = wx.CheckBox(panel,-1,u"    CCDF")
        eyeDispl = wx.CheckBox(panel,-1,u"    眼图")
        conDispl = wx.CheckBox(panel,-1,u"   星座图")
        displBtn = wx.Button(panel,-1,u"显示")
        
        img_waveform = wx.Image('.//icons//waveform.png',wx.BITMAP_TYPE_ANY)
        bmp_waveform = wx.StaticBitmap(panel,-1,wx.BitmapFromImage(img_waveform))
        
        img_spectrum = wx.Image('.//icons//spectrum.png',wx.BITMAP_TYPE_ANY)
        bmp_spectrum = wx.StaticBitmap(panel,-1,wx.BitmapFromImage(img_spectrum))
        
        img_waterfall = wx.Image('.//icons//waterfull.png',wx.BITMAP_TYPE_ANY)
        bmp_waterfall = wx.StaticBitmap(panel,-1,wx.BitmapFromImage(img_waterfall))
        
        img_ccdf = wx.Image('.//icons//ccdf.png',wx.BITMAP_TYPE_ANY)
        bmp_ccdf = wx.StaticBitmap(panel,-1,wx.BitmapFromImage(img_ccdf))
        
        img_eye = wx.Image('.//icons//eye.png',wx.BITMAP_TYPE_ANY)
        bmp_eye = wx.StaticBitmap(panel,-1,wx.BitmapFromImage(img_eye))
        
        img_constellation = wx.Image('.//icons//constellation.png',wx.BITMAP_TYPE_ANY)
        bmp_constellation = wx.StaticBitmap(panel,-1,wx.BitmapFromImage(img_constellation))
        
        pSizer = wx.BoxSizer(wx.VERTICAL)
        pSizer.Add(locpathLbl,0,wx.ALL,5)
        pSizer.Add(self.locpath,0,wx.ALL|wx.EXPAND,5)
        pSizer.Add(chooseBtn,0,wx.ALIGN_CENTER,5)
        pSizer.Add((10,10))
        pSizer.Add(wx.StaticLine(panel),0,wx.EXPAND,5)
        
        
        iqdisSizer = wx.GridSizer(5,3,0,0)
        
        iqdisSizer.Add(powLbl,0,wx.ALL,5)
        iqdisSizer.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        iqdisSizer.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        
        iqdisSizer.Add(bmp_waveform,0,wx.ALIGN_CENTER,5)
        iqdisSizer.Add(bmp_spectrum,0,wx.ALIGN_CENTER,5)
        iqdisSizer.Add(bmp_waterfall,0,wx.ALIGN_CENTER,5)
        
        iqdisSizer.Add(self.waveDispl,0,wx.ALL,5)
        iqdisSizer.Add(spDispl,0,wx.ALL,5)
        iqdisSizer.Add(waterDispl,0,wx.ALL,5)
        
        iqdisSizer.Add(bmp_ccdf,0,wx.ALIGN_CENTER,5)
        iqdisSizer.Add(bmp_eye,0,wx.ALIGN_CENTER,5)
        iqdisSizer.Add(bmp_constellation,0,wx.ALIGN_CENTER,5)
        
        iqdisSizer.Add(ccdfDispl,0,wx.ALL,5)
        iqdisSizer.Add(eyeDispl,0,wx.ALL,5)
        iqdisSizer.Add(conDispl,0,wx.ALL,5)
        
        btnSizer = wx.BoxSizer(wx.VERTICAL)
        btnSizer.Add(displBtn,0,wx.ALL,5)
        
        pSizer.Add(iqdisSizer,0,wx.ALL,5)
        pSizer.Add(btnSizer,0,wx.ALIGN_CENTER,5)
        panel.SetSizer(pSizer)
        #pSizer.Fit(self)
        #pSizer.SetSizeHints(self)
        
        self.Bind(wx.EVT_BUTTON,self.chooseClick,chooseBtn)
        self.Bind(wx.EVT_BUTTON, self.displClick, displBtn)
    def chooseClick(self,evt):
        self.dirLocalDlg = wx.FileDialog(None,u"本地文件路径选择：")
        if self.dirLocalDlg.ShowModal() == wx.ID_OK:
            self.item = self.dirLocalDlg.GetPath()
            self.locpath.AppendText(self.item)

    def displClick(self, evt):

        if (self.waveDispl.GetValue()):
            self.Close()
            self.thread = Thread(target=self.foo)
            self.thread.start()

    def foo(self):

        self.parent.parent.WaveFrame = IQWave.WaveIQ(self.parent.parent, u"定频波形图              ")
        self.parent.parent.WaveFrame.Activate()
        try:
            for i in range(5):
                 self.drawIQ(self.item)

        except Exception, e:
            print e
            self.parent.parent.WaveFrame.Destroy()
            self.parent.parent.WaveFrame = None

        # self.parent.parent.WaveFrame.Destroy()
    def drawIQ(self, path):
        if (not self.locpath == None):

            locfile = open(path, 'rb')
            file_loc = locfile.read()
            IQB = []

            for line in file_loc:
                i = ord(line)
                IQB.append(i)
            self.N = IQB[14]
            self.n = IQB[15]
            #             Fc=(IQB[10] << 6) + (IQB[11] & 0x3F) + float(((IQB[11] >> 6) << 8) + IQB[12])/ 2 ** 10
            #
            #             DataRate = IQB[13] & 0x0F
            #             if(DataRate==0x01):self.Fs=5e6
            #             elif(DataRate==0x02):self.Fs=2.5e6
            #             elif(DataRate==0x03):self.Fs=1e6
            #             elif(DataRate==0x04):self.Fs=0.5e6
            #             elif(DataRate==0x05):self.Fs=0.1e6
            #             else:
            #                 pass


            for j in range(self.N):
                IData = []
                QData = []
                for i in range(2000):
                    if ((6001 * (j + 1) - 5983 + i * 3) < (len(IQB) - 1)):
                        HighI1 = ((IQB[6001 * (j + 1) - 5985 + i * 3]) >> 4) << 8
                        LowI1 = IQB[6001 * (j + 1) - 5984 + i * 3]
                        if (HighI1 >= 2048):
                            I1 = -(2 ** 12 - HighI1 - LowI1)
                        else:
                            I1 = (HighI1 + LowI1)
                        IData.append(I1)

                        HighQ1 = ((IQB[6001 * (j + 1) - 5985 + i * 3]) & 0x0F) << 8
                        LowQ1 = IQB[6001 * (j + 1) - 5983 + i * 3]
                        if (HighQ1 >= 2048):
                            Q1 = -(2 ** 12 - HighQ1 - LowQ1)
                        else:
                            Q1 = (HighQ1 + LowQ1)
                        QData.append(Q1)

                        #                 data = []
                        #                 for i in range(len(IData)):
                        #                     dataTmp = 2 * pi * Fc / self.Fs * i
                        #                     data.append(IData[i]*cos(dataTmp)+QData[i]*sin(dataTmp))

                IData_abs = []
                QData_abs = []
                for i in IData:
                    IData_abs.append(abs(IData[i]))
                for i in QData:
                    QData_abs.append(abs(QData[i]))
                IData_max = max(IData_abs)
                QData_max = max(QData_abs)
                I_Q = math.sqrt(IData_max ** 2 + QData_max ** 2)

                IData_nor = []
                for j in range(len(IData)):
                    IData_nor.append(IData[i] / I_Q)
                QData_nor = []
                for j in range(len(QData)):
                    QData_nor.append(QData[i] / I_Q)

                # print 'len arr',len(arr)
                self.parent.parent.WaveFrame.Wave(IData_nor,'y')
                self.parent.parent.WaveFrame.Wave(QData_nor,'r')
