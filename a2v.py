import os
import sys
import platform

def scale_and_rename(first_image):

        count = 1
        height = 1280
        width = 720
        for filename in os.listdir(os.getcwd()):
                if '.jpg' in filename:
                        if first_image == filename:
                                cmd = f"ffmpeg -i {filename} -vf scale={height}:{width} img_0.jpg"
                        else:
                                cmd = f"ffmpeg -i {filename} -vf scale={height}:{width} img_{count}.jpg"
                        os.system(cmd)
                        count += 1

def create_video(audio):
        cmd = (
                f"ffmpeg -loop 1 -i img_%d.jpg -i {audio} "
                f"-vf zoompan=d=(4+1)/1:fps=1,framerate=25:interp_start=0:interp_end=255:scene=100 "
                f"-c:v libx264 -c:a aac -shortest {audio.replace('mp3', 'mp4')}"
        )
        os.system(cmd)

def clean_up():
        '''delete scaled and renamed images'''
        if platform.system == 'Windows':
                command = 'del '
        else:
                command = 'rm '
        cmd = f"{command} img*"
        os.system(cmd)
        print("deleted all scaled images.")

if __name__ == "__main__":        
            
        audio = sys.argv[1] 
        first_image = sys.argv[2]  
        scale_and_rename(first_image)      
        create_video(audio)
        clean_up()
        print("conversion complete! check folder.")