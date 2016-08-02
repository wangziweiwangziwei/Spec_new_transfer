# -*- coding: utf-8 -*-
import wx
from numpy import array, linspace
import matplotlib
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas 
from matplotlib.cm import jet 
import wx.aui 

class Water(wx.aui.AuiMDIChildFrame):
    def __init__(self,parent):
        wx.aui.AuiMDIChildFrame.__init__(self,parent,-1,title=u"瀑布图                    ")
        self.parent=parent
        self.waterFirst=1
        self.col=1024
        self.row=500
        self.rowCpy=5
        self.CreatePanel()
        self.setWfLabel_init()
        self.initWaterFall()

        self.Bind(wx.EVT_WINDOW_DESTROY,self.OnClose)

    def CreatePanel(self):
        self.Figure = matplotlib.figure.Figure(figsize=(1,1))
        self.axes=self.Figure.add_axes([0.05,0.05,0.93,0.93])
        self.FigureCanvas = FigureCanvas(self,-1,self.Figure)
        
        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        bSizer = wx.BoxSizer( wx.VERTICAL )
        bSizer.Add( self.FigureCanvas, 1, wx.EXPAND, 5 )
        self.SetSizer( bSizer )
        self.Layout()
        
        self.Centre( wx.BOTH )
        
    def initWaterFall(self):
        self.matrixFull = [[-120 for i in range(self.col)] for i in range(self.row)]
        norm = matplotlib.colors.Normalize(vmin=-120, vmax=0)
        self.image = self.axes.imshow(array(self.matrixFull),origin='lower',cmap=jet,norm=norm,interpolation='nearest')
        cbar=self.Figure.colorbar(self.image)
        ticks=linspace(-120,0,10)
        cbar.set_ticks(ticks)
        tick_labels=[str(int(i)) for i in ticks]
        cbar.set_ticklabels(tick_labels)
        self.FigureCanvas.draw()

    def WaterFall(self,yData):  ###传进来的不是列表
        
        del self.matrixFull[self.row-self.rowCpy:self.row]

        for i in range(self.rowCpy):
            self.matrixFull.insert(0,yData)
        self.image.set_data(array(self.matrixFull))
        self.FigureCanvas.draw()
      
           

    def setWfLabel_init(self,beginFreq=70,endFreq=5995):
        self.ylabel('Frame Number')
        self.xlabel('MHz')
        xLabelNum = 15
        xticks = linspace(0,self.col,15)
        self.axes.set_xticks(xticks)
        label=linspace(beginFreq,endFreq,15)
        xticklabels=['%0.1f'%i for i in label]
        self.axes.set_xticklabels(xticklabels,rotation=0) 
        intervalY = self.row/10
        yticks = range(0, self.row+1, intervalY)
        yticklabels = [str(i) for i in yticks]
        self.axes.set_yticks(yticks)
        self.axes.set_yticklabels(yticklabels,rotation=0)      

    def setWfLabel(self,beginFreq,endFreq):
        label=linspace(beginFreq,endFreq,15)
        xticklabels=['%0.1f'%i for i in label]
        self.axes.set_xticklabels(xticklabels,rotation=0)  


    def xlim(self,x_min,x_max):  
        self.axes.set_xlim(x_min,x_max)  
  
  
    def ylim(self,y_min,y_max):  
        self.axes.set_ylim(y_min,y_max)

    def xlabel(self,XabelString="X"):   
        self.axes.set_xlabel(XabelString)  
  
  
    def ylabel(self,YabelString="Y"):  
        self.axes.set_ylabel(YabelString)

    def OnClose(self,event):
        self.parent.WaterFrame=None
        self.Close()

