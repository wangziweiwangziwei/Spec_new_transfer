# -*- coding: cp936 -*-
import wx

import wx.aui 
import matplotlib
#matplotlib.use("WXAgg")    
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

from math import sqrt, log10, pi, cos, sin, atan
from wx import Left
from src.SweepDialog.download_choice import dialog_download


class WaveIQ(wx.aui.AuiMDIChildFrame):
    def __init__(self,parent,name):
        wx.aui.AuiMDIChildFrame.__init__(self,parent,-1,title=name)
        self.Fs=5e6
        self.parent=parent

        
        self.CreatePanel()  
        self.setWaveLabel()
    
#     def getisUpload(self):
#         return self.isUpload
#     def getisDownload(self):
#         return self.isDownload
#     def getDownloadDir(self):
#         return self.dir 
#     
#     def restoreisUpload(self):
#         self.isUpload=0
#     
#     def restoreisDownload(self):
#         self.isDownload=0
    
    
    
    ###################################################################
    def CreatePanel(self):
        self.Figure = matplotlib.figure.Figure(figsize=(1,1))
        self.axes=self.Figure.add_axes([0.1,0.1,0.8,0.8])
        self.FigureCanvas = FigureCanvas(self,-1,self.Figure)
        
#         self.Upload=wx.Button(self,-1,size=(100,25),label="Upload")
#         self.Download=wx.Button(self,-1,size=(100,25),label="Download")
        
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
#         bSizerh = wx.BoxSizer( wx.HORIZONTAL )
#         bSizerh.Add( self.Upload, 0, wx.ALL|wx.LEFT , 5 )
#         bSizerh.Add(self.Download,0,wx.ALL|wx.RIGHT, 5)
    
        bSizer = wx.BoxSizer( wx.VERTICAL )
#         bSizer.Add(bSizerh, 0, wx.EXPAND, 5 )
        bSizer.Add( self.FigureCanvas, 1, wx.EXPAND, 5 )
        self.SetSizer( bSizer )
        self.Layout()
        self.Centre( wx.BOTH )
        
        #Events
#        self.Bind(wx.EVT_BUTTON,self.OnUpload,self.Upload)
#        self.Bind(wx.EVT_BUTTON,self.OnDownload,self.Download)
        #self.Bind(wx.EVT_WINDOW_DESTROY,self.OnCloseWindow)
        
        
        #xdata=[i for i in xrange(2000)]
        #ydata=[0]*2000
        xdata=[]
        ydata=[]
        
        self.LineWave,=self.axes.plot(xdata,ydata,'r')

        self.LineWave.set_xdata([i for i in xrange(2000)])

    
    def OnCloseWindow(self, event):
        ###先停止或者取消画图线程#####
        self.parent.WaveFrame=None 
        print 'xxxxxxxxxxxx'
        self.Close()
    
#     def OnUpload(self,event):
#         self.isUpload=1
#             
#                 
#     def OnDownload(self,event):
#         dlg=dialog_download(self)
#         dlg.ShowModal()
#         if(dlg.isValid):
#             self.isDownload=1
#             self.dir=dlg.m_dirPick.GetPath()
#             print self.dir      
       
    def setWaveLabel(self,begin_X=0,end_X=100,begin_Y=-1 ,end_Y=1 ):
    
        yLabelNum=8
        self.axes.set_xlim(begin_X,end_X)
        self.axes.set_ylim(begin_Y,end_Y)
        interval=float(end_Y-begin_Y)/ yLabelNum
        yticks=[(begin_Y+interval*i) for i in range(yLabelNum+1)]
        yticklabels = [str(int(n*100)/100.00) for n in yticks]
        self.axes.set_ylabel('V',rotation=1)
        
        xLabelNum = 9
        interval = (end_X-begin_X)/xLabelNum
        xticks = [begin_X+interval*i for i in range(xLabelNum+1)]
        xticklabels = [str('%0.2f'%i) for i in xticks]
        self.axes.set_xlabel('s')
        self.axes.set_xticks(xticks)
        self.axes.set_xticklabels(xticklabels,rotation=0)
        self.axes.set_yticks(yticks)
        self.axes.set_yticklabels(yticklabels,rotation=0)
        self.axes.grid(True)


    def Wave(self, chData,color):
        self.LineWave.set_color(color)
        self.LineWave.set_ydata(chData)
        self.FigureCanvas.draw()    

        
        
            
        


        



        
