import os
import sys
import subprocess
import json

audio_name = sys.argv[1]
image_names = sys.argv[2:]
number_of_images = len(image_names) + 1 # +1 because we use the first / cover image twice at both ends
output_name = audio_name.replace('mp3', 'mp4')

# for target video resolution, input images should be >= the following
height = 1280
width = 720

# get audio length and divide time equally for each image
args=("ffprobe", "-print_format", "json", "-show_entries", "format=duration","-i", audio_name)
ffprobeOutput = subprocess.check_output(args).decode('utf-8')
ffprobeOutput = json.loads(ffprobeOutput)
duration = ffprobeOutput['format']['duration']
duration = int(float(duration))
time_for_each_image = duration // number_of_images
fade_out_at = time_for_each_image - 1

# this forces all input images to resize to given height and width above
#the final string will look like the following, we'll construct it incrementally to avoid repeating
# filter_string = (
#     f"\"[0]scale={height}:{width}:force_original_aspect_ratio=decrease,pad={height}:{width}:(ow-iw)/2:(oh-ih)/2,setsar=1[i0];"
#     f"[1]scale={height}:{width}:force_original_aspect_ratio=decrease,pad={height}:{width}:(ow-iw)/2:(oh-ih)/2,setsar=1[i1];"
#     f"[2]scale={height}:{width}:force_original_aspect_ratio=decrease,pad={height}:{width}:(ow-iw)/2:(oh-ih)/2,setsar=1[i2];"
#     f"[3]scale={height}:{width}:force_original_aspect_ratio=decrease,pad={height}:{width}:(ow-iw)/2:(oh-ih)/2,setsar=1[i3];"
#     f"[i0][i1][i2][i3]concat=n=4\""
# )

filter_string = f"\""
for n in range(number_of_images):
    filter_string += f"[{n}]scale={height}:{width}:force_original_aspect_ratio=decrease,pad={height}:{width}:(ow-iw)/2:(oh-ih)/2,setsar=1, fade=t=in:st=0:d=2,fade=t=out:st={fade_out_at}:d=2[i{n}];"

for n in range(number_of_images):
    filter_string += f"[i{n}]"

filter_string+= f"concat=n={number_of_images}\""

# for single image video
# cmd = "ffmpeg -loop 1 -i " + image_name +  " -i " + audio_name + " -shortest -acodec copy " + output_name

# for multi image slideshow video
# again, the string will look like the following but we use concatenation to avoid repetition 
# cmd = (
#     f"ffmpeg -y "
#     f"-loop 1 -t {time_for_each_image} -i {cover_image} "
#     f"-loop 1 -t {time_for_each_image} -i {second_image} "
#     f"-loop 1 -t {time_for_each_image} -i {third_image} "
#     f"-loop 1 -i {cover_image} " 
#     f"-i {audio_name} "
#     f"-filter_complex {filter_string} "
#     f"-shortest "
#     f"-c:v libx264 -pix_fmt yuv420p -c:a aac {output_name}"
# )
cmd_string = f"ffmpeg -y "
for image in image_names:
    cmd_string += f"-loop 1 -t {time_for_each_image} -i {image} "

cmd_string += f"-loop 1 -i {image_names[0]} "
cmd_string += (
    f"-i {audio_name} "
    f"-filter_complex {filter_string} "
    f"-shortest "
    f"-c:v libx264 -pix_fmt yuv420p -c:a aac {output_name}"
)

os.system(cmd_string)