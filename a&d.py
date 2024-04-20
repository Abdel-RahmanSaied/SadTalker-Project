#
#
# # !git clone https://github.com/Dareenaymann/SadTalker.git &> /dev/null
#
# ### make sure that CUDA is available in Edit -> Nootbook settings -> GPU
# # !nvidia-smi --query-gpu=name,memory.total,memory.free --format=csv,noheader
#
# # Commented out IPython magic to ensure Python compatibility.
# # !update-alternatives --install /usr/local/bin/python3 python3 /usr/bin/python3.8 2
# # !update-alternatives --install /usr/local/bin/python3 python3 /usr/bin/python3.9 1
# # !sudo apt install python3.8
#
# # !sudo apt-get install python3.8-distutils
#
# # !python --version
#
# # !apt-get update
#
# # !apt install software-properties-common
#
# # !sudo dpkg --remove --force-remove-reinstreq python3-pip python3-setuptools python3-wheel
#
# # !apt-get install python3-pip
#
# print('Git clone project and install requirements...')
# # !git clone https://github.com/Dareenaymann/SadTalker.git &> /dev/null
# # %cd SadTalker
# # !export PYTHONPATH=/content/SadTalker:$PYTHONPATH
# !python3 -m pip install torch==1.12.1+cu113 torchvision==0.13.1+cu113 torchaudio==0.12.1 --extra-index-url https://download.pytorch.org/whl/cu113
# !apt update
# !apt install ffmpeg &> /dev/null
# !python3 -m pip install -r requirements.txt
#
# print('Download pre-trained models...')
# !rm -rf checkpoints
# !bash scripts/download_models.sh
#
# # borrow from makeittalk
# import ipywidgets as widgets
# import glob
# import matplotlib.pyplot as plt
# print("Choose the image name to animate: (saved in folder 'examples/')")
# img_list = glob.glob1('examples/source_image', '*.png')
# img_list.sort()
# img_list = [item.split('.')[0] for item in img_list]
# default_head_name = widgets.Dropdown(options=img_list, value='full3')
# def on_change(change):
#     if change['type'] == 'change' and change['name'] == 'value':
#         plt.imshow(plt.imread('examples/source_image/{}.png'.format(default_head_name.value)))
#         plt.axis('off')
#         plt.show()
# default_head_name.observe(on_change)
# display(default_head_name)
# plt.imshow(plt.imread('examples/source_image/{}.png'.format(default_head_name.value)))
# plt.axis('off')
# plt.show()
#
# # selected audio from exmaple/driven_audio
# img = 'examples/source_image/{}.png'.format(default_head_name.value)
# print(img)
# !python3 inference.py --driven_audio ./examples/driven_audio/RD_Radio31_000.wav \
#            --source_image {img} \
#            --result_dir ./results --still --preprocess full --enhancer gfpgan
#
# # visualize code from makeittalk
# from IPython.display import HTML
# from base64 import b64encode
# import os, sys
#
# # get the last from results
#
# results = sorted(os.listdir('./results/'))
#
# mp4_name = glob.glob('./results/*.mp4')[0]
#
# mp4 = open('{}'.format(mp4_name),'rb').read()
# data_url = "data:video/mp4;base64," + b64encode(mp4).decode()
#
# print('Display animation: {}'.format(mp4_name), file=sys.stderr)
# display(HTML("""
#   <video width=256 controls>
#         <source src="%s" type="video/mp4">
#   </video>
#   """ % data_url))