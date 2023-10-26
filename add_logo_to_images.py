import os
import sys
import cv2
import shutil
from PIL import Image

def add_logo_to_image(image_path, logo_path):
    # Open the image and the logo
    image = Image.open(image_path)
    logo = Image.open(logo_path)
    
    # Calculate the aspect ratio of the logo
    aspect_ratio = logo.height / logo.width
    
    # Determine the new width of the logo (e.g., 15% of image's width)
    new_logo_width = int(image.width * 0.15)
    new_logo_height = int(new_logo_width * aspect_ratio)
    
    # Ensure the logo dimensions are proportional to the original
    logo = logo.resize((new_logo_width, new_logo_height))
    
    # Get position to place logo at the bottom right of the image
    position = (image.width - logo.width, image.height - logo.height)
    
    # Add logo to the image
    image.paste(logo, position, logo)  # using logo as alpha/mask for transparency
    image.save(image_path)  # Save the modified image

def create_video(captures_directory, output_path):
    # Get all the image files from the captures directory
    files = [os.path.join(captures_directory, f) for f in os.listdir(captures_directory) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    # Check if there are any image files
    if not files:
        print("No images found in the specified directory!")
        return

    # Find out the frame width and height from the first image
    frame = cv2.imread(files[0])
    h, w, layers = frame.shape
    size = (w, h)
    
    # Define the codec using VideoWriter_fourcc and create a VideoWriter object
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), 19, size)
    
    # Read each file and write it to the video
    for file in files:
        img = cv2.imread(file)
        out.write(img)
    
    out.release()

def main():
    # Get current directory from the argument passed from the .bat file
    current_directory = sys.argv[1].replace("\\", "/").replace("\"","")
    file_name = sys.argv[2]
    captures_folder = sys.argv[3]
    captures_directory = os.path.join(current_directory, captures_folder)
    # Path to the logo
    logo_path = "G:/Meine Ablage/3D Modelling/#s9hU_All_logos/bandicam_logo.png"
    
    for root, dirs, files in os.walk(captures_directory):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(root, file)
                add_logo_to_image(image_path, logo_path)

    video_output_path = os.path.join(current_directory, file_name + ".mp4")
    create_video(captures_directory, video_output_path)

    # Remove the "Captures" folder after processing
    if os.path.exists(captures_directory):
        shutil.rmtree(captures_directory)

if __name__ == "__main__":
    main()