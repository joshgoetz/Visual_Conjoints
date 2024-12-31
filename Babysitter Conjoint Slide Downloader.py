# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 20:13:12 2024

@author: jag11
"""

'''
Does the same thing as the "Image_Resize_and_Blur_Works.py" file
Except the output size is different and there is no blur
The code should remove the white space, leaving just the profile image

Then, upload each one to Qualtrics
Still figuring out how to automate this part
'''

# Import libraries
import os
import glob
import numpy as np
from PIL import Image, ImageFilter, ImageOps

def remove_whitespace(image, tolerance=30):
    # Convert image to RGB mode if not already
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Convert image to numpy array
    image_array = np.array(image)
    
    # Define a threshold for near-white pixels
    white_color = np.array([255, 255, 255])
    tolerance = np.array([tolerance, tolerance, tolerance])
    
    # Create a mask for pixels within the tolerance range of white
    mask = np.all(np.abs(image_array - white_color) <= tolerance, axis=-1)
    
    # Find non-white pixels using the mask
    non_white_pixels = np.where(~mask)
    
    if len(non_white_pixels) != 2 or len(non_white_pixels[0]) == 0:
        raise ValueError("No non-white pixels found in the image.")
    
    # Get bounding box coordinates
    top, left = np.min(non_white_pixels, axis=1)
    bottom, right = np.max(non_white_pixels, axis=1)
    
    # Crop the image to the bounding box
    cropped_image = image.crop((left, top, right, bottom))
    return cropped_image

def resize_and_blur(image, output_size=(610, 985), blur_radius=0): 
    # Remove white space
    image = remove_whitespace(image)
    
    # Resize the image
    resized_image = ImageOps.fit(image, output_size, Image.Resampling.LANCZOS)
    
    # Blur the image
    blurred_image = resized_image.filter(ImageFilter.GaussianBlur(blur_radius))
    
    return blurred_image

def process_images(input_folder, output_folder):
    # Create output folder if it does not exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Get list of all image files in the input folder and sort by modification time
    image_files = sorted(
        glob.glob(os.path.join(input_folder, '*.*')),
        key=os.path.getmtime
    )
    
    # Process each file and rename them in the output folder
    for i, image_file in enumerate(image_files, start=1):
        try:
            # Open image
            image = Image.open(image_file)
            
            # Process image
            output_image = resize_and_blur(image)
            
            # Define new file name and output path
            new_file_name = f"babysitter_profile_{i:03d}.png"  # :03d ensures 3 digits with leading zeros
            output_path = os.path.join(output_folder, new_file_name)
            
            # Save the output image
            output_image.save(output_path)
            
            print(f"Processed image saved to {output_path}")
        
        except Exception as e:
            print(f"Error processing {image_file}: {e}")

# Define input and output folders
input_folder = "C:/Users/OSU/UCLA/UCLA Quarter VII/Conjoint Profiles v3 raw slides"
output_folder = "C:/Users/OSU/UCLA/UCLA Quarter VII/Conjoint Profiles v3 Processed"

# Process all images in the folder
process_images(input_folder, output_folder)

