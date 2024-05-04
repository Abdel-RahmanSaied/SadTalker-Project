from PIL import Image

def resize_image(image_path, desired_width=800):
    # Load the image
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
