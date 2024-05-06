from SadTalker.sadTalker import SadTalkerApp


# Usage
app = SadTalkerApp()
# img_path = app.display_animation_interface()  # User chooses image via command line input
img_path = 'SadTalkerProject/417A5876.jpg'

print("Image path:", img_path)

# audio_path = input("Enter the path to the audio file: ")  # User provides the path to the audio file
audio_path = r"SadTalker/examples/driven_audio/bus_chinese.wav"  # User provides the path to the audio file

app.setParams(audio_path, img_path)

generated_video = app.run_inference()

print("Generated video:", generated_video)