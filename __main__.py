from sadTalker import SadTalkerApp


# Usage
app = SadTalkerApp()
# img_path = app.display_animation_interface()  # User chooses image via command line input
img_path = '/Users/saied/WorkDir/Projects/SadTalkerProject/SadTalker/examples/source_image/art_0.png'

print("Image path:", img_path)

# audio_path = input("Enter the path to the audio file: ")  # User provides the path to the audio file
audio_path = r"SadTalker/examples/driven_audio/bus_chinese.wav"  # User provides the path to the audio file
result_dir = app.run_inference(audio_path=audio_path, img_path=img_path)
app.display_animation(result_dir)
