import os

sourceVideo = "movie.mp4"
subtitles = "'media/IMG_958999.srt'"
force_style = ":force_style='Fontsize=24'"
outputVideo = "movie_output.mp4"
os.system("ffmpeg -i "+sourceVideo+" -i "+subtitles+" -c:s mov_text -c:v copy -c:a copy "+outputVideo)
