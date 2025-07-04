# Whirpool-Product-Image-Scraper
A Python-based web scraping system that automates image extraction of Whirlpool product parts using data from a CSV or Google Sheet.

How to Use:
-----------

1. Requirements:
   --------------
   - Python 3.10 or higher installed
   - Google Chrome browser installed
   - Internet connection (used for scraping websites)

2. Install the necessary Python libraries:
   ---------------------------------------
   Open Command Prompt (CMD) inside the project folder and run:

   pip install flask selenium pandas webdriver-manager

3. Folder Structure:
   ------------------
   Scraping Image Web tool/
   ├── app.py                          => Main backend logic
   ├── templates/
   │   └── index.html                  => Web interface for uploading and scraping
   ├── static/
   │   └── style.css                   => Styling for the frontend
   ├── For image scraping - Sheet1.csv => Your input CSV file (must include a column named "Title")
   └── downloaded_images/             => Folder where all scraped images will be saved

4. Run the Web Application:
   -------------------------
   From the same directory as app.py, run:

   python app.py

   Once running, open this in your browser:

   http://127.0.0.1:5000

5. Using the Interface:
   ---------------------
   - Drag and drop your CSV file into the web page (it must contain a 'Title' column with part numbers).
   - Click the “Start Scraping” button.
   - The system will go through each part number and search Whirlpool sources for actual product images or diagrams.
   - Once completed, click “Download Images” to download all the scraped images as a .zip file.

6. CSV File Notes:
   ----------------
   - Make sure your CSV has a column labeled "Title" which contains the part numbers.
   - The second column in your file should be the one with part numbers (if using a different name, update the script).

7. Output:
   --------
   - All images are saved inside the 'downloaded_images' folder.
   - You can download them all together as a ZIP file after scraping.
   - If no product photo is found, a diagram image may be used if available.

Credits:
--------
Created by: Mark Jenri Ocampo
Tool designed for Whirlpool part number image automation needs.

![image](https://github.com/user-attachments/assets/39ea958e-f2b1-4d66-aa0a-a54707a00667)

