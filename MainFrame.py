import wx
from wx.core import ID_ANY
from operator import add
import os


class MainFrame(wx.Frame):
    def __init__(self):
        self.title = "Scripter Client"
        self.size = (800, 600)
        super().__init__(parent=None, id=wx.ID_ANY, title=self.title, size=self.size)

        self.CreateStatusBar()
        self.SetStatusText('Testapp')
        self.GetStatusBar().SetBackgroundColour(None)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)

        top_panel = TopPanel(self)
        self.set_panel(top_panel)

    def set_panel(self, panel_instance):
        self.sizer.Clear(False)
        self.DestroyChildren()
        self.sizer.Add(panel_instance, 1, wx.EXPAND)
        self.sizer.Layout()

    def insert_message(self, label, pos, fontsize=15):
        message = wx.StaticText(parent=self, id=wx.ID_ANY, label=label, pos=pos)
        font = wx.Font(fontsize, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        message.SetFont(font)


class TopPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, wx.ID_ANY)
        self.parent = parent
        size = parent.size

        # [position(x,y), size]
        self.base_position = {}
        self.base_position["title"] = [size[0]/2 - 100, 30]
        self.base_position["message"] = [size[0]/4, self.base_position["title"][1] + 70]
        title_fontsize = 40
        self.video_path = ""

        # Welcome
        self.parent.insert_message("Welcome!!", self.base_position["title"], title_fontsize)

        self.parent.insert_message('Select The Video File to Edit', self.base_position["message"])
        tmp_pos = list(map(add, self.base_position["message"], [300, 0]))
        self.btn_selectvideo = wx.Button(self, wx.ID_ANY, 'select', pos=tmp_pos)
        self.btn_selectvideo.Bind(wx.EVT_BUTTON, self.select_videofile)

        tmp_pos = list(map(add, self.base_position["title"], [50, 150]))
        self.btn_start_edit = wx.Button(self, wx.ID_ANY, 'start editor', pos=tmp_pos)
        self.btn_start_edit.Bind(wx.EVT_BUTTON, self.start_editor)
        self.btn_start_edit.Disable()

    def select_videofile(self, event):
        dialog = wx.FileDialog(None, u'select the video file (mp4)')
        dialog.ShowModal()
        self.video_path = dialog.GetPath()
        tmp_pos = list(map(add, self.base_position["message"], [20, 30]))
        self.parent.insert_message(f"selected: '{self.video_path}'", pos=tmp_pos, fontsize=10)
        self.btn_start_edit.Enable()

    def save_json(self):
        fname = os.path.basename(self.video_path)
        with open(f"editinfo_{fname}.json", "w") as f:
            f.write("")

    def start_editor(self, event):
        self.save_json()
        editor_panel = EditorPanel(self.parent, self.video_path)
        self.parent.set_panel(editor_panel)


class EditorPanel(wx.Panel):
    def __init__(self, parent, video_path):
        super().__init__(parent, id=wx.ID_ANY)
        self.parent = parent
        self.video_path = video_path

        self.x_position = {
            "message": 25, "form": 45}
        self.y_position = []
        ypos = 25
        for i in range(15):  # 初期値10に 20,30,20,30,...と足してく
            self.y_position.append(ypos)
            ypos = ypos + 40 if i % 2 else ypos + 25

        self.input_info = {}
        # select video file
        print(self.video_path)
        # script
        self.parent.insert_message('Text', pos=(self.x_position["message"], self.y_position.pop(0)))
        self.insert_ctrl(wx.TextCtrl, "script", "sample text", style=wx.TE_MULTILINE, size=(360, 40))
        self.y_position = list(map(lambda x: x+20, self.y_position))
        # fontsize
        self.parent.insert_message('Fontsize', pos=(self.x_position["message"], self.y_position.pop(0)))
        self.insert_ctrl(wx.SpinCtrl, "fontsize", "60", size=(57, 22))
        # color
        self.parent.insert_message('Color', pos=(self.x_position["message"], self.y_position.pop(0)))
        self.insert_ctrl(wx.TextCtrl, "color", "black", size=(180, 20))
        # start time
        self.parent.insert_message('Start Time', pos=(self.x_position["message"], self.y_position.pop(0)))
        self.insert_ctrl(wx.SpinCtrlDouble, "starttime", "0.0", size=(57, 22))
        # end time
        self.parent.insert_message('End Time', pos=(self.x_position["message"], self.y_position.pop(0)))
        self.insert_ctrl(wx.SpinCtrlDouble, "endtime", "5.0", size=(57, 22))
        # xy mode
        self.parent.insert_message('XY Mode', pos=(self.x_position["message"], self.y_position.pop(0)))
        self.insert_ctrl(wx.TextCtrl, "xymode", "center", size=(105, 22))
        # start edit
        btn = wx.Button(self.panel, wx.ID_ANY, 'start edit', pos=(self.x_position["form"], self.y_position.pop(0)))
        btn.Bind(wx.EVT_BUTTON, self.info_toJson)

    def insert_ctrl(self, ctrl, info_key, value="", size="", style=0):
        self.input_info[info_key] =\
            ctrl(parent=self.panel, id=wx.ID_ANY, pos=(self.x_position["form"], self.y_position.pop(0)), value=value, size=size)

    def select_videofile(self, event):
        dialog = wx.FileDialog(None, u'select the video file (mp4)')
        dialog.ShowModal()
        path = dialog.GetPath()
        wx.StaticText(parent=self.panel, id=wx.ID_ANY, pos=(self.x_position+100, self.btn_selectvideo.Position[1]+3),
                      label=f"selected: '{path}'")

        print(self.btn_selectvideo.Position)
        print(path)

    def info_toJson(self, event):
        print({info_k: info_v.GetValue() for info_k, info_v in self.input_info.items()})