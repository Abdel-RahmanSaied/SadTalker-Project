import os
import sys
import glob
from PIL import Image
import subprocess
import matplotlib.pyplot as plt
from torchvision.transforms.functional import rgb_to_grayscale

from SadTalker.inference import SadTalker


class SadTalkerApp:
    def __init__(self):
        # self.download_models()
        self.audio_path = None
        self.img_path = None

    def setParams(self, audio_path, img_path):
        self.audio_path = audio_path
        self.img_path = img_path

    def resize_image(self,  desired_width=800):
        # Load the image
        image_path = self.img_path
        img = Image.open(image_path)

        # Extract the base name for the image without path and extension
        img_name = img.filename.split('/')[-1].split('.')[0]

        # Calculate the scaling factor to maintain aspect ratio
        scaling_factor = desired_width / img.width

        # Calculate the new height to maintain aspect ratio
        new_height = int(img.height * scaling_factor)

        # Resize the image using the LANCZOS filter
        img_resized = img.resize((desired_width, new_height), Image.Resampling.LANCZOS)

        # Save the resized image
        resized_image_path = f'{img_name}_resized.jpg'
        img_resized.save(resized_image_path)

        print("Resized image saved as:", resized_image_path)
        return resized_image_path

    def checkSystem(self):
        if sys.platform == "darwin":
            return "macOS"
        elif sys.platform == "linux":
            return "Linux"
        elif sys.platform == "win32":
            return "Windows"
        else:
            return "Unknown"

    def setup_environment(self):
        system = self.checkSystem()
        if system == "Linux":
            self.run_command('bash SadTalker/scripts/install_reqs_linux.sh')
        elif system == "macOS":
            self.run_command('bash SadTalker/scripts/install_reqs_macOS.sh')

        self.download_models()

        print("Environment setup complete.")

    def run_command(self, command):
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            print("Error:", stderr.decode())
        return stdout.decode()

    def download_models(self):
        print('Downloading pre-trained models...')
        if os.listdir('SadTalker/checkpoints') == 15:
            print("Models already downloaded.")
        else:
            self.run_command('rm -rf SadTalker/checkpoints && bash SadTalker/scripts/download_models.sh')

    def run_inference(self, result_dir='results'):
        if not os.path.exists(result_dir):
            os.makedirs(result_dir)

        driven_audio = self.audio_path
        resize_image = self.resize_image()

        generatedVideo = SadTalker(source_image=resize_image, driven_audio=driven_audio, result_dir=result_dir).run()
        print("Generated video:", generatedVideo)
        return result_dir
