# Number Plate Recognition System

A Bangla number plate recognition system made using Python and done by me and my teammates from IUB for our Senior Project

Streets and parkways are one of the main methods of transport and there should be a few guidelines to guarantee that everything is good to go. Street rules are intended to safeguard us and from different drivers out and about and to keep up with appropriate traffic stream. Auto collisions are principally brought about by infringement of transit regulations. Street accidents and mishaps kill 12,000 individuals and cause 35,000 wounds in Bangladesh every year, says the Accident Research Institute of the state-run Bangladesh University of Engineering and Technology.
We are making a framework to recognize the number plates and speed of a vehicle. Our initiative would dispense the manual approach of recognizing traffic offenders. As a result, it decreases staff and permits us to take necessary actions faster.

## Dependencies

1. **pytesseract**, **Tesseract-OCR** (install from **<https://tesseract-ocr.github.io/tessdoc/Home.html>** and choose Bengali language)
2. **numpy**
3. **cv2** (install by running "pip install opencv-contrib-python")
4. **PIL** (for image resizing and processing)
5. **datetime**, **time**
6. **mysql.connector** (for database connection) (install by running "pip install mysql-connector-python")
7. **XAMPP** (for running the mysql server) (install from **<https://www.apachefriends.org/download.html>**) (for linux follow the instructions from **<https://www.apachefriends.org/faq_linux.html>**)
(for linux start server with **sudo /opt/lampp/lampp start** and stop with **sudo /opt/lampp/lampp stop**)
8. **Microsoft .NET 4.0** (for Rebex Tiny SFTP Server)
9. **os** (for running the sftp application "Rebex Tiny SFTP Server")
10. **keyboard**
11. **tkinter** (for GUI)
12. **prettytable** (for report and receipt generate)
13. **requests**, **json** (for accessing SMSQ's SMS API)
14. **pywhatkit**, **pyautogui** (for optional WhatsApp message sending)
15. **envelopes** (for single mail)
16. **email**, **smtplib**, **ssl**, **Template** (for bulk email)
17. **msvcrt**, **sys**, **termios** (for input flushing)
18. **pdfkit**, **wkhtmltopdf** (for converting html to pdf) (install from **<https://wkhtmltopdf.org/downloads.html>**)

* **For Windows, install all requirements by running "pip install -r requirements.txt"**
* **For Linux, run *sudo su* and install requirements one by one and follow instructions at <https://iotdesignpro.com/projects/real-time-license-plate-recognition-using-raspberry-pi-and-python> in order to install pytesseract and opencv (use pip3 for installation)**

## How to Run

1. Install Python and the dependencies
2. Run "number plate recognition system.py"

## File and Folder Structure

N.B. {epoch_time} represents the time of saving the record

1. **Detected_Plates** - folder contains the image of the detected number plates (following the format "Plate {epoch_time}.png")
2. **Frames** - folder contains the captured image (following the format "Frame {epoch_time}.png")
3. **License_Info_data** - folder contains the license info after making a query (following the format "Info {epoch_time}.txt" and "ID card {epoch_time}.jpg" for the NID card)
4. **Plate_data** - folder contains the detected plate info after making a query (following the format "Plate {epoch_time}.txt" and "Plate {epoch_time}.jpg" for the detected plate)
5. **sample** - folder contains some sample images
6. **email contacts.txt** - text file contains the name and email address of contacts separated by comma for bulk email. For example, "Hakim,hakim@jashim.com"
7. **email template.txt** - text file contains the starting template for each bulk email. ${PERSON_NAME} is replaced with the name provided in "email contacts.txt"
8. **help image.jpg** - image file contains the keyboard shortcuts that can be used while a camera or image is open
9. **keyboard shortcuts.txt** - text file contains the keyboard shortcuts that can be used while a camera or image is open and can be shown when "h" is pressed
10. **nid_image_resized.jpg** - image file generated when selecting an image file whose resolution is greater than 600x600
11. **numberPlates.txt** - text file generated when detected number plate is saved to text file
12. **receipt.html** - html file generated by prettytable containing the money receipt of all dues
13. **receipt.pdf** - converted pdf file of "receipt.html" which is sent by email
14. **records.html** - html file generated by prettytable containing all data of the specified table
15. **requirements.txt** - text file containing the list of required modules
16. **senior project.code-workspace** - generated by Visual Studio Code
17. **server-private-key-dss.ppk**, **server-private-key-rsa.ppk** - generated by Rebex Tiny SFTP Server
18. **sent_email_log.txt**, **sent_sms_log.txt** - text files containing the log of the messages sent

## Contributors

* **Abu Musa Sakib** - 1810617
* **Sumyia Afnan Mukta** - 1810668
* **Chowdhury Mohammad Rayik** - 1821734
