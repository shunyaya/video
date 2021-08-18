import os
from moviepy import editor
from moviepy.editor import *
import speech_recognition as sr
import numpy as np
import auditok
FONT_URL = 'media/wt024.ttf'

record_start = np.zeros(100)
record_end = np.zeros(100)
duration = np.zeros(100)
speech = np.zeros(100)
num = 0
sub = []

# split returns a generator of AudioRegion objects
audio_regions = auditok.split(
    "media\\0708.wav",
    min_dur=0.01,        # minimum duration of a valid audio event in seconds
    max_dur=100,        # maximum duration of an event
    max_silence=2,      # maximum duration of tolerated continuous silence within an event
    energy_threshold=40  # threshold of detection
)

for i, r in enumerate(audio_regions):
    record_start[i] = r.meta.start
    record_end[i] = r.meta.end
    speech[i] = record_end[i] - record_start[i]
    print("Speech  {i}: {r.meta.start:.3f}s -- {r.meta.end:.3f}s".format(i=i,
          r=r), "Duration : ", speech[i])
    num = num+1
    filename = r.save("media\\region13.wav")

    r = sr.Recognizer()
    with sr.AudioFile("media\\region13.wav") as source:
        audio = r.record(source)

    # recognize speech using Google Speech Recognition
    try:
        s = r.recognize_google(audio, language='zh-TW', show_all=False)
        print(s)
        #print("Google Speech Recognition thinks you said " + r.recognize_google(audio_data=audio, key=None, language="zh-TW", show_all=True))

        text = str(s)
        rei = (int(record_start[i]), int(record_end[i]))
        sub.append(((rei), text))
        # sub.append(text)
        # spe=(int(record_end[i]),)
        #text=' '
        # sub.append((spe))
        # sub.append(text)

        #video = VideoFileClip("media/IMG_9589.MOV").subclip(int(record_start[i]), int(record_end[i]))

        # txt_clip = (TextClip(text, fontsize=70, color='white')
        #       .set_position('center')
        #      .set_duration(10))
        # result = CompositeVideoClip([video, txt_clip],)  # Overlay text on video
        # result.write_videofile("media/IMG_9589.mp4", fps=30)  # Many options...

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print(
            "Could not request results from Google Speech Recognition service; {0}".format(e))

print(sub)


def annotate(clip, txt, txt_color='white', fontsize=50, font=FONT_URL):
    """ Writes a text at the bottom of the clip. """
    txtclip = editor.TextClip(txt, fontsize=fontsize,
                              font=font, color=txt_color)
    cvc = editor.CompositeVideoClip(
        [clip, txtclip.set_pos(('center', 'bottom'))])
    return cvc.set_duration(clip.duration)


video = editor.VideoFileClip("media\\0708.mp4")
subs = sub
annotated_clips = [annotate(video.subclip(from_t, to_t), txt)
                   for (from_t, to_t), txt in subs]
final_clip = editor.concatenate_videoclips(annotated_clips)
final_clip.write_videofile("media\\070815.mp4")
