# -*- coding: utf-8 -*- 
import time
from numpy import linspace
import wx
from src.Spectrum import Spectrum_1

from threading import Thread
class PowerSptrLocDialog(wx.Dialog):
    
    def __init__(self,parent):
        wx.Dialog.__init__(self,parent,-1,u"本地功率谱文件",wx.DefaultPosition,size=(200,350))
        panel = wx.Panel(self,-1)

        self.parent=parent

        locpathLbl = wx.StaticText(panel,-1,u"本地文件路径选择：")
        self.locpath = wx.TextCtrl(panel,-1,u"")
        chooseBtn = wx.Button(panel,-1,u"选择")
        
        powLbl = wx.StaticText(panel,-1,u"功率谱文件图形显示：")
        self.powsptrDispl = wx.CheckBox(panel,-1,u"   功率谱图")
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
        
        pSizer = wx.BoxSizer(wx.VERTICAL)
        pSizer.Add(locpathLbl,0,wx.ALL,5)
        pSizer.Add(self.locpath,0,wx.ALL|wx.EXPAND,5)
        pSizer.Add(chooseBtn,0,wx.ALIGN_CENTER,5)
        pSizer.Add((10,10))
        pSizer.Add(wx.StaticLine(panel),0,wx.EXPAND,5)
        
        iqdisSizer = wx.GridSizer(5,2,0,0)
        
        iqdisSizer.Add(powLbl,0,wx.ALL,5)
        iqdisSizer.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
         
        iqdisSizer.Add(bmp_spectrum,0,wx.ALIGN_CENTER,5)
        iqdisSizer.Add(bmp_waterfall,0,wx.ALIGN_CENTER,5)
        
        iqdisSizer.Add(self.powsptrDispl,0,wx.ALL,5)
        iqdisSizer.Add(waterfallDispl,0,wx.ALL,5)
        
        iqdisSizer.Add(bmp_list,0,wx.ALIGN_CENTER,5)
        iqdisSizer.Add(bmp_stat,0,wx.ALIGN_CENTER,5)
        
        iqdisSizer.Add(listtableDispl,0,wx.ALL,5)
        iqdisSizer.Add(statisticDispl,0,wx.ALL,5)
        
     
        btnSizer = wx.BoxSizer(wx.VERTICAL)
        btnSizer.Add(displBtn,0,wx.ALL,5)
        
        pSizer.Add(iqdisSizer,0,wx.ALL,5)
        pSizer.Add(btnSizer,0,wx.ALIGN_CENTER,5)
        panel.SetSizer(pSizer)
        #pSizer.Fit(self)
        #pSizer.SetSizeHints(self)
        
        self.Bind(wx.EVT_BUTTON,self.chooseClick,chooseBtn)
        self.Bind(wx.EVT_BUTTON,self.displClickBtn,displBtn)
        
    def chooseClick(self,evt):
        self.dirLocalDlg = wx.FileDialog(None,u"本地文件路径选择：",style=wx.MULTIPLE)
        if self.dirLocalDlg.ShowModal() == wx.ID_OK:
            for item in self.dirLocalDlg.GetPaths():
                self.locpath.AppendText('"')
                self.locpath.AppendText(item)
                self.locpath.AppendText('";')

    def displClickBtn(self, evt):

        if (self.powsptrDispl.GetValue()):
            self.Close()

            thread = Thread(target=self.foo)
            thread.start()

    def foo(self):



        try:
            for i in range(5):
                if (isinstance(self.parent.parent.HistorySpecFrame, Spectrum_1.Spec)):
                    for item in self.dirLocalDlg.GetPaths():
                        loc_freq_array_y = self.freqArray(item)
                        freq_s_x = 70 + 25 * (self.n - 1)
                        freq_e_x = 70 + 25 * (self.N)
                        self.showLocFile(freq_s_x, freq_e_x, loc_freq_array_y)

        except Exception, e:
            print e
            self.parent.parent.HistorySpecFrame.Destroy()
            

    def showLocFile(self, begin_x, end_x, loc_freq_array):
        begin = begin_x
        end = end_x
        begin_Y = -120
        end_Y = 60
        # SpecFrame.panelFigure.setSpLabel(begin_X=begin, end_X=end)
        self.parent.parent.HistorySpecFrame.panelFigure.setSpLabel(begin, end, begin_Y, end_Y)
        self.parent.parent.HistorySpecFrame.FreqMin = begin
        self.parent.parent.HistorySpecFrame.FreqMax = end
        self.parent.parent.HistorySpecFrame.panelFigure.FFT_Min_X = begin
        self.parent.parent.HistorySpecFrame.panelFigure.FFT_Max_X = end
        self.parent.parent.HistorySpecFrame.panelFigure.Min_X.SetValue(str(begin))
        self.parent.parent.HistorySpecFrame.panelFigure.Max_X.SetValue(str(end))
        x = linspace(begin, end, len(loc_freq_array))
        self.parent.parent.HistorySpecFrame.panelFigure.lineSpec.set_xdata(x)
        self.parent.parent.HistorySpecFrame.panelFigure.PowerSpectrum(0x51, loc_freq_array)
        # print x

    def freqArray(self, path):
        if (not self.locpath == None):

            locfile = open(path, 'rb')
            file_loc = locfile.read()
            FreqArrayB = []
            FreqArray = []
            for line in file_loc:
                i = ord(line)
                FreqArrayB.append(i)
            index = self.myfind(255, FreqArrayB)
            self.index_e = index[len(index) - 1]
            self.N = FreqArrayB[12]
            self.n = FreqArrayB[13]
            if (self.N == 1):
                for i in range(512):
                    HighFreq1 = ((FreqArrayB[14 + i * 3]) & 0xF0) << 4
                    LowFreq1 = FreqArrayB[15 + i * 3]
                    if (HighFreq1 >= 8):
                        Freq1 = -(2 ** 12 - (HighFreq1) - LowFreq1) / 8.0
                    else:
                        Freq1 = ((HighFreq1) + LowFreq1) / 8.0
                    FreqArray.append(Freq1)
                    HighFreq2 = ((FreqArrayB[14 + i * 3]) & 0x0F) << 8
                    LowFreq2 = FreqArrayB[16 + i * 3]
                    if (HighFreq2 >= 8):
                        Freq2 = -(2 ** 12 - (HighFreq2) - LowFreq2) / 8.0
                    else:
                        Freq2 = ((HighFreq2) + LowFreq2) / 8.0
                    FreqArray.append(Freq2)
            elif (self.N > 1):
                FreqArray = []
                for j in range(self.N + 1):
                    for i in range(512):
                        if ((1537 * (j + 1) - 1520 + i * 3 - 1) < (self.index_e)):
                            HighFreq1 = ((FreqArrayB[1537 * (j + 1) - 1522 + i * 3 - 1]) & 0xF0) << 4
                            LowFreq1 = FreqArrayB[1537 * (j + 1) - 1521 + i * 3 - 1]
                            if (HighFreq1 >= 2048):
                                Freq1 = -(2 ** 12 - HighFreq1 - LowFreq1) / 8.0
                            else:
                                Freq1 = (HighFreq1 + LowFreq1) / 8.0
                            FreqArray.append(Freq1)
                            HighFreq2 = ((FreqArrayB[1537 * (j + 1) - 1522 + i * 3 - 1]) & 0x0F) << 8
                            LowFreq2 = FreqArrayB[1537 * (j + 1) - 1520 + i * 3 - 1]
                            if (HighFreq2 >= 2048):
                                Freq2 = -(2 ** 12 - HighFreq2 - LowFreq2) / 8.0
                            else:
                                Freq2 = (HighFreq2 + LowFreq2) / 8.0
                            FreqArray.append(Freq2)
        # print 'FreqArray',FreqArray
        # print len(FreqArray)
            return FreqArray

    def myfind(self, x, array):
        return [index for index in range(len(array)) if array[index] == x]


                #if __name__ == '__main__':
#    app = wx.App()
#    app.MainLoop()
#    dialog = PowerSptrDialog()
#    dialog.ShowModal()
        
