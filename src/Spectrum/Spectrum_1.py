# -*- coding: utf-8 -*-
import wx
from numpy import array, linspace
import matplotlib
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas 



# from DragMarker import DraggableRectangle
import wx.aui 
from src.SweepDialog.download_choice import dialog_download
from src.Thread import thread_localsave

class Spec(wx.aui.AuiMDIChildFrame):
    def __init__(self,parent,title):
        if(title==1): name=u"功率谱图                "
        else: name=u"信号分析功率谱图       "
        wx.aui.AuiMDIChildFrame.__init__(self,parent,-1,name)
 
        topSplitter = wx.SplitterWindow(self)
        hSplitter = wx.SplitterWindow(topSplitter)

        self.panelAbFreq = MyListCtrlAbFreq(hSplitter)
        self.panelQuery = MyListCtrlQuery(hSplitter)
        hSplitter.SplitHorizontally(self.panelAbFreq, self.panelQuery)
        hSplitter.SetSashGravity(0.5)

        self.panelFigure = PanelSpec(topSplitter,parent)
        topSplitter.SplitVertically(self.panelFigure, hSplitter)
        topSplitter.SetSashGravity(0.8)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(topSplitter, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
        ###################
        
        self.iq_sequence=0
        
        ###################
        
class MyListCtrlAbFreq(wx.ListCtrl):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES)
        self.InsertColumn(0, u'序号')
        self.InsertColumn(1, u'异常频点频率(MHz)')
        self.InsertColumn(2, u'异常频点功率(dB)')
        self.SetColumnWidth(0, 50)
        self.SetColumnWidth(1, 120)
        self.SetColumnWidth(2, 130)
        for i in range(1,201):
            self.InsertStringItem(i-1,str(i))

class MyListCtrlQuery(wx.ListCtrl):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES)
        self.InsertColumn(0, u"帧类型")
        self.InsertColumn(1, u'参数类型')
        self.InsertColumn(2, u'参数值')
        self.SetColumnWidth(0, 100)
        self.SetColumnWidth(1, 100)
        self.SetColumnWidth(2, 100)
        for i in range(1,5301):
            self.InsertStringItem(i-1,str(i))

    
class PanelSpec(wx.Panel):
    def __init__(self,parent,parentMainFrame):
        wx.Panel.__init__(self,parent)
        self.CreatePanel()
        self.setSpLabel()
        self.parent=parentMainFrame 
        
        self.FFT_Max_X=5995
        self.FFT_Min_X=70
        self.FFT_Max_Y=20
        self.FFT_Min_Y=-120 
        
        ######## upload ###########
        self.start_upload=0
       
        
        ###### download #########
        self.download=0
        self.dir=""
        
        ############################
        self.thread=0
    
    def getstartUploadOnce(self):
        return self.start_upload
    
    
    def getisDownLoad(self):
        return self.download
  
    def getDownloadDir(self):
        return self.dir 
    
    
    def restore2unstart(self):
        self.start_upload=0
    
    
    def restoreisDownLoad(self):
        self.download=0
    
    ######################################################

    def CreatePanel(self):
        self.Figure = matplotlib.figure.Figure()
        self.axes=self.Figure.add_axes([0.05,0.05,0.93,0.93])
        self.FigureCanvas = FigureCanvas(self,-1,self.Figure)
        self.ButtonAutoY=wx.Button(self,-1,label=u"纵轴恢复")
        self.ButtonAutoX=wx.Button(self,-1,label=u"横轴恢复")
        self.Max_Y=wx.TextCtrl(self,-1,'20',size=(60,20),style=wx.TE_PROCESS_ENTER)
        self.Min_Y=wx.TextCtrl(self,-1,'-120',size=(60,20),style=wx.TE_PROCESS_ENTER)
        self.Min_X=wx.TextCtrl(self,-1,'70',size=(60,20),style=wx.TE_PROCESS_ENTER)
        self.Max_X=wx.TextCtrl(self,-1,'5995',size=(60,20),style=wx.TE_PROCESS_ENTER)

        self.Upload=wx.Button(self,-1,label=u"手动上传")
        self.Download=wx.Button(self,-1,label=u"本地存储")
#         self.str_rbw = 'RBW:__'
#         self.str_vbw = 'VBW:__'

        
        self.rbw = wx.StaticText(self,-1,'RBW:_____')
        self.vbw = wx.StaticText(self,-1,'VBW:_____')

        self.show_txt = wx.StaticText(self, -1, u'显示模式：')
        self.showList = [u"实时功率谱",u"最大保持",u"最小保持",u"迹线平均"]
        self.show_box = wx.ComboBox(self,-1,u"实时功率谱",choices=self.showList,style=wx.CB_DROPDOWN)
        
        ###################################test sizer##############################
        font = wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD)

        self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
        
        bSizer4 = wx.BoxSizer( wx.VERTICAL )
        
        gSizer6 = wx.GridSizer( 1, 7, 0, 0 )
        
        gSizer6.Add( self.ButtonAutoX, 0, wx.ALL|wx.ALIGN_BOTTOM|wx.ALIGN_RIGHT, 5 )
        
        gSizer6.Add( self.ButtonAutoY, 0, wx.ALL, 5 )
        gSizer6.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
        gSizer6.Add(self.show_txt,0,wx.ALL|wx.ALIGN_CENTER|wx.ALIGN_RIGHT,5)
        gSizer6.Add(self.show_box,0,wx.ALL|wx.ALIGN_CENTER|wx.ALIGN_LEFT,5)
           
        gSizer6.Add( self.Upload, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )
        gSizer6.Add( self.Download, 0, wx.ALL|wx.ALIGN_LEFT, 5 )
        
        
        bSizer4.Add( gSizer6, 0, wx.EXPAND, 5 )
        
        bSizer5 = wx.BoxSizer( wx.HORIZONTAL )
        
        gSizer8 = wx.GridSizer( 3, 1, 0, 0 )
        

        gSizer8.Add( self.Max_Y, 0, wx.ALL, 5 )

        text1=wx.StaticText(self, -1, 'dBm')
        text1.SetFont(font)
        gSizer8.Add(text1,0,wx.ALIGN_CENTER,5)
        
        gSizer8.Add( self.Min_Y, 0, wx.ALIGN_BOTTOM|wx.ALL, 5 )
        
        
        bSizer5.Add( gSizer8, 0, wx.EXPAND, 5 )
        
        gSizer10 = wx.GridSizer( 1, 1, 0, 0 )
        
        
        gSizer10.Add( self.FigureCanvas, 1, wx.ALL|wx.EXPAND, 5 )
        
        
        bSizer5.Add( gSizer10, 5, wx.EXPAND, 5 )
        
        
        bSizer4.Add( bSizer5, 4, wx.EXPAND, 5 )
        
        gSizer9 = wx.GridSizer( 1, 5, 0, 0 )
        
#         gSizer9.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
#         self.m_textCtrl16 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), 0 )
        gSizer9.Add( self.Min_X, 0, wx.ALL, 5 )
        
        #gSizer9.AddSpacer((0,0),1,wx.EXPAND,5)
        gSizer9.Add(self.rbw,0,wx.ALL,5)
        gSizer9.Add(self.vbw,0,wx.ALL,5)

        text2 = wx.StaticText(self, -1, 'MHz')
        text2.SetFont(font)
        gSizer9.Add(text2, 0, wx.ALIGN_CENTER, 5)
        
#         self.m_textCtrl17 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 80,-1 ), 0 )
        gSizer9.Add( self.Max_X, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
        
        
        bSizer4.Add( gSizer9, 0, wx.EXPAND, 5 )
        
        
        self.SetSizer( bSizer4 )
        self.Layout()
        
        self.Centre( wx.BOTH )
        
        
        
        
        
        
        
        #####################################################################################
        self.Bind(wx.EVT_TEXT_ENTER,self.OnEnterMin_X,self.Min_X)
        self.Bind(wx.EVT_TEXT_ENTER,self.OnEnterMax_X,self.Max_X)
        self.Bind(wx.EVT_TEXT_ENTER,self.OnEnterMax_Y,self.Max_Y)
        self.Bind(wx.EVT_TEXT_ENTER,self.OnEnterMin_Y,self.Min_Y)
        self.Bind(wx.EVT_BUTTON,self.OnAutoX,self.ButtonAutoX)
        self.Bind(wx.EVT_BUTTON,self.OnAutoY,self.ButtonAutoY)
        self.Bind(wx.EVT_BUTTON,self.OnUpload,self.Upload)
        self.Bind(wx.EVT_BUTTON,self.OnDownload,self.Download)
        
        
        self.popupmenu=wx.Menu()
        StringList=["Add Marker","Remove Marker", "All Markers Off"]
        for text in StringList:
            item=self.popupmenu.Append(-1,text)
            self.FigureCanvas.Bind(wx.EVT_CONTEXT_MENU,self.OnShowPopup)
            self.FigureCanvas.Bind(wx.EVT_MENU,self.OnPopupItemSelected,item)
        
        '''
        Array=linspace(70, 5995,238)
        self.xDataList=[]
        self.LineSpec=[]
        self.LineSpecBack=[]
        for i in xrange(237):
            xData=linspace(Array[i],Array[i+1],1024)
            self.xDataList.append(xData)
        
        ydata=[0]*1024
        for xData in self.xDataList:
            lineSpec,=self.axes.plot(xData,ydata,'y')
            lineSpecBack,=self.axes.plot(xData,ydata,'r')
            self.LineSpec.append(lineSpec)
            self.LineSpecBack.append(lineSpecBack)
        '''
        self.xData=linspace(70,6470,1024)
        self.yData=[0]*1024
        self.lineSpec,=self.axes.plot(self.xData,self.yData,'y')
        self.lineSpecBack,=self.axes.plot(self.xData,self.yData,'r')
        ####Marker############
        self.drs=[]
    
    
    def OnUpload(self,event):
        self.start_upload=1
                
                
    def OnDownload(self,event):
        if(self.Download.GetLabel()==u"本地存储"):
            '''
            dlg=dialog_download(self)
            dlg.ShowModal()
            if(dlg.isValid):
                self.dir=dlg.m_dirPick.GetPath()
                print self.dir 
                '''
            self.download=1
            self.Download.SetLabel(u"停止存储")
            '''start the thread localsave'''
            if(self.thread==0):
                self.thread=thread_localsave.LocalSaveThread(self.parent,
                    self.parent.queueFFTLocalSave, self.parent.queueAbLocalSave)
                self.thread.start()

            else:
                self.thread.event.set()
                
        else:
            '''stop the thread localsave'''
            self.thread.stop()
            
            self.Download.SetLabel(u"本地存储")
            self.download=0
            
            

    def OnAutoX(self,event):
        self.setSpLabel(begin_X=self.parent.FreqMin,end_X=self.parent.FreqMax ,
            begin_Y=self.FFT_Min_Y,end_Y=self.FFT_Max_Y)
        self.FigureCanvas.draw()
        self.FFT_Min_X=self.parent.FreqMin
        self.FFT_Max_X=self.parent.FreqMax   
        self.Min_X.SetValue(str(self.FFT_Min_X))
        self.Max_X.SetValue(str(self.FFT_Max_X))

    def OnAutoY(self,event):
        self.setSpLabel(begin_X=self.FFT_Min_X,end_X=self.FFT_Max_X)
        self.FigureCanvas.draw()
        self.FFT_Min_Y=-120
        self.FFT_Max_Y=20
        self.Min_Y.SetValue("-120")
        self.Max_Y.SetValue("20")

    def OnEnterMin_X(self,event):
        self.FFT_Min_X=int(self.Min_X.GetValue())
        self.setSpLabel(self.FFT_Min_X,self.FFT_Max_X,self.FFT_Min_Y,self.FFT_Max_Y)
        self.FigureCanvas.draw()

    def OnEnterMax_X(self,event):
        self.FFT_Max_X=int(self.Max_X.GetValue())
        self.setSpLabel(self.FFT_Min_X,self.FFT_Max_X,self.FFT_Min_Y,self.FFT_Max_Y)
        self.FigureCanvas.draw()

    def OnEnterMin_Y(self,event):
        self.FFT_Min_Y=int(self.Min_Y.GetValue())
        self.setSpLabel(self.FFT_Min_X,self.FFT_Max_X,self.FFT_Min_Y,self.FFT_Max_Y)
        self.FigureCanvas.draw()

    def OnEnterMax_Y(self,event):
        self.FFT_Max_Y=int(self.Max_Y.GetValue())
        self.setSpLabel(self.FFT_Min_X,self.FFT_Max_X,self.FFT_Min_Y,self.FFT_Max_Y)
        self.FigureCanvas.draw()
    
    def OnShowPopup(self,event):
        pos=event.GetPosition()
        pos=self.FigureCanvas.ScreenToClient(pos)
        self.FigureCanvas.PopupMenu(self.popupmenu,pos)

    def OnPopupItemSelected(self,event):
        item=self.popupmenu.FindItemById(event.GetId())
        text=item.GetText()
        if(text=="Add Marker"):
            self.OnAddMarker()  
        elif(text=="Remove Marker"):
            self.OnRemove()
        elif(text=="All Markers Off"):
            self.OnAllRemove()
    
    def DrawMarker(self,Max_X,Max_Y):
        distance=((self.FFT_Max_X-self.FFT_Min_X)/10)**2
        index=len(self.drs)+1
        rect,=self.axes.plot(Max_X,Max_Y,'rd',markersize=10)
        text=self.axes.text(Max_X+5,Max_Y+2,'M'+str(index),color='r')
        textM=self.axes.text(self.FFT_Min_X+5,self.FFT_Max_Y-5*(index),'M'+str(index)+':'  \
            +'%.2f'%(Max_X)+'MHz  '+'%.2f'%(Max_Y)+'dBm')
#         DragRect=DraggableRectangle(rect,text,textM,self.LineSpec,self.FigureCanvas)
#         DragRect.setM_id('M'+str(index)+':')
#         
#         DragRect.setRadius(distance)
#         DragRect.connect()
#         self.drs.append(DragRect)
        #self.FigureCanvas.draw()
 
    def OnAddMarker(self):
        if(len(self.drs)<4):
            startSection=(self.FFT_Min_X-70)/25 
            endSection=(self.FFT_Max_X-70)/25
            lenStart=len(self.LineSpec[startSection].get_ydata())
            lenEnd=len(self.LineSpec[endSection].get_ydata())
            indexStart=int((self.FFT_Min_X-(startSection*25+70))*lenStart/25.0)
            indexEnd=int((self.FFT_Max_X-(endSection*25+70))*lenEnd/25.0)
            MaxList=[]
            MaxList.append(max(list(self.LineSpec[startSection].get_ydata())[indexStart:lenStart]))
            for i in range(startSection+1,endSection,1):
                MaxList.append(max(list(self.LineSpec[i].get_ydata())))
            if(indexEnd!=0):
                MaxList.append(max(list(self.LineSpec[endSection].get_ydata())[0:indexEnd]))
                
            Max_Y=max(MaxList)
            Max_Y_Index=MaxList.index(Max_Y)+startSection
            y=self.LineSpec[Max_Y_Index].get_ydata()
            Max_X_Index=list(y).index(Max_Y)
            Max_X=70+Max_Y_Index*25+Max_X_Index*25.0/len(y) 
            self.DrawMarker(Max_X,Max_Y)


    def OnRemove(self):
        
        if(len(self.axes.texts)):
            self.axes.lines.pop()
            self.axes.texts.pop()
            self.axes.texts.pop()
            self.drs.pop()
            #self.FigureCanvas.draw()

    def OnAllRemove(self):
       
        while(len(self.axes.texts)):
            self.axes.lines.pop()
            self.axes.texts.pop()
            self.axes.texts.pop()
            self.drs.pop()
        #self.FigureCanvas.draw()



    def setSpLabel(self, begin_X=70, end_X=5995,begin_Y=-120,end_Y=20):
        # self.ylabel('dBuV/m')
        # self.xlabel('MHz')
        self.ylim(begin_Y,end_Y)
        self.xlim(begin_X,end_X)
        yticks=linspace(begin_Y,end_Y,15)  ##11个数总共###
        yticklabels = [str(int(i)) for i in yticks]  
        xticks=linspace(begin_X,end_X,11)

        xticklabels = [str('%0.1f'%(i)) for i in xticks]
        self.axes.set_xticks(xticks)
        self.axes.set_xticklabels(xticklabels,rotation=0)
        self.axes.set_yticks(yticks)
        self.axes.set_yticklabels(yticklabels,rotation=0)
        self.axes.grid(True)
        #self.FigureCanvas.draw()


    def PowerSpectrum(self,funcPara,y):
       
        if(funcPara==0x51 or funcPara==0x56):
            
            self.lineSpec.set_ydata(array(y))
            '''
            for i in range(len(self.drs)):
                self.drs[i].yData=self.LineSpec 
                self.DrawAfterRelease()
                '''
        elif(funcPara==0x52 or funcPara==0x57):
            
            self.lineSpecBack.set_ydata(array(y))
        self.FigureCanvas.draw()
                
    def DrawAfterRelease(self):
        
        for i in range(len(self.drs)):
            xData=self.drs[i].rect.get_xdata()

            index=(int(xData)-70)/25
            Section=index*25+70
            y=self.LineSpec[index].get_ydata()
            
            index_Y=(xData-Section)*len(y)/25.0
            Marker_Y=list(y)[int(index_Y)]
            self.drs[i].rect.set_ydata(Marker_Y)
            self.drs[i].textMarker.set_position((xData,Marker_Y+2))
            self.drs[i].textM.set_text(self.drs[i].M_index+'%.2f'%(xData)+ \
                'MHz  '+'%.2f'%(Marker_Y)+'dBm')
      

    def xlim(self,x_min,x_max):  
        self.axes.set_xlim(x_min,x_max)  
  
    def ylim(self,y_min,y_max):  
        self.axes.set_ylim(y_min,y_max)

    def xlabel(self,XabelString="X"):   
        self.axes.set_xlabel(XabelString)  
  
  
    def ylabel(self,YabelString="Y"):  
        self.axes.set_ylabel(YabelString)
        

            
