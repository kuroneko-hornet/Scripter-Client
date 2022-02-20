from turtle import width
from moviepy.editor import \
    VideoFileClip, TextClip, concatenate_videoclips, CompositeVideoClip
import json


class VideoEditor():
    script_list = []
    annotated_clip_list = []

    def __init__(self, path):
        self.clip = VideoFileClip(path)
        self.frames = self.clip.reader.nframes
        self.fps = self.clip.fps
        self.duration = self.clip.duration
        self.size = [self.clip.w, self.clip.h]

    def print_info(self):
        print(f"frames: {self.frames}")
        print(f"fps: {self.fps}")
        print(f"duration: {self.duration}")
        print(f"size: {self.size}")
        print("script_list:")
        [print(i) for i in self.script_list]

    def preview_script(self, script_info):
        print(script_info)
        onesecond_before = self.clip.subclip(script_info.duration[0]-1, script_info.duration[0])
        annotation = self.create_annotation(script_info)
        onesecond_after = self.clip.subclip(script_info.duration[1], script_info.duration[1]+1)

        preview_clip = concatenate_videoclips([onesecond_before, annotation, onesecond_after])

        audio = preview_clip.audio.set_fps(44100)
        preview_clip = preview_clip.without_audio().set_audio(audio)
        preview_clip = preview_clip.resize(width=500)
        preview_clip.preview(fps=60)

    def create_annotation(self, script):
        sub_clip = self.clip.subclip(*script.duration)
        txtclip = TextClip(script.text, fontsize=script.fontsize, font=script.font, color=script.color)
        cvc = CompositeVideoClip([sub_clip, txtclip.set_pos(script.pos)])
        return cvc.set_duration(sub_clip.duration)

    def script_list_to_annotation(self):
        for script in self.script_list:
            self.annotated_clip_list.append(self.create_annotation(script))

    def concatenate_annotation(self, output_fname="created_by_moviepy_code(default_file_name).mp4"):
        final_clip = concatenate_videoclips(self.annotated_clip_list)
        final_clip.write_videofile(output_fname)
        self.annotated_clip_list = []

    def create_script_infolist(self, script_json_path):
        with open(script_json_path, 'r') as f:
            script_dict = json.load(f)
        for script_info in script_dict.values():
            if not self.script_list:
                self.script_list.append(ScriptInfo(" ", [0.0, script_info["duration"][0]]))
            else:
                self.script_list.append(ScriptInfo(" ", [self.script_list[-1].duration[1], script_info["duration"][0]]))
            self.script_list.append(ScriptInfo(**script_info))


class ScriptInfo():
    def __init__(self, text, duration, fontsize=50, font="ヒラギノ丸ゴ-ProN-W4", color="white", pos=("center", "bottom")):
        self.text = text
        self.duration = duration  # [start, end]
        self.fontsize = fontsize
        self.font = font
        self.color = color
        self.pos = pos

    def __str__(self):
        return \
            "  print ScriptInfo object:\n"\
            f"    text: {self.text}\n"\
            f"    duration: {self.duration}\n"\
            f"    fontsize: {self.fontsize}\n"\
            f"    font: {self.font}\n"\
            f"    color: {self.color}\n"\
            f"    pos: {self.pos}"


if __name__ == "__main__":

    v_editor = VideoEditor("movie-data/IMG_7033.mp4")

    script_json_path = "Scripter-Client/scriptinfo.json"
    # v_editor.create_script_infolist(script_json_path)
    # v_editor.print_info()
    sample_script = ScriptInfo("サンプル", [1.0, 5.5], pos=("center", "center"))
    v_editor.preview_script(sample_script)

    # v_editor.script_list_to_annotation()
    # v_editor.concatenate_annotation("textclip.mp4")
