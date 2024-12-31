# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 18:20:34 2024

@author: jag11
"""



'''
This code is used to generate all possible profiles for a conjiont experiment with a visual treatment
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
    12. Convert the slides into pngs *
    13. Process the profile pngs through the "Babysitter Conjoint Slide Downloader.py" file
    14. Manually upload the processed profile pngs to Qualtrics library
    15. Run the scraper in R to get all of the links to the profile pngs in the Qualtrics Library
    16. Format JavaScript code in R using the created_profiles.csv file and the profile png links
    17. Write the JavaScript code which randomized which profiles are shown in Qualtrics
    18. Ensure forced difference on religion, if desired
    19. Ensure that embedded data is set and viewable in Qualtrics output data
    20. Download the output of the Qualtrics survey into R
    21. Manipulate the data to get it in the correct format for each analysis
    22. Analyze data in R. 



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
Currently, it adds the updated slide right after the template slide each time.
So the slides end up appearing in inverse order (the slide that is added first ends up being last).
For each slide that is added, the placeholder text and image are replaced.
Also, a data frame is created with one row for each new profile and columns containing profile information. 
The data frame is saved as created_profiles.csv. Further manipulation in R prepares the JavaScript code. 


The sixth cell converts the slides into png images and saves them to a folder
You do have to manually download the full slideshow as a pdf before running this cell 


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

#Interact with Google Slides
#Using Google Slides API
# RUN THIS EVERY TIME YOU RESET THE GOOGLE SLIDES PRESENTATION
# BECAUSE THE OBJECT IDS OF THE IMAGES WILL CHANGE IF YOU RESET IT


#File path to OAuth2.0 JSON credientials file:
#"C:\Users\OSU\UCLA\Summer 2024\client_secret_405781185705-ecrfr93aaeq9d0d3rfr33a4bbut609o9.apps.googleusercontent.com.json"

#However, that's actually not the one we need
#We need the credential key to the service account
#which is this: "C:\Users\OSU\UCLA\Summer 2024\field-paper-conjoint-74d810572666.json"


from google.oauth2 import service_account
print("google-auth is successfully installed!")



from google.oauth2 import service_account
from googleapiclient.discovery import build

# Load credentials from file
credentials = service_account.Credentials.from_service_account_file("C:/Users/OSU/UCLA/Summer 2024/field-paper-conjoint-74d810572666.json")

# Initialize the Google Slides API
slides_service = build('slides', 'v1', credentials=credentials)

# Replace with your presentation ID
# Presentation ID is the string of characters in the URL that is between the "/d/" and the "/edit".
# Here, it is 1dkRagKYQ1eUaPvR5gpkDFbpcDvIeoGCsObAz6HgXDfM
# Remember that you need to share the presentation with the service account
presentation_id = '1dkRagKYQ1eUaPvR5gpkDFbpcDvIeoGCsObAz6HgXDfM'

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
SERVICE_ACCOUNT_FILE = 'C:/Users/OSU/UCLA/Summer 2024/field-paper-conjoint-74d810572666.json'

creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('drive', 'v3', credentials=creds)

# Folder ID from Google Drive
folder_id = '12jCo4BZCYjhv82GO9QyOXEziZAlmeriz'

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
costs = [19.25, 19.50, 19.75]

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
credentials = service_account.Credentials.from_service_account_file("C:/Users/OSU/UCLA/Summer 2024/field-paper-conjoint-74d810572666.json")

# Initialize the Google Slides API
slides_service = build('slides', 'v1', credentials=credentials)

# Replace with your presentation ID
presentation_id = '1dkRagKYQ1eUaPvR5gpkDFbpcDvIeoGCsObAz6HgXDfM'

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
                #Which means you need to append it to the end of some nonsense. 
                #Correct format should be https://drive.google.com/uc?export=download&id=11uLX6adYJKtDHQHG5ZBKeWy6M1ymnXN_
                
                #Example:
                #Share URL (what you copy): https://drive.google.com/file/d/1KyHNXMtcGXt7eN0oYkpq4KJoIIGQpjDM/view?usp=drive_link
                #Truncated URL: 1KyHNXMtcGXt7eN0oYkpq4KJoIIGQpjDM
                #Base of correct URL: https://drive.google.com/uc?export=download&id=
                #Correct URL: https://drive.google.com/uc?export=download&id=1KyHNXMtcGXt7eN0oYkpq4KJoIIGQpjDM
                
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

# Call the function to duplicate and edit slides (from Slide 5 to Slide 11)
#for i in range(5, 11):  # Duplicating and editing slides from Slide 5 to Slide 11 (inclusive)
#    duplicate_and_edit_slide(i, template_slide_id)


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
        # Within each yexp, first 5 profiles should have picture 1
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
created_profiles_df.to_csv('C:/Users/OSU/UCLA/UCLA Quarter VII/created_profiles.csv', index=False) 
print("created_profile.csv downloaded to UCLA Quarter VII folder")

# End the timer
end_time = time.time()

# Calculate the amount of time it took to create all possible conjoint profiles
elapsed_time = end_time - start_time


#Count the number of slides created
num_slides_created = (slide_number - 1) - slides_base

print(f"Elapsed time: {elapsed_time} seconds to create {num_slides_created} profiles")



#%%




#%%

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

output_pdf_path = "C:/Users/OSU/UCLA/UCLA Quarter VII/Conjoint Auto Python v3.pdf"

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
output_folder = "C:/Users/OSU/UCLA/UCLA Quarter VII/Conjoint Profiles v3 raw slides"
os.makedirs(output_folder, exist_ok=True)

# Convert the PDF to a list of images (one per page)
# DPI = 200 (300 = high quality, 150 = lower quality but still good)
# Lower DPI leads to faster processing
# But when DPI is too low, the border around the images looks weird
pages = convert_from_path(output_pdf_path, 300, first_page = 5)

# Save each page as a PNG
for i, page in enumerate(pages, start=1):
    image_path = os.path.join(output_folder, f"slide_{i}.png")
    page.save(image_path, 'PNG')
    print(f"Saved slide {i} as {image_path}")
 





#%%










#%%