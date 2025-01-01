# Visual_Conjoints
This repository contains all of the code needed to generate all possible profiles for a visual conjoint experiment and integrate the created profiles with Qualtrics.

It aims to provide all code needed for all steps of the process, from generating the images used in the profiles to analyzing data from the Qualtrics survey. 

Please note that I am not the first social scientist to create a method for generating visual conjoint profiles. A method developed by Alessandro Vecchiato exists and is available on GitHub at the following link: https://github.com/avecchiato/Introducing_Visual_Conjoints (Citation: Alessandro Vecchiato (2021), "Replication Material of Introducing Visual Conjoint Experiments."). I developed my method independently of Vecchiato, and our methods are different. If you find my method confusing or hard to follow, I recommend checking out Vecchiato's method as an alternative. 

My method is built for survey experiments in social science but could be used for other purposes. 
The code provided is used to generate all possible profiles for a specific project that seeks to measure religious discrimination against babysitters and uses a forced-choice conjoint, but it could be adapted for any visual conjoint. In my case, the profiles are made to look like babysitter profiles on a fictitious app where parents choose babysitters to hire. The profiles contain a blurred picture of a babysitter, as well as information about the babysitter such as cost to hire, years of experience, etc. 

Summary of my method:  <br/>
Paragraph Form: The goal is to randomly show two profiles in Qualtrics to a respondent and be able to know which profile the respondent picked as well as which attributes were included in each profile shown to each respondent. With this information, one can find the AMCEs of different attributes and do all sorts of analyses. The goal can be accomplished in Qualtrics if images of all possible profiles (all possible attribute level combinations) are included in the Qualtrics library, and JavaScript code is written in the Qualtrics survey to randomly sample from the library. To do this, one must first create all possible profiles for the conjoint. To do this, a profile template must first be created, and then the template can be filled in with all possible attribute level combintations. This can be done by creating the template in a Google Slides presentation and then using the Google Slides API to duplicate and edit the template slide to create all possible profiles. The Python script "Conjoint v3 all profiles.py" does the duplicating and editing, while other scripts in this repository (e.g. "Image_Resize_and_Blur_Works.py") automate other small tasks. 

Succinct List of Steps: <br/>
    1. Create the template profile in Google Slides
    2. Define attributes and attribute levels
    3. Generate all possible profiles in Google Slides
    4. Download the profiles as pngs and then upload them all to Qualtrics library
    5. Write JavaScript code in Qualtrics that randomly samples images of profiles from the library and sets embedded data based on the chosen profile's attributes
    6. Once the survey is fielded and data is collected, download the data and analyze it. 


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
    17. Write JavaScript code that randomizes which profiles are shown in Qualtrics (Do this by hand - mostly this can be copied from the R script output) <br/>
    18. Ensure forced difference on relevant attributed, if desired (For example, I wanted to force difference on religion) (Do this by hand) <br/>
    19. Ensure that embedded data is set and viewable in Qualtrics output data (Do this by hand) <br/>
    20. Download the output of the Qualtrics survey into R (Do this by hand) <br/>
    21. Manipulate the data to get it in the correct format for each analysis (R) <br/>
    22. Analyze data in R. (R) <br/>


I'd like to thank the following people for their help in the process of creating this method: Salma Mousa, Graeme Blair, Chris Tausanovitch, and Jeff Lewis. My JavaScript code is based on a template written by Clayton Becker, who I would also like to thank. 
