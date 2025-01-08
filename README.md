# Visual_Conjoints
This repository contains the code needed to generate all possible profiles for a visual conjoint experiment and integrate the created profiles with Qualtrics.

It aims to provide all code needed for all steps of the process, from generating the images used in the profiles to analyzing data from the Qualtrics survey. That said, there are still some steps that must be done manually.

Please note that I am not the first social scientist to create a method for generating visual conjoint profiles. A method developed by Alessandro Vecchiato exists and is available on GitHub at the following link: https://github.com/avecchiato/Introducing_Visual_Conjoints (Citation: Alessandro Vecchiato (2021), "Replication Material of Introducing Visual Conjoint Experiments."). I developed my method independently of Vecchiato, and our methods are different. If you find my method confusing or hard to follow, I recommend checking out Vecchiato's method as an alternative. 

My method is built for survey experiments in social science but could be used for other purposes. 
The code provided was originally used to generate all possible profiles for a project that seeks to measure religious discrimination against babysitters and uses a forced-choice conjoint, but it could be adapted for any visual conjoint. In my case, the profiles are made to look like babysitter profiles on a fictitious app where parents choose babysitters to hire. The profiles contain a blurred picture of a babysitter, as well as information about the babysitter such as cost to hire, years of experience, religion, etc. 

Summary of my method:  <br/>
The goal of this method is to randomly show two profiles in Qualtrics to a respondent and be able to know which profile the respondent picked as well as the attributes that were included in each profile shown to each respondent. With this information, one can find the AMCEs of different attributes and do all sorts of analyses. The goal can be accomplished in Qualtrics if images of all possible profiles (all possible attribute level combinations) are included in the Qualtrics library, and JavaScript code is written in the Qualtrics survey to randomly sample from the library and set the chosen profile's attributes as embedded data. To do this, one must first create all possible profiles for the conjoint. To do this, a profile template must first be created, and then the template can be filled in with all possible attribute level combintations. This can be done by creating the template in a Google Slides presentation and then using the Google Slides API to repeatedly duplicate and edit the template slide to create all possible profiles. The provided Python script "Conjoint v3 all profiles.py" does the duplicating and editing, while other scripts in this repository (e.g. "Image_Resize_and_Blur_Works.py") automate other small tasks. 

Succinct List of Steps: <br/>
    1. Create the template profile in Google Slides (do this manually)
    2. Define attributes and attribute levels (modify the "Conjoint v3 all profiles.py" file for your purposes)
    3. Generate all possible profiles in Google Slides (by running the "Conjoint v3 all profiles.py" file)
    4. Download the profiles as pngs (this is done automatically when you run the "Conjoint v3 all profiles.py" file)
    5. Upload all profile pngs to Qualtrics library (This must be done manually, and it takes roughly 5 minutes for every 200-300 pngs)
    6. Write JavaScript code in Qualtrics that randomly samples images of profiles from the library and sets embedded data based on the chosen profile's attributes (use the "JavaScript Qualtrics" file and the "Scraping Qualtrics.qmd" file to simplify and automate the majority of this process)
    7. Once the survey is fielded and data is collected, download the data and analyze it. 


The full list of steps, in detail, is below. In parentheses, I indicate which script is used to accomplish the step, or denote that the step must be done "by hand" / manually (without code). Steps 1, 2, 3, 4, and 9 are optional and only necessary if the profiles include images (for example, my profiles contained a blurred headshot of a babysitter).  <br/>
    1. Obtain images (For example, I generated AI images from Canva AI image generator: https://www.canva.com/ai-image-generator/) (Do this by hand) <br/>
    2. Download the desired images to a folder on your computer (Do this by hand) <br/>
    3. Process the images (For example, I needed to remove white space, resize, and blur images) ("Image_Resize_and_Blur_Works.py") <br/>
    4. Manually upload the processed images to a folder in Google Drive (Do this by hand) <br/>
    5. Create a Google Slides presentation with the template conjoint profile (Do this by hand) <br/>
    6. Create a service account through the Google Cloud API (Do this by hand) <br/>
    7. Share the Google Slides presentation and the Google Drive folder with the service account (Do this by hand) <br/>
    8. Read through the presentation using Python and identify object elements ("Conjoint v3 all profiles.py")  <br/>
    9. Get shareable links to the images from the Google Drive folder ("Conjoint v3 all profiles.py")  <br/>
    10. Define attributes and attribute levels ("Conjoint v3 all profiles.py")  <br/>
    11. Generate all possible profiles in the Google Slides presentation ("Conjoint v3 all profiles.py")  <br/>
    12. Convert the slides into pngs ("Conjoint v3 all profiles.py")  <br/>
    13. Process the profile pngs (For example, I needed to remove white space) ("Babysitter Conjoint Slide Downloader.py") <br/>
    14. Manually upload the processed profile pngs to Qualtrics library (Do this by hand) <br/>
    15. Run a scraper in R to get all of the links to the profile pngs in the Qualtrics Library ("Scraping Qualtrics.qmd") <br/>
    16. Format JavaScript code in R using the created_profiles.csv file and the profile png links ("Scraping Qualtrics.qmd") <br/>
    17. Write JavaScript code that randomizes which profiles are shown in Qualtrics (Copy the output from the "Scraping Qualtrics.qmd" file into the provided "JavaScript Qualtrics" code) <br/>
    18. Modify JavaScript code as desired (e.g. you may want to force a difference on a relevant attribute) (Do this by hand) <br/>
    19. Ensure that embedded data is set and viewable in Qualtrics output data (Do this by hand) <br/>
    20. Download the output of the Qualtrics survey (Do this by hand) <br/>
    21. Manipulate the data to get it in the correct format for each analysis, and analyze the data (in R, Python, or whatever language you are most comfortable with!) <br/>


I'd like to thank the following people for their advice which was helpful in the process of creating this method: Salma Mousa, Chris Tausanovitch, and Jeff Lewis. I'd also like to thank Clayton Becker, who provided a template which the "JavaScript Qualtrics" file is based on. 
