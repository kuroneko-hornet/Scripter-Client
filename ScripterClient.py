
import wx
from MainFrame import MainFrame

if __name__ == "__main__":
    app = wx.App(redirect=False)
    top_frame = MainFrame()
    top_frame.Show()
    app.MainLoop()
