import os
import glob
import subprocess
import matplotlib.pyplot as plt

class SadTalkerApp:
    def __init__(self):
        self.download_models()
        pass

    def run_command(self, command):
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            print("Error:", stderr.decode())
        return stdout.decode()

    def download_models(self):
        print('Downloading pre-trained models...')
        self.run_command('rm -rf checkpoints && bash SadTalker/scripts/download_models.sh')

    def display_animation_interface(self):
        print("Choose the image name to animate: (saved in folder 'examples/source_image/')")
        img_list = glob.glob('SadTalker/examples/source_image/*.png')
        img_list.sort()
        img_list = [os.path.basename(item).split('.')[0] for item in img_list]
        # This is just for command line. User needs to manually type the selection.
        print("Available images:", img_list)
        selected_image = input("Enter the name of the image to animate: ")
        img_path = f"SadTalker/examples/source_image/{selected_image}.png"
        plt.imshow(plt.imread(img_path))
        plt.axis('off')
        plt.show()
        return img_path

    def run_inference(self, audio_path, img_path, result_dir='results'):
        command = f"python3 SadTalker/inference.py --driven_audio {audio_path} " \
                  f"--source_image {img_path} --result_dir {result_dir} --still --preprocess full --enhancer gfpgan"
        self.run_command(command)
        return result_dir

    def display_animation(self, result_dir):
        results = sorted(os.listdir(result_dir))
        print("Results:", results)
        mp4_name = glob.glob(f'{result_dir}/*.mp4')[0]
        print(f"Animation video saved at: {os.path.abspath(mp4_name)}")
        print("You can view the video with any media player that supports MP4 format.")