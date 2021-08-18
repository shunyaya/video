FONT_URL='/home/ball45/Downloads/TaipeiSansTCBeta-Light.ttf'
from moviepy import editor
import os.path as op

# handling with video source
source_file = input('Enter your video stream and file name:')
slash_pos = source_file.rfind('/')
dot_pos = source_file.rfind('.')
source_path, source_name, source_format = source_file[:slash_pos+1], source_file[slash_pos+1:dot_pos], source_file[dot_pos:]
source_clip = editor.VideoFileClip(source_file)

# handling with subtitle file
subtitle_file = open(source_path + source_name + '.srt')
subtitle_line = subtitle_file.readlines()
subtitle_file.close()

class Subtitle:
    def __init__(self, time_start, time_end, string):
        self.time_start = time_start
        self.time_end = time_end
        self.string = string

subtitle_list = []
for index in range(0, len(subtitle_line), 4):
    string = subtitle_line[index + 2]
    time_start = subtitle_line[index + 1][:12]
    time_end = subtitle_line[index+1][17:28]
    subtitle_list.append(Subtitle(time_start, time_end, string))


def annotate(clip, txt, txt_color='red', fontsize=50, font='Xolonium-Bold'):
    """ Writes a text at the bottom of the clip. """
    txtclip = editor.TextClip(txt, fontsize=fontsize, font=FONT_URL, color=txt_color)
    cvc = editor.CompositeVideoClip([clip, txtclip.set_pos(('center', 'bottom'))])
    return cvc.set_duration(clip.duration)

# bind subtitle file into video stream
annotated_clips = [annotate(source_clip.subclip(subtitle.time_start, subtitle.time_end), subtitle.string) for subtitle in subtitle_list]
final_clip = editor.concatenate_videoclips(annotated_clips)
final_clip.write_videofile("movie_output.mp4")