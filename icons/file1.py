# -*- coding: cp936 -*-
import wx
import wx.lib.buttons as buttons
class GenericButtonFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "Generic Button Example",
                            size=(500, 500))
        panel = wx.Panel(self, -1)
        sizer = wx.FlexGridSizer(1, 3, 20, 20)
        b = wx.Button(panel, -1, 'A wx.Button')
        b.SetDefault()
        sizer.Add(b)
        b = wx.Button(panel, -1, 'non-default wx.Button')
        sizer.Add(b)
        sizer.Add((10,10))
        b = buttons.GenButton(panel, -1, 'Genric Button')#基本的通用按钮
        sizer.Add(b)

        b = buttons.GenButton(panel, -1, 'disabled Generic')#无效的通用按钮
        b.Enable(False)
        sizer.Add(b)
        b = buttons.GenButton(panel, -1, 'F')#自定义尺寸和颜色的按钮
        b.SetFont(wx.Font(20, wx.SWISS, wx.NORMAL, wx.BOLD, False))
        b.SetBezelWidth(5)
        b.SetBackgroundColour("Navy")
        b.SetForegroundColour("white")
        b.SetToolTipString("This is a BIG button...")
        sizer.Add(b)
        bmp = wx.Image("Pause.png", wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        b = buttons.GenBitmapButton(panel, -1, bmp)#通用位图按钮
        sizer.Add(b)
        self.btest = buttons.GenBitmapToggleButton(panel, -1, bmp)#通用位图开关按钮
        sizer.Add(self.btest)
        b = buttons.GenBitmapTextButton(panel, -1, bmp, 'Bitmapped Text',size=(375, 75))#位图文本按钮
        b.SetUseFocusIndicator(False)
        sizer.Add(b)
        b = buttons.GenToggleButton(panel, -1, 'Toggle Button')#通用开关按钮
        sizer.Add(b)
        panel.SetSizer(sizer)
if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = GenericButtonFrame()
    frame.Show()
    app.MainLoop()
