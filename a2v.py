import os, sys

audio_name = sys.argv[1]
image_name = sys.argv[2]
output = audio_name.replace('mp3', 'mp4')

cmd = "ffmpeg -loop 1 -i " + image_name +  " -i " + audio_name + " -shortest -acodec copy " + output 

os.system(cmd)