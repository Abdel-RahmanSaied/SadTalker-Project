import os
import shutil
import sys
from time import strftime
import torch

# Import necessary SadTalker components
from SadTalker.src.facerender.animate import AnimateFromCoeff
from SadTalker.src.generate_batch import get_data
from SadTalker.src.generate_facerender_batch import get_facerender_data
from SadTalker.src.test_audio2coeff import Audio2Coeff
from SadTalker.src.utils.init_path import init_path
from SadTalker.src.utils.preprocess import CropAndExtract


class SadTalker:
    def __init__(self, source_image='./examples/source_image/full_body_1.png', driven_audio='./examples/driven_audio/bus_chinese.wav',
                 result_dir='./SadTalker/results', pose_style=0, batch_size=2, size=256, expression_scale=1.0, input_yaw=None,):
        self.current_root_path = os.path.join(os.path.dirname(sys.argv[0]), 'SadTalker')
        sys.path.append(self.current_root_path)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # Configuration parameters
        self.source_image = source_image
        self.driven_audio = driven_audio
        self.ref_eyeblink = None
        self.ref_pose = None
        self.checkpoint_dir = './SadTalker/checkpoints'
        self.result_dir = './results'
        self.pose_style = 0
        self.batch_size = batch_size
        self.size = size
        self.expression_scale = expression_scale
        self.input_yaw = input_yaw
        self.input_pitch = None
        self.input_roll = None
        self.enhancer = None
        self.background_enhancer = None
        self.still = False
        self.preprocess = 'crop'
        self.old_version = False

        self.sadtalker_paths = init_path(self.checkpoint_dir, os.path.join(self.current_root_path, 'src/config'),
                                         self.size, self.old_version, self.preprocess)

        # Initialize models
        self.preprocess_model = CropAndExtract(self.sadtalker_paths, self.device)
        self.audio_to_coeff = Audio2Coeff(self.sadtalker_paths, self.device)
        self.animate_from_coeff = AnimateFromCoeff(self.sadtalker_paths, self.device)

    def run(self):
        save_dir = os.path.join(self.result_dir, strftime("%Y_%m_%d_%H.%M.%S"))
        os.makedirs(save_dir, exist_ok=True)

        first_frame_dir = os.path.join(save_dir, 'first_frame_dir')
        os.makedirs(first_frame_dir, exist_ok=True)
        print('3DMM Extraction for source image')
        first_coeff_path, crop_pic_path, crop_info = self.preprocess_model.generate(self.source_image, first_frame_dir,
                                                                                    self.preprocess,
                                                                                    source_image_flag=True,
                                                                                    pic_size=self.size)
        if first_coeff_path is None:
            print("Can't get the coeffs of the input")
            return

        ref_eyeblink_coeff_path = self.extract_coefficients(self.ref_eyeblink, save_dir)
        ref_pose_coeff_path = self.extract_coefficients(self.ref_pose, save_dir, ref_eyeblink_coeff_path)

        batch = get_data(first_coeff_path, self.driven_audio, self.device, ref_eyeblink_coeff_path, still=self.still)
        coeff_path = self.audio_to_coeff.generate(batch, save_dir, self.pose_style, ref_pose_coeff_path)

        data = get_facerender_data(coeff_path, crop_pic_path, first_coeff_path, self.driven_audio, self.batch_size,
                                   self.input_yaw, self.input_pitch, self.input_roll,
                                   expression_scale=self.expression_scale,
                                   still_mode=self.still, preprocess=self.preprocess, size=self.size)

        result = self.animate_from_coeff.generate(data, save_dir, self.source_image, crop_info, enhancer=self.enhancer,
                                                  background_enhancer=self.background_enhancer,
                                                  preprocess=self.preprocess, img_size=self.size)

        shutil.move(result, save_dir + '.mp4')
        print('The generated video is named:', save_dir + '.mp4')

        generated_video = save_dir + '.mp4'
        return generated_video

    def extract_coefficients(self, reference_video, save_dir, existing_coeff_path=None):
        if reference_video is None:
            return None

        videoname = os.path.splitext(os.path.split(reference_video)[-1])[0]
        frame_dir = os.path.join(save_dir, videoname)
        os.makedirs(frame_dir, exist_ok=True)
        print('3DMM Extraction for video:', videoname)
        return self.preprocess_model.generate(reference_video, frame_dir, self.preprocess, source_image_flag=False)[
            0] if existing_coeff_path is None else existing_coeff_path


if __name__ == '__main__':
    sad_talker = SadTalker()
    sad_talker.run()
