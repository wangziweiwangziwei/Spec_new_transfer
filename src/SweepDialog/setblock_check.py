# -*- coding: utf-8 -*- 

import wx
import wx.grid

class SetblockDlg ( wx.Dialog ):
    
    def __init__(self,parent):
        wx.Dialog.__init__(self,parent,-1,u"设置模板检测值",pos = wx.DefaultPosition,size = (470,550))

        self.blk_arr = []
        self.parent = parent 
        
        self.setblk_txt = wx.StaticText(self,-1,u"注意频率值必须设置在扫频范围内。")
        self.grid = wx.grid.Grid(self)
        self.grid.CreateGrid(50,4)
        self.grid.SetColLabelValue(0,u"起始频率")
        self.grid.SetColLabelValue(1,u"终止频率")
        self.grid.SetColLabelValue(2,u"功率谱")
        self.grid.SetColLabelValue(3,u"")
        self.grid.SetRowLabelSize(45)
        self.grid.DisableDragColSize()
        self.grid.DisableDragRowSize()
        self.btn_ok = wx.Button(self,-1,u"设置")
        self.btn_can = wx.Button(self,-1,u"取消")
        
        m_sizer = wx.BoxSizer(wx.VERTICAL)
        m_sizer.Add(self.setblk_txt,0,wx.ALL,5)
        
        g_sizer = wx.BoxSizer(wx.HORIZONTAL)
        g_sizer.Add(self.grid,0,wx.ALL,5)
        
        b_sizer = wx.BoxSizer(wx.VERTICAL)
        b_sizer.Add(self.btn_ok,0,wx.ALL|wx.BOTTOM,5)
        b_sizer.Add(self.btn_can,0,wx.ALL|wx.BOTTOM,5)
        
        g_sizer.Add(b_sizer,0,wx.ALL)
        m_sizer.Add(g_sizer,0,wx.ALL)
        self.SetSizer(m_sizer)
        
        self.Center()
        
        self.freq_s = self.parent.freq_s
        self.freq_e = self.parent.freq_e
        self.grid.SetCellValue(0,0,str(self.freq_s))
        

        self.grid.Bind(wx.grid.EVT_GRID_CELL_CHANGED,self.change_nc)
        
        self.btn_ok.Bind(wx.EVT_BUTTON,self.btn_setBlockThres)
        
    def change_nc(self,evt):
        for row in range(50):
            blk_b_e = self.grid.GetCellValue(row,1)
            if ((len(blk_b_e)> 0) & (len(self.grid.GetCellValue(row,2))> 0)):
                if (int(blk_b_e) < self.freq_e):
                    self.grid.SetCellValue(row+1,0,blk_b_e)

        
    def btn_setBlockThres(self,evt):
                     
        for row in range(50):
            
            if len(self.grid.GetCellValue(row,1)) > 0 :
                blk_arr_1 = []
                
                blk_arr_1.append(int(self.grid.GetCellValue(row,1)))
                blk_arr_1.append(int(self.grid.GetCellValue(row,2)))
                self.blk_arr.append(blk_arr_1)
            
            elif len(self.grid.GetCellValue(row,1)) == 0 :
                if len(self.grid.GetCellValue(row,0)) > 0 :
#                     if int(self.grid.GetCellValue(row,1)) < self.freq_e:
                    self.grid.SetCellValue(row,1,str(self.freq_e))
                    self.grid.SetCellValue(row,2,u'/')
                
                blk_arr_1 = [0,0]
                for i in range(50 - row):
                    self.blk_arr.append(blk_arr_1)
                break
            
            
#         print self.blk_arr
#         print len(self.blk_arr)
        
        
#         
# app = wx.App()
# dlg = SetblockDlg(None)
# dlg.ShowModal()
# app.MainLoop()
