# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 18:20:34 2024

@author: jag11
"""



'''
This code is used to generate all possible profiles for a visual conjoint experiment.
The code interacts with Google Slides to do this, creating each possible profile on a new slide

What you need at the start: 
    - A Google Slideshow with one slide that contains the profile template
    - Note: Mine has the template on the 4th slide and intro stuff on the first three slides

What this code does (overview): 
    - Iterates through all possible combinations of attribute levels
    - For each combination, it creates a profile by doing the following: 
        - Duplicating template slide of the Google Slideshow add appending it to the slideshow
        - Filling in each template attribute of the duplicated slide with the assigned attribute level
    - Downloads the slide as a png 
    - Creates a data frame containing the attributes of each profile
    - Writes and formats JavaScript code that can be pasted into Qualtrics

Where this fits in the full workflow (* indicates that this code is used to complete that step):
    1. Generate AI images from Canva AI image generator: https://www.canva.com/ai-image-generator/
    2. Download the desired images to a folder on your computer
    3. Process the images through the "Image_Resize_and_Blur_Works.py" file
    4. Manually upload the processed images to a folder in Google Drive
    5. Create a Google Slides presentation with the template conjoint profile
    6. Create a service account through the Google Cloud API
    7. Share the Google Slides presentation and the Google Drive folder with the service account
    8. Read through the presentation using Python and identify object elements *
    9. Get shareable links to the images *
    10. Define attributes and attribute levels *
    11. Generate all possible profiles in the Google Slides presentation *
    12. Convert the slides into processed profile images *
    13. Manually upload the processed profile images to the Qualtrics library
    14. Scrape the links to the Qualtrics library images and add to df *
    15. Create a data frame (df) containting the attributes of each profile *
    16. Write / format JavaScript (JS) code to display two random profiles *
    17. Paste formatted JS code into relevant question's JS editor in survey
    18. Create necessary embedded data fields in the survey flow editor
    19. Write HTML code in each conjoint task for proper display
    20. Field survey, download data, analyze data, write up results, publish



What this code does (cell-by-cell):
    
    

The first code cell imports libraries

The second code cell interacts with Google Slides using the Google Slides API. It retrieves critical information about the slideshow.
YOU MUST RUN THIS CODE CHUNK EVERY TIME THE SLIDESHOW IS MANUALLY UPDATED, BECAUSE THE OBJECT IDS WILL CHANGE EACH TIME.
However, if the code is working properly, you should never have to update the slideshow manually.
If you run into issues, check the project on Google Cloud and ask Chat-GPT

The third code cell interacts with Google Drive. Specifically, it finds all pictures in the picture folder and gets their links
It then creates downloadable links for these images so they can be inserted into the templates on Google Slides.

The fourth cell defines attributes for the conjoint. It is fairly self-explanatory.

The fifth cell is where the magic happens. 
The code iterates through all possible combinations of profile attribute levels.
For each combination, it duplicates the template slide and adds it to the slideshow.
For each slide that is added, the placeholder text and image are replaced.
Also, a data frame is created with one row for each new profile and columns containing profile information. 
The data frame is saved as created_profiles.csv. Further manipulation in R prepares the JavaScript code. 


The sixth cell converts the slides into png images and saves them to a folder

The seventh cell processes the pngs, creating final (processed) profile images

The eighth cell ("Cell 8.8") scrapes the profile images links from Qualtrics

The ninth cell combines the scraped links and the profile info into a single df

The tenth cell formats JavaScript (JS) code
The JS code randomly samples two profiles, displays them, & sets embedded data
You can paste the JS code output directly into the JS editor in Qualtrics


I think that's it! Good luck and have fun!
'''

# %%

# Cell 1

# Import libraries

import random
import json
import os
import glob


# %%



# %%

# Cell 2

###############################################################################
#Interact with Google Slides
#Using Google Slides API
###############################################################################
# RUN THIS EVERY TIME YOU RESET THE GOOGLE SLIDES PRESENTATION
# BECAUSE THE OBJECT IDS OF THE IMAGES WILL CHANGE IF YOU RESET IT

from google.oauth2 import service_account
print("google-auth is successfully installed!")

from google.oauth2 import service_account
from googleapiclient.discovery import build

# There are two different file paths that seem relevant
# One is the file path to the OAuth2.0 JSON credientials file
# The other is hte file path to the credential key to the service account
# The latter is the one we need
# Find it on your computer and insert it below

# Load credentials from file
credentials = service_account.Credentials.from_service_account_file("[YOUR_FILE_PATH_HERE.json]")

# Initialize the Google Slides API
slides_service = build('slides', 'v1', credentials=credentials)

# Replace with your presentation ID
# Presentation ID is the string of characters in the URL that is between the "/d/" and the "/edit".
# Remember that you need to share the presentation with the service account
presentation_id = '[YOUR_PRESENTATION_ID_HERE]'


###############################################################################
# Below, identify the object IDs of all template profile attributes
###############################################################################

# Get the first slide (or any specific slide)
slide_deck = slides_service.presentations().get(presentationId=presentation_id).execute()
slides = slide_deck.get('slides')


# Get Object IDs (Not important if you know the image ID already):
# Get the presentation details
presentation = slides_service.presentations().get(presentationId=presentation_id).execute()
slides = presentation.get('slides')

# Print the object IDs and their types
slide_counter = 1
for slide in slides:
    page_elements = slide.get('pageElements')
    print(f"Slide Number: {slide_counter}")
    slide_counter += 1
    for element in page_elements:
        if slide_counter < 14:
            print(f"Object ID: {element['objectId']}, Type: {element['shape']['shapeType'] if 'shape' in element else 'image'}")

# On Slide 4 (The Template Slide)
# Object ID: g3224f75cb5d_0_124, Type: image - This is the picture
# Object ID: g3224f75cb5d_0_12, Type: TEXT_BOX - This contains "[NAME]"
# Object ID: g3224f75cb5d_0_14, Type: TEXT_BOX - This contains "[NUMBER] years experience"
# Object ID: g3224f75cb5d_0_23, Type: TEXT_BOX - This contains "Daycare volunteer at [RELIGIOUS CENTER]"
# Object ID: g3224f75cb5d_0_13, Type: TEXT_BOX - This contains "$[COST] per hour"
    
#Slide IDs
slide_id_list = []
for i, slide in enumerate(slides):
    slide_id = slide['objectId']
    slide_id_list.append(slide_id)
    print(f"Slide {i + 1} ID: {slide_id}")
    
print(slide_id_list)



# %%





# %%

# Cell 3

# Interact wtih Google Drive
# Using Google Drive API
# Get the links to the picture options from a Google Drive folder
# The folder should contain all picture options, as pngs of the appropriate size and blur. 
# See "Image_Resize_and_Blur_Works.py" file for image processing. Then upload manually to a folder in Drive
# Make sure to share the folder with the service account


#Assume that the credentials file from Google Slides API also works here

# Load credentials
SCOPES = ['https://www.googleapis.com/auth/drive']

# Insert same file path from Cell 2
SERVICE_ACCOUNT_FILE = '[YOUR_FILE_PATH_HERE.json]'

creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('drive', 'v3', credentials=creds)

# Folder ID from Google Drive
folder_id = '[YOUR_FOLDER_ID_HERE]'

# Query to get all files in the folder
query = f"'{folder_id}' in parents and mimeType='image/png'"
results = service.files().list(q=query, fields="files(id, name)").execute()
items = results.get('files', [])

# Create a list which will contain the links to the picture options
image_links = []

if not items:
    print('No files found.')
else:
    print('Files:')
    for item in items:
        # Make the file shareable
        file_id = item['id']
        service.permissions().create(
            fileId=file_id,
            body={'role': 'reader', 'type': 'anyone'},
        ).execute()

        # Get shareable link
        link = f"https://drive.google.com/uc?export=download&id={file_id}"
        image_links.append(link)
        print(f"{item['name']}: {link}")
        
        
        #Note: These links are in the correct format for placing in Slides
        
# You'll get an error in this code chunk unless you share the folder with the service account (crawler) 

# %%







# %%

# Cell 4

# Define levels for each attribute: 
    
#Attribute List: 
    # Picture
    # Religion (indicated through Name + Religious Center)
    # Cost per hour
    # Years of Experience


#Picture:
    #Links to the images are contained in the image_links list, defined above
    
#Religion:
religions = ["Jewish", "Muslim", "Protestant", "Catholic", "Confucian"]

#Cost:
costs = [14, 15, 16]

#Number of Years of Experience:
years_of_experience = [3, 7, 11] 
#Ojo! If digits match digits elsewhere in the profile, this could create issues with text replacement

# %%






#%%

# Cell 5


'''
This is where the magic happens

Here, we do the following steps:
    - Duplicate the template slide and add the duplicate to the end of the slideshow
    - Edit the elements of the newly-created slide
    - Create a data frame with a row for each new profile and save it as a .csv file
'''

import time # Use for sleep function (avoid API rate limit)
import pandas as pd # Use to create data frame


# Setup (Redundant from above cells)

from google.oauth2 import service_account
from googleapiclient.discovery import build

# Load credentials from file
credentials = service_account.Credentials.from_service_account_file("[SAME_FILE_PATH_HERE.json]")

# Initialize the Google Slides API
slides_service = build('slides', 'v1', credentials=credentials)

# Replace with your presentation ID
presentation_id = '[SAME_PRESENTATION_ID]'

# Get the slide deck
slide_deck = slides_service.presentations().get(presentationId=presentation_id).execute()
slides = slide_deck.get('slides')




# Get the ID of Slide 4 (the template slide)
# Note: This is specific to my slideshow
# Change "3" to the number of your template slide if you are using a different slideshow
template_slide_number = 4
template_slide_id = slides[3]['objectId']  # Assuming slide 4 is at index 3 (0-indexed)


# Identify the object ID of the picture on each of the new slides
# Note that - in this particular slideshow - there are multiple images per slide
# In this particular slideshow, there is only one image that needs to be replaced per slide
# And in this particular slideshow, it is the first image on the slide
# So the following function should find the corresponding object ID on each slide
def get_image_object_id_from_slide(slide_id):
    # Get the slide content
    slide = slides_service.presentations().pages().get(
        presentationId=presentation_id, pageObjectId=slide_id).execute()
    
    image_object_ids = []
    
    # Loop through all page elements to find images
    for element in slide['pageElements']:
        if 'image' in element:
            image_object_ids.append(element['objectId'])
            
    # Extract the first one
    pic_object_id = image_object_ids[0]
    
    return pic_object_id


# Define a function to duplicate and edit the slide
# Inputs: 
    # Slide number (the number of the new slide)
    # Counter for each attribute (religion, yexp, cost, image)
    # The ID of the template slide (Slide #4 in this case)
def duplicate_and_edit_slide(slide_number, relig_counter, yexp_counter, 
                             cost_counter, img_counter, template_slide_id):
    # Create a request to duplicate the slide
    requests = [
        {
            'duplicateObject': {
                'objectId': template_slide_id
            }
        }
    ]
    
    # Execute the request to duplicate the slide
    response = slides_service.presentations().batchUpdate(
        presentationId=presentation_id, body={'requests': requests}).execute()
    
    # After duplicating, reorder the slides to ensure the new slide goes to the end
    # Get all slide IDs in the presentation
    slide_id_list = [slide['objectId'] for slide in slides]
    
    # Move the newly duplicated slide to the end
    new_slide_id = response['replies'][0]['duplicateObject']['objectId']
    slide_id_list.append(new_slide_id)  # Add the duplicated slide to the end of the list
    
    # Add the new slide's ID to the list of new slide IDs initialized outside of the function
    # Same with slide number
    new_slide_ids.append(new_slide_id)
    slide_number_actual.append(slide_number)
    
    # Assign attribute levels
    # Take the ith element of the attribute levels list for each attribute
    p_religion = religions[relig_counter]
    p_cost = costs[cost_counter]
    p_yoe = years_of_experience[yexp_counter]
    p_image = image_links[img_counter]
    
    #Specify 2 decimal places for cost
    p_cost_2d = "{:.2f}".format(p_cost)
    
    #Add values to lists (columns of data frame for JavaScript code)
    religion_column.append(p_religion)
    cost_column.append(p_cost_2d)
    yexp_column.append(p_yoe)
    image_column.append(p_image)
    
    # Assign name and religious center given the religion
    # Do this because religion is not explicitly listed in the profile
    # Instead, it is signaled through name and religious center
    if p_religion == "Jewish":
        name = "Golda"
        center = "Zohar Synagogue"

    elif p_religion == "Muslim":
        name = "Khadija"
        center = "Dar Al-Iman Mosque"
        
    elif p_religion == "Protestant":
        name = "Jane"
        center = "Christ Lutheran Church"
        
    elif p_religion == "Catholic":
         name = "Alejandra"
         center = "San Miguel Cathedral"
         
    elif p_religion == "Confucian":
        name = "Mei Ling"
        center = "Sheng Dao Temple"
        
    else:
        print("Error in choice of religion: No valid option selected")
        
        
        
    # Get object ID of the image that needs to be replaced
    # Call the get_image_object_id_from_slide function
    img_to_replace = get_image_object_id_from_slide(new_slide_id)
    

    # Now, you can edit the newly added slide (e.g., change text, images, etc.)
    edit_requests = [
        {
            'replaceAllText': {
                'containsText': {'text': '[NAME]'},
                'replaceText': f'{str(name)}',  # Example: changing [NAME]
                'pageObjectIds': [new_slide_id]  # Apply to the new slide
            }
        },
        {
            'replaceAllText': {
                'containsText': {'text': '[NUMBER]'},
                'replaceText': f'{str(p_yoe)}',  # Example: changing [NUMBER]
                'pageObjectIds': [new_slide_id]  # Apply to the new slide
            }
        },
        {
            'replaceAllText': {
                'containsText': {'text': '[RELIGIOUS CENTER]'},
                'replaceText': f'{str(center)}',  # Example: changing [RELIGIOUS CENTER]
                'pageObjectIds': [new_slide_id]  # Apply to the new slide
            }
        },
        {
            'replaceAllText': {
                'containsText': {'text': '[COST]'},
                'replaceText': f'{str(p_cost_2d)}',  # Example: changing [COST]
                'pageObjectIds': [new_slide_id]  # Apply to the new slide
            }
        },
        {
            'replaceImage': {
                'imageObjectId': img_to_replace,  # The object ID of the image to be replaced
                'url': p_image,  # Publicly accessible URL of the image
                
                #It's actually not the entire URL
                #Again, it's a segment of it, between "/d/" and "/view?"
                #You then need to create a direct download link using this segment
                
                #Walk-through:
                #Share URL: What you copy
                #Truncated URL: The stuff between "/d/" and "/view?"
                #Base of correct URL: https://drive.google.com/uc?export=download&id=
                #Correct URL: Append the truncated URL to the base of the correct URL
                
            # Only do this to the specified slide
            # We took care of this already by specifying the object ID
            # (Object ID is unique to slide)
            }
        }
    ]
    
    
    # Apply the edit requests to the newly created slide
    slides_service.presentations().batchUpdate(
        presentationId=presentation_id, body={'requests': edit_requests}).execute()

    print(f"Slide {slide_number} duplicated and edited successfully!")


# Initialize slide number
# For this slideshow, we start at 5
# More generally, it is template_slide_number + 1
slide_number = template_slide_number + 1

# Identify number of slides that already exist
slides_base = template_slide_number




# Figure out how long the whole process takes
# "The whole process" = create all possible profiles in slideshow and in data frame
# Start a timer
start_time = time.time()


# Initialize empty lists
# These will be filled in during the function calls
# And then used to construct a data frame that will be useful for the JavaScript code
# Initatize empty list to hold slide IDs for newly-created slides
new_slide_ids = []
slide_number_actual = []
# Initialize attribute lists
religion_column = []
cost_column = []
yexp_column = []
image_column = []

# Iterate through all possible attribute level combinations
# First 45 profiles should all be Jewish, next 45 Muslim, etc.
for i in range(0, len(religions)):
    # Within each religion, first 15 profiles should have 3 years of experience
    for j in range(0, len(years_of_experience)):
        # Within each yexp, first 5 profiles should have the same cost
        for k in range(0, len(costs)):
            # Within each cost level, change image each time
            for l in range(0, len(image_links)):
                # Call duplicate function
                duplicate_and_edit_slide(slide_number, i, j, k, l, template_slide_id)
                # Iterate slide number
                slide_number += 1
                # Sleep for two seconds to avoid hitting API limit
                time.sleep(2)

# Combine lists together as columns of a data frame (for JavaScript code)
# Create a dictionary from the lists
created_profiles = {
    "Slide_Number": slide_number_actual,
    "Slide_ID": new_slide_ids,
    "Religion": religion_column,
    "Cost": cost_column,
    "Years_Experience": yexp_column,
    "Image_Link": image_column
}

# Create a dataframe from the dictionary
created_profiles_df = pd.DataFrame(created_profiles)

# Save the data frame as a .csv file 
# (Do further manipulation in R to prepare JavaScript code)
created_profiles_df.to_csv('[YOUR_OUTPUT_DATA_FRAME_FILE_PATH.csv]', index=False) 
print("created_profile.csv downloaded to [YOUR_FOLDER_NAME] folder")

# End the timer
end_time = time.time()

# Calculate the amount of time it took to create all possible conjoint profiles
elapsed_time = end_time - start_time


#Count the number of slides created
num_slides_created = (slide_number - 1) - slides_base

print(f"Elapsed time: {elapsed_time} seconds to create {num_slides_created} profiles")



#%%




#%%

# Cell 6

'''
In this chunk, we convert each created slide into a png
Then we save all the pngs to a folder.  
'''


from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
import os
import io
from pdf2image import convert_from_path


# Step 1: Download presentation as pdf
output_pdf_path = "[YOUR_PDF_FILE_PATH.pdf]"

drive_service = build("drive", "v3", credentials=creds)

# Request to export the presentation as a PDF
request = drive_service.files().export_media(
    fileId=presentation_id,
    mimeType="application/pdf"
)

# Save the PDF locally
with io.FileIO(output_pdf_path, "wb") as file:
    downloader = MediaIoBaseDownload(file, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}% complete.")

print(f"Presentation downloaded as {output_pdf_path}")


# Step 2: Save each slide from the downloaded pdf as a png

# Output folder for PNGs
output_folder = "[YOUR_OUTPUT_FOLDER_FOR_PNGS]"
os.makedirs(output_folder, exist_ok=True)

# Convert the PDF to a list of images (one per page)
# DPI = 200 (300 = high quality, 150 = lower quality but still good)
# Lower DPI leads to faster processing
# But when DPI is too low, the border around the images looks weird
pages = convert_from_path(output_pdf_path, 300, first_page = 5)

# Save each page as a PNG
for i, page in enumerate(pages, start=1):
    image_path = os.path.join(output_folder, f"slide_{i:03d}.png")
    page.save(image_path, 'PNG')
    print(f"Saved slide {i} as {image_path}")
 





#%%






#%%

# Cell 7

'''
Process raw slides into profile images
This code is copied directly from "Babysitter Conjoint Slide Downloader.py"

Basically this code just removes white space and saves the profile as an image
'''

# Import libraries
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
    # Since blur is set to 0 here, the image doesn't blur
    # Blurring is an artifact from old use of this code
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
input_folder = "[YOUR_INPUT_FOLDER]"
output_folder = "[YOUR_OUTPUT_FOLDER]"

# Process all images in the folder
process_images(input_folder, output_folder)




#%%





#%%

# Cell 8

# THERE USED TO BE A FUNCTIONING CELL HERE
# IT MADE PUBLICLY ACCESSIBLE GOOGLE DRIVE LINKS TO PROFILE IMAGES
# HOWEVER, QUALTRICS HAS TROUBLE DISPLAYING IMAGES FROM GOOGLE DRIVE IN SURVEYS
# SO THE CODE IS NOT USEFUL

# INSTEAD, UPLOAD PROCESSED PROFILES IMAGES TO QUALTRICS LIBRARY MANUALLY
# THEN RUN CELL 8.8



# %%





#%%

# Cell 8.8

'''
Before running this code, manually upload the Processed Profile images to Qualtrics Library
This code scrapes the library to get their urls
I know - this is annoying and seems repetitive, but nothing else was working
'''

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# Assume 25 library items per page
n_item_per_page = 25

# Set number of Qualtrics library pages manually
# 225 / 25 = 9
n_qual_lib_pages = 9

# Base URL for Qualtrics library
url_base = "[YOUR_QUALTRICS_LIBRARY_BASE_URL]"

# Initialize WebDriver (Firefox here; adjust if you want Chrome)
driver = webdriver.Chrome()
driver.get(url_base + "1")

# Wait for manual login
print("Please log in manually.")
time.sleep(25)  # Adjust this wait time as needed

# ---- NEW: Click into the "IPC Profiles v4.0" subfolder ----
# This is the subfolder which houses all of the relevant images and nothing else. 
# Sub out "IPC Profiles v4.0" below for whatever your subfolder is called

try:
    folder_button = driver.find_element(By.CSS_SELECTOR, "div[aria-label*='IPC Profiles v4.0']")
    folder_button.click()
    print("Clicked into 'IPC Profiles v4.0' subfolder.")
    time.sleep(5)  # give time for the folder contents to load
except Exception as e:
    print("Could not find or click the IPC Profiles v4.0 folder:", e)

# Initialize an empty DataFrame to store links
all_links_df = pd.DataFrame(columns=["final_links"])

# Loop through all pages of Qualtrics library
for i in range(1, n_qual_lib_pages + 1):
    time.sleep(3)  # Wait for page to load
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, "html.parser")

    # Extract image links
    full_links = [img.get("src") for img in soup.find_all("img") if img.get("src")]
    full_links = [link for link in full_links if "/ControlPanel" in link]

    # Append base URL
    base_pic_url = "https://sscucla.qualtrics.com"
    final_links = [base_pic_url + link for link in full_links]

    # Debug: print links
    print(final_links)

    # Add to dataframe
    all_links_df = pd.concat([all_links_df, pd.DataFrame({"final_links": final_links})], ignore_index=True)

    # Try clicking "Next Page"
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Next Page']")
        next_button.click()
    except Exception as e:
        print("Next button not found or cannot be clicked. Ending loop.")
        break

# Shorten the links by removing everything after "&last"
short_links_df = all_links_df.copy()
short_links_df["short_links"] = short_links_df["final_links"].str.replace(r"&last.*", "", regex=True)

# Add a profile number so this can be merged with created_profiles_df
# Reverse the order because it got flipped during the profile generation process
n = len(short_links_df)
short_links_df["profile_number"] = range(n, 0, -1)


# Count unique rows
num_unique_rows_short = short_links_df["short_links"].nunique()
print(num_unique_rows_short)

# Save the links to CSV
# short_links_df.to_csv("[YOUR_FILE_PATH.csv]", index=False)


# Check and stop existing Selenium sessions
try:
    driver.quit()
except Exception as e:
    print("No active session to close.")



#%%





#%%

# Cell 9

'''
Add the URLs to the data frame 'created_profiles_df'
Then add columns containing repetitive JavaScript code
Then save the completed data frame as a .csv file. 
'''

import pandas as pd

# Run this line if data frame is already saved on computer (if skipping Cell 5)
created_profiles_df = pd.read_csv('[YOUR_CREATED_PROFILES_DATA_FRAME.csv]')



# Create new variable to match the slide id. 
created_profiles_df['profile_number'] = created_profiles_df['Slide_Number'] - 4


# Merge short_links_df into created_profiles_df on profile_number
created_profiles_df = created_profiles_df.merge(
    short_links_df[["profile_number", "short_links"]],
    on="profile_number",
    how="left"
)

# Rename the new column
created_profiles_df = created_profiles_df.rename(columns={"short_links": "visual_profile_url"})





# Create new (simpler) variable for babysitter image
simple_image_mapping = {
    "[YOUR_GOOGLE_DRIVE_LINK_TO_IMAGE_1]": 1,
    "[YOUR_GOOGLE_DRIVE_LINK_TO_IMAGE_2]": 2,
    "[YOUR_GOOGLE_DRIVE_LINK_TO_IMAGE_3]": 3,
    "[YOUR_GOOGLE_DRIVE_LINK_TO_IMAGE_4]": 4,
    "[YOUR_GOOGLE_DRIVE_LINK_TO_IMAGE_5]": 5
}

created_profiles_df['Image_ID'] = created_profiles_df['Image_Link'].map(simple_image_mapping)




# Add repetitive lines in JavaScript
# There are three repetitive sections of code. 
# Add column of identifiers for each profile (with and without comma)

# Repetitive Section #3
created_profiles_df["prof_identifier"] = (
    "'" 
    + created_profiles_df["Religion"].astype(str) + "_" 
    + created_profiles_df["Cost"].astype(str) + "_" 
    + created_profiles_df["Years_Experience"].astype(str) + "_" 
    + "pic" + created_profiles_df["Image_ID"].astype(str) 
    + "'"
)

created_profiles_df["prof_identifier_comma"] = created_profiles_df["prof_identifier"] + ","

created_profiles_df["map_i_a"] = (
    created_profiles_df["prof_identifier"] + ": ['" 
    + created_profiles_df["Religion"].astype(str) + "', '" 
    + created_profiles_df["Cost"].astype(str) + "', '" 
    + created_profiles_df["Years_Experience"].astype(str) + "', 'pic" 
    + created_profiles_df["Image_ID"].astype(str) + "']"
)

created_profiles_df["map_i_a_comma"] = created_profiles_df["map_i_a"] + ","


# Repetitive Section #2
created_profiles_df["map_links_i"] = (
    "'" + created_profiles_df["visual_profile_url"].astype(str) + "': " 
    + created_profiles_df["prof_identifier"]
)

created_profiles_df["map_links_i_comma"] = created_profiles_df["map_links_i"] + ","


# Repetitive Section #1
created_profiles_df["qual_link_quote_comma"] = (
    "'" + created_profiles_df["visual_profile_url"].astype(str) + "',"
)



# Save completed df to .csv. 
# Uncomment to save. 
created_profiles_df.to_csv("[YOUR_FILE_PATH_TO_COMPLETED_DATA_FRAME.csv]", index=False)


#%%






#%% 

# Cell 10

import pyperclip

'''
Fill in the JavaScript shell with formatted code

Overview: This JavaScript code is used to randomly sample profiles from the Qualtrics library and display two of them at a time to the respondent. 
It also makes note of the attributes of the profiles that are shown and saves these attributes as embedded data. 
The embedded data appears in the resulting data frame of responses, providing all data necessary for the researcher to analyze the data as a conjoint. 
(NOTE: YOU MUST CREATE THE CORRESPONDING EMBEDDED DATA FIELDS BY HAND IN QUALTRICS). 

The code consists of a provided shell and three "repetitive sections". 
The repetitive sections are created below and inserted into the shell. 
The first is the list of links to the profile images in the Qualtrics library. 
The second creates an identifier for each image. 
The third specifies the attributes that are included in each profile image. 

The following code writes and formats JS code for conjoint tasks in Qualtrics, and copies it to the clipboard. 

You can then just paste the output into the JS editor in your Qualtrics survey. 

To display the profiles to users, you must also write (by hand) a few lines of HTML code in the each conjoint question's HTML editor. 
'''

# Step 1: Store JS shell exactly as-is (triple quotes preserve formatting)
java_shell = """Qualtrics.SurveyEngine.addOnload(function() {
    // Insert CSS for image sizing and responsive layout
    var style_[task_num] = document.createElement('style');
    style_[task_num].innerHTML = `
        .image-wrapper {
            display: flex;
            justify-content: center; /* Center images on desktop */
            align-items: center;    /* Center images vertically on desktop */
            gap: 20px;              /* Space between images */
            flex-wrap: wrap;        /* Allow wrapping for smaller screens */
        }
        .image-container {
            text-align: center; /* Center the text and image */
            margin: 20px auto;  /* Add spacing between containers */
        }
        .randomized-image {
            max-width: 500px;   /* Set a consistent width */
            max-height: 500px;  /* Set a consistent height */
            width: 100%;        /* Ensure the image scales properly */
            height: auto;       /* Maintain aspect ratio */
        }
        .image-label {
            font-size: 18px;     /* Label font size */
            font-weight: bold;   /* Bold label */
            margin-top: 10px;    /* Space between image and label */
        }
        /* Responsive design for small screens */
        @media (max-width: 768px) {
            .image-wrapper {
                flex-direction: column; /* Stack images vertically */
            }
        }
    `;
    document.head.appendChild(style_[task_num]);

    // Array of image URLs from your Qualtrics library
    var images_[task_num] = [
        [qual_link_quote_comma]
    ];
	
	
	// Mapping of image URLs to identifiers
    var imageIdentifiers_[task_num] = {
        [map_links_i_comma]
    };
	


    // Shuffle the array to randomize order
    for (let i = images_[task_num].length - 1; i > 0; i--) {
        let j = Math.floor(Math.random() * (i + 1));
        [images_[task_num][i], images_[task_num][j]] = [images_[task_num][j], images_[task_num][i]];
    }

    // Select the first two images from the shuffled array
    var selectedImage1_[task_num] = images_[task_num][0];
    var selectedImage2_[task_num] = images_[task_num][1];
	
	
	// Get identifier for the selected images
    var profileIdentifier1_[task_num] = imageIdentifiers_[task_num][selectedImage1_[task_num]];
	var profileIdentifier2_[task_num] = imageIdentifiers_[task_num][selectedImage2_[task_num]];
	

    // Create <img> HTML elements for the selected images with labels
    var imageHTML1_[task_num] = '<div class="image-container"><img src="' + selectedImage1_[task_num] + '" alt="Babysitter A" class="randomized-image"/><div class="image-label">Babysitter A</div></div>';
    var imageHTML2_[task_num] = '<div class="image-container"><img src="' + selectedImage2_[task_num] + '" alt="Babysitter B" class="randomized-image"/><div class="image-label">Babysitter B</div></div>';

    // Insert the <img> elements into a wrapper div
    var wrapperHTML_[task_num] = '<div class="image-wrapper">' + imageHTML1_[task_num] + imageHTML2_[task_num] + '</div>';
    document.getElementById("imageContainer1_[task_num]").innerHTML = wrapperHTML_[task_num];
	
	
	
	
	// Set additional embedded data based on the profile identifier
	// First create a variable that maps the profile identifier to the profile attributes
	var attributes_[task_num] = {
		[map_i_a_comma]
	};

    // Set Embedded Data for tracking the displayed images and attributes
    Qualtrics.SurveyEngine.setEmbeddedData("SelectedImage1_[task_num]", selectedImage1_[task_num]);
    Qualtrics.SurveyEngine.setEmbeddedData("SelectedImage2_[task_num]", selectedImage2_[task_num]);
	Qualtrics.SurveyEngine.setEmbeddedData("Link_[task_num]_A", selectedImage1_[task_num]);
    Qualtrics.SurveyEngine.setEmbeddedData("Link_[task_num]_B", selectedImage2_[task_num]);
	Qualtrics.SurveyEngine.setEmbeddedData("Type_[task_num]_A", attributes_[task_num][profileIdentifier1_[task_num]][0]);
	Qualtrics.SurveyEngine.setEmbeddedData("Type_[task_num]_B", attributes_[task_num][profileIdentifier2_[task_num]][0]);
	Qualtrics.SurveyEngine.setEmbeddedData("Cost_[task_num]_A", attributes_[task_num][profileIdentifier1_[task_num]][1]);
	Qualtrics.SurveyEngine.setEmbeddedData("Cost_[task_num]_B", attributes_[task_num][profileIdentifier2_[task_num]][1]);
	Qualtrics.SurveyEngine.setEmbeddedData("Yexp_[task_num]_A", attributes_[task_num][profileIdentifier1_[task_num]][2]);
	Qualtrics.SurveyEngine.setEmbeddedData("Yexp_[task_num]_B", attributes_[task_num][profileIdentifier2_[task_num]][2]);
	Qualtrics.SurveyEngine.setEmbeddedData("Pic_[task_num]_A", attributes_[task_num][profileIdentifier1_[task_num]][3]);
	Qualtrics.SurveyEngine.setEmbeddedData("Pic_[task_num]_B", attributes_[task_num][profileIdentifier2_[task_num]][3]);

	
});"""

# Step 2: helper to format column values into JS lines
def format_js_block(series):
    """Convert a pandas Series into a block of lines for insertion in JS."""
    lines = series.astype(str).tolist()
    # Remove the trailing comma from the last entry
    if lines:
        lines[-1] = lines[-1].rstrip(",")
    return "\n        ".join(lines)

# Step 3: create the replacements
qual_links_block = format_js_block(created_profiles_df["qual_link_quote_comma"])
map_links_block = format_js_block(created_profiles_df["map_links_i_comma"])
map_ia_block    = format_js_block(created_profiles_df["map_i_a_comma"])




# Step 4: generate all task scripts
number_of_tasks = 5 # Number of conjoint task questions in Qualtrics survey. 
java_filled = []  # will hold all JS blocks

for task in range(1, number_of_tasks + 1):
    script = (java_shell
        .replace("[qual_link_quote_comma]", qual_links_block)
        .replace("[map_links_i_comma]", map_links_block)
        .replace("[map_i_a_comma]", map_ia_block)
        .replace("[task_num]", str(task))
    )
    java_filled.append(script)

# Step 5: Copy one of the scripts to clipboard (then paste in Qualtrics)
pyperclip.copy(java_filled[4])
print("✅ First JavaScript block copied to clipboard!")




#%%





