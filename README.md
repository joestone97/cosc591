# Directional Hearing Workshop
Hello! In this repository you will find the code and data used to create the Directional Hearing Workshop WebApp.

The web application is currently accessible using the following link:

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://joestone97-cosc591-home-page-publish-test2-2c3vq0.streamlit.app/)


## Context
The educational workshop was created for a University of New England (UNE) Masters of Data Science project. The client, Ron Bradbury, requested a web application be developed that can be used to teach High School Students the key concepts in directional hearing.

The essence of the project relates to the ability of humans (and other animals) to identify the direction of a
sound source in a transverse plane is due to having two ears. It is
thought that the key factors in identifying direction are differences in
L-R sound:
- Arrival time (delay)
- Volume
- Frequency

Additionally, to explore and introduce the more advanced audio augmentation methodologies which are related these factors. The creation and application of Head Related Transfer Functions (HRTFs) is one such method.

## Meet the team 

- **Joseph Stone** email@email.com

<sub>blurb about studies/role in the project/experience</sub> 

- **Jesse Taylor** email@email.com

<sub>blurb about studies/role in the project/experience</sub> 

- **Bhagya Karunarathna** email@email.com

<sub>blurb about studies/role in the project/experience</sub> 

- **Ron Bradbury** email@email.com

<sub>blurb about him being a former lecturer</sub> 

## Manuals
The project required the creation of the following manuals. These explain to users how to set up the web application from scratch, and explain the expected use cases for the application.

### User
link?

### Installation
link?

### Repository overview
Use relative links to link to the different folders, and use this section to explain the folder structure?
- **Front-end**: The website's design and structure are provided by the script [Home_Page.py](/Home_Page.py) and the scripts in the folder titled ["Pages"](pages/). the three scripts are named after as they appear in the sidebar in the web application, and contain all of the code relating to the display of each web page.
- **Back-end**: The scripts in the folder "[scripts](/scripts/)" essentially provide all of the audio alteration functionality for the web application (the "back end"). The changes to the delay, volume, and frequency are performed using the appropriately named scripts, and the application of the HRTF is done using the "htrf" script.
- **Data**: The data the web application needs to run is also all contained in a single folder, the [data](/data) folder. Inside there are three subfolders dividing the inputs into the audio, images, and hrtf data used.
- **Deployment Requirements**: The requirements for the web application must be specified in the [requirements text file](/requirements.txt) in order for the website which hosts the web application deploy the application without errors.


## Credit / Acknowledgements
### HRTFs
The HRTFs were sourced from https://3d3a.princeton.edu/3d3a-lab-head-related-transfer-function-database#:-:text=hrtf, specifically this embedded link https://gofile-36477a4a30.us5.quickconnect.to/fsdownload/67b2jfkjw/Public-Data.
maybe link/mention the exact hrtf subject used?

### Audio Data
???

### Image Data
???

# Copyright
note about it being copyleft
