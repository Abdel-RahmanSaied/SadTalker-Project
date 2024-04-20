import os
import glob
import matplotlib.pyplot as plt
# from IPython.display import display, HTML
import ipywidgets as widgets
from base64 import b64encode
import subprocess

class SadTalkerApp:
    def __init__(self):
        # self.setup_environment()
        # self.clone_repository()
        # self.install_dependencies()
        self.download_models()
        # pass
    def run_command(self, command):
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.returncode != 0:
            print("Error:", stderr.decode())
        return stdout.decode()

    # def setup_environment(self):
    #     # macOS specific cleanup and setup
    #     self.run_command('rm -rf /path/to/SadTalker')  # Adjust the path as necessary
    #
    # def clone_repository(self):
    #     print('Cloning Git repository and setting up...')
    #     self.run_command('git clone https://github.com/Dareenaymann/SadTalker.git &> /dev/null')
    #     os.environ['PYTHONPATH'] = f"{os.getcwd()}/SadTalker:${PYTHONPATH}"

    # def install_dependencies(self):
    #     print('Installing required packages...')
    #     # Use brew to install ffmpeg and other dependencies if needed
    #     self.run_command('brew install ffmpeg')
    #     # Install PyTorch with MPS support for Apple Silicon
    #     self.run_command('pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/macosx/arm64/nightly')

    def download_models(self):
        print('Downloading pre-trained models...')
        # Ensure the script is compatible with macOS
        self.run_command('rm -rf checkpoints && bash SadTalker/scripts/download_models.sh')

    def display_animation_interface(self):
        print("Choose the image name to animate: (saved in folder 'examples/source_image/')")
        img_list = glob.glob('SadTalker/examples/source_image/*.png')
        img_list.sort()
        img_list = [os.path.basename(item).split('.')[0] for item in img_list]
        default_head_name = widgets.Dropdown(options=img_list)
        display(default_head_name)
        img_path = f"SadTalker/examples/source_image/{default_head_name.value}.png"
        plt.imshow(plt.imread(img_path))
        plt.axis('off')
        plt.show()

    def run_inference(self, audio_path, img_path, result_dir='results'):
        command = f"python3 SadTalker/inference.py --driven_audio {audio_path} " \
                  f"--source_image {img_path} --result_dir {result_dir} --still --preprocess full --enhancer gfpgan"
        self.run_command(command)
        return result_dir

    def display_animation(self, result_dir):
        results = sorted(os.listdir(result_dir))
        mp4_name = glob.glob(f'{result_dir}/*.mp4')[0]
        mp4 = open(mp4_name, 'rb').read()
        data_url = "data:video/mp4;base64," + b64encode(mp4).decode()
        display(HTML(f"""
          <video width=256 controls>
                <source src="{data_url}" type="video/mp4">
          </video>
          """))

