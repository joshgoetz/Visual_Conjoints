# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 16:37:57 2024

@author: jag11
"""


'''
This code takes images (.png) from a folder and does the following:
    - Resizes the image
    - Removes the white space in the background of the image
    - Blurs the image
    - Saves all modified images to a different folder

'''

#Import libraries
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
    #Why include tolerance?
    #Use because the white background may not be totally white
    #If it's an off-white color we still want to be able to detect it
    
    # Create a mask for pixels within the tolerance range of white
    mask = np.all(np.abs(image_array - white_color) <= tolerance, axis=-1)
    
    # Find non-white pixels using the mask
    non_white_pixels = np.where(~mask)
    
    # Check if non_white_pixels contains the expected number of arrays
    if len(non_white_pixels) != 2:
        raise ValueError("Unexpected non_white_pixels structure.")
    
    # Check if there are any non-white pixels
    if len(non_white_pixels[0]) == 0:
        raise ValueError("No non-white pixels found in the image.")
    
    # Get bounding box coordinates
    top, left = np.min(non_white_pixels, axis=1)
    bottom, right = np.max(non_white_pixels, axis=1)
    
    # Crop the image to the bounding box
    cropped_image = image.crop((left, top, right, bottom))
    return cropped_image

def resize_and_blur(image, output_size=(288, 168), blur_radius=0): #Blur radius = 0 means no blur
    # Remove white space
    image = remove_whitespace(image)
    
    # Resize the image
    #This should crop the image if necessary to fit the specified aspect ratio
    resized_image = ImageOps.fit(image, output_size, Image.Resampling.LANCZOS)
    
    # Blur the image
    blurred_image = resized_image.filter(ImageFilter.GaussianBlur(blur_radius))
    
    return blurred_image

def process_images(input_folder, output_folder):
    # Create output folder if it does not exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Get list of all image files in the input folder
    image_files = glob.glob(os.path.join(input_folder, '*.*'))
    
    for image_file in image_files:
        try:
            # Open image
            image = Image.open(image_file)
            
            # Process image
            output_image = resize_and_blur(image)
            
            # Define output file path
            base_name = os.path.basename(image_file)
            output_path = os.path.join(output_folder, base_name)
            
            # Save the output image
            output_image.save(output_path)
            
            print(f"Processed image saved to {output_path}")
        
        except Exception as e:
            print(f"Error processing {image_file}: {e}")

# Define input and output folders
input_folder = "[YOUR_INPUT_FOLDER_HERE]"
output_folder = "[YOUR_OUTPUT_FOLDER_HERE]"

# Process all images in the folder
process_images(input_folder, output_folder)
