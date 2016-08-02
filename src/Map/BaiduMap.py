#encoding=utf-8
import wx
import os
import wx.lib.iewin as iewin
#from python_changeDataofJs import ChangeHotMap
import time
import wx.aui
class Map(wx.aui.AuiMDIChildFrame):
    def __init__(self,parent):
        wx.aui.AuiMDIChildFrame.__init__(self,parent,-1,title=u"地图显示                ")
        self.parent=parent
        self.ie = iewin.IEHtmlWindow(self, -1, style = wx.NO_FULL_REPAINT_ON_RESIZE)
        self.Bind(wx.EVT_WINDOW_DESTROY,self.OnClose)
        URL="http://localhost:8080/MapTest/map.jsp"
#         self.ie.Navigate(URL)
        
        self.box = wx.BoxSizer(wx.VERTICAL)
        self.box.Add(self.ie, 1, wx.GROW)
  
      #  self.ie.LoadUrl(URL)
        self.ie.Navigate(URL)
        self.SetSizer(self.box)
        self.SetAutoLayout(True)
  


    def OnClose(self, event):
        #os.chdir("./apache-tomcat-7.0.68//bin//")
        self.parent.MapFrame=None
        self.Close()
        
        


        
