# plate recognition modules
import imutils
import pytesseract
#import easyocr
import numpy as np
import cv2  # opencv-contrib-python

# image enhancement and processing modules
from PIL import Image, ImageEnhance, ImageFilter

# date and time modules
import datetime
import time

# database modules
import mysql.connector  # mysql-connector-python
from mysql.connector import Error

import os
import sys

# keyboard entry module
import keyboard

# gui modules
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import askyesno, showinfo
from tkinter.messagebox import showerror
from tkinter.messagebox import askquestion

# receipt and report generate module
from prettytable import PrettyTable

import io


selected_query = ''

#number plate data
epoch_time = int(time.time())

now = datetime.datetime.now()
date_time = str(now)

license_plate = ''
plate_image = ''

#email related data
attachment_file = ''
query_result = ''

sys_manager_name = "System Manager"
sys_manager_phone_number = 8801621554760
sys_manager_email = "1810617@iub.edu.bd"

def is_raspberrypi():
    try:
        with io.open('/sys/firmware/devicetree/base/model', 'r') as m:
            if 'raspberry pi' in m.read().lower(): return True
    except Exception: pass
    return False

if(not(is_raspberrypi())):
    cap = cv2.VideoCapture(1) #camera capture
# database functions


# table create functions
def create_plate_table():
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='license_plates',
                                             user='root',
                                             password='')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            mySql_Create_Table_Query = """CREATE TABLE plate (
                                            epoch_time INT(10) NOT NULL ,
                                            date TIMESTAMP NOT NULL ,
                                            license_plate VARCHAR(250) NOT NULL ,
                                            plate_image BLOB NOT NULL ,
                                            CONSTRAINT Plate_PK PRIMARY KEY (license_plate,date))
                                            ENGINE = InnoDB; """
            cursor = connection.cursor()

            result = cursor.execute(mySql_Create_Table_Query)
            print("Plate Table created successfully ")
    except mysql.connector.Error as error:
        print("Failed to create table: {}".format(error))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
            time.sleep(3)

def create_license_info_table():
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='license_plates',
                                             user='root',
                                             password='')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            mySql_Create_Table_Query = """CREATE TABLE license_info (
                                            license_plate VARCHAR(250) NOT NULL ,
                                            date_of_expiry TIMESTAMP NOT NULL ,
                                            owner_name VARCHAR(250) NOT NULL ,
                                            owner_phone_number VARCHAR(13) NOT NULL ,
                                            owner_email VARCHAR(250) NOT NULL ,
                                            owner_nid_card_number VARCHAR(10) NOT NULL ,
                                            owner_nid_card_image BLOB NOT NULL ,
                                            CONSTRAINT LicenseInfo_PK PRIMARY KEY (license_plate),
                                            CONSTRAINT LicenseInfo_FK FOREIGN KEY (license_plate) REFERENCES plate(license_plate))
                                            ENGINE = InnoDB; """
            cursor = connection.cursor()

            result = cursor.execute(mySql_Create_Table_Query)
            print("License info Table created successfully ")
    except mysql.connector.Error as error:
        print("Failed to create table: {}".format(error))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
            time.sleep(3)

def create_dues_table():
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='license_plates',
                                             user='root',
                                             password='')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            mySql_Create_Table_Query = """CREATE TABLE dues (
                                            license_plate VARCHAR(250) NOT NULL ,
                                            epoch_time INT(10) NOT NULL ,
                                            last_fined_date TIMESTAMP NOT NULL ,
                                            amount_of_fine INT(10) NOT NULL ,
                                            times_fined_for_expiry INT(10) NOT NULL ,
                                            times_fined_for_unregistered INT(10) NOT NULL ,
                                            CONSTRAINT Dues_PK PRIMARY KEY (license_plate,last_fined_date),
                                            CONSTRAINT Dues_FK FOREIGN KEY (license_plate) REFERENCES plate(license_plate))
                                            ENGINE = InnoDB; """
            cursor = connection.cursor()

            result = cursor.execute(mySql_Create_Table_Query)
            print("Dues Table created successfully ")
    except mysql.connector.Error as error:
        print("Failed to create table: {}".format(error))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
            time.sleep(3)


# table insert functions
def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        binaryData = file.read()
    return binaryData

def insert_data_into_plate_table(epoch_time, date, license_plate, plate_image):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='license_plates',
                                             user='root',
                                             password='')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)

            cursor = connection.cursor()
            mySql_insert_query = """INSERT INTO plate (epoch_time, date, license_plate,plate_image) 
                                        VALUES (%s, %s, %s,%s) """

            plate_image_bin = convertToBinaryData(plate_image)

            # Convert data into tuple format
            record = (epoch_time, date, license_plate, plate_image_bin)
            result = cursor.execute(mySql_insert_query, record)
            connection.commit()
            print("Record inserted successfully into Plate table")
            showinfo(
                title='Success',
                message="Successfully written to database"
            )

    except mysql.connector.Error as error:
        print("Failed to insert record into Plate table: {}".format(error))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def insert_data_into_license_info_table(license_plate, date_of_expiry, owner_name, owner_phone_number, owner_email, owner_nid_card_number, owner_nid_card_image):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='license_plates',
                                             user='root',
                                             password='')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)

            cursor = connection.cursor()
            mySql_insert_query = """INSERT INTO license_info (license_plate, date_of_expiry, owner_name, owner_phone_number, owner_email, owner_nid_card_number, owner_nid_card_image) 
                                        VALUES (%s, %s, %s, %s, %s, %s, %s) """

            owner_nid_card_image_bin = convertToBinaryData(
                owner_nid_card_image)

            # Convert data into tuple format
            record = (license_plate, date_of_expiry, owner_name, owner_phone_number,
                      owner_email, owner_nid_card_number, owner_nid_card_image_bin)
            result = cursor.execute(mySql_insert_query, record)
            connection.commit()
            print("Record inserted successfully into License info table")
            showinfo(
                title='Registration Complete',
                message='Registered successfully to the system'
            )

    except mysql.connector.Error as error:
        print("Failed to insert record into License info table: {}".format(error))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")

def insert_data_into_dues_table(license_plate, epoch_time, last_fined_date, amount_of_fine, times_fined_for_expiry, times_fined_for_unregistered):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='license_plates',
                                             user='root',
                                             password='')
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)

            cursor = connection.cursor()
            mySql_insert_query = """INSERT INTO dues (license_plate, epoch_time, last_fined_date, amount_of_fine, times_fined_for_expiry, times_fined_for_unregistered) 
                                        VALUES (%s, %s, %s,%s,%s,%s) """

            # Convert data into tuple format
            record = (license_plate, epoch_time, last_fined_date, amount_of_fine,
                      times_fined_for_expiry, times_fined_for_unregistered)
            result = cursor.execute(mySql_insert_query, record)
            connection.commit()
            print("Record inserted successfully into Dues table")

    except mysql.connector.Error as error:
        print("Failed to insert record into Dues table: {}".format(error))
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")


# table print functions
def print_plate_data(records):
    print("\nPrinting each row")
    for row in records:
        print("Epoch Time = ", row[0])
        print("Date  = ", row[1])
        print("License Plate  = ", row[2], "\n")

def print_license_info_data(records):
    print("\nPrinting each row")
    for row in records:
        print("License Plate  = ", row[0])
        print("Date of Expiry = ", row[1])
        print("Owner Name  = ", row[2])
        print("Owner Phone Number  = ", row[3])
        print("Owner Email  = ", row[4])
        print("Owner NID card number = ", row[5], "\n")

def print_single_due_data(record):
    lines = "License Plate  = " + record[0] + "\n" +  "Epoch Time  = " + str(record[1]) + "\n" + "Last fined Date  = " + str(record[2]) + "\n" + "Amount of fine  = " + str(record[3]) + "\n" + "Number of times fined for license expiry  =  " + str(record[4]) + "\n" + "Number of times fined for not registering license  = " + str(record[5]) + "\n"
    print(lines)
    return lines


# table get all data functions
def get_all_data_from_plate_table():
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='license_plates',
                                             user='root',
                                             password='')
        if connection.is_connected():
            sql_select_Query = "select * from plate"
            cursor = connection.cursor()
            cursor.execute(sql_select_Query)
            # get all records
            records = cursor.fetchall()
            print("Total number of rows in table: ", cursor.rowcount)

    except mysql.connector.Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    return records

def get_all_data_from_license_info_table():
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='license_plates',
                                             user='root',
                                             password='')
        if connection.is_connected():
            sql_select_Query = "select * from license_info"
            cursor = connection.cursor()
            cursor.execute(sql_select_Query)
            # get all records
            records = cursor.fetchall()
            print("Total number of rows in table: ", cursor.rowcount)

    except mysql.connector.Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    return records

def get_all_data_from_dues_table():
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='license_plates',
                                             user='root',
                                             password='')
        if connection.is_connected():
            sql_select_Query = "select * from dues"
            cursor = connection.cursor()
            cursor.execute(sql_select_Query)
            # get all records
            records = cursor.fetchall()
            print("Total number of rows in table: ", cursor.rowcount)

    except mysql.connector.Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    return records


# table search functions
def write_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)

def get_car_data_from_license_info_table(license_plate):
    print("Reading data from License info table")

    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='license_plates',
                                             user='root',
                                             password='')

        cursor = connection.cursor()
        sql_select_Query = """SELECT * from license_info where license_plate = %s"""

        cursor.execute(sql_select_Query, (license_plate,))
        record = cursor.fetchall()

        for row in record:
            owner_nid_card_image = row[6]
            file = open(
                    f"License_Info_data/Info {row[5]}.txt", 'w', encoding='utf-8')
            expiry_dt_obj = datetime.datetime.strptime(
                str(row[1]), "%Y-%m-%d %H:%M:%S")
            date_time_formal = expiry_dt_obj.strftime(
                "%A, %d %B %Y at %I:%M %p")
            file.write(
                "Number Plate is: \n"+str(row[0])+"\n"
                "Date of expiry: "+date_time_formal+"\n" +
                "Owner name: "+row[2]+"\n" +
                "Owner phone number: "+str(row[3])+"\n" +
                "Owner email address: "+row[4]+"\n" +
                "Owner NID card number: "+str(row[5])+"\n"
            )

            print("Storing NID card image on disk \n")
            write_file(owner_nid_card_image,
                        f"License_Info_data/ID card {row[5]}.jpg")

    except mysql.connector.Error as error:
        print("Failed to read data from MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    return record

def get_license_info_data_by_nid_card_number(nid_card_number):
    print("Reading data from License info table")

    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='license_plates',
                                             user='root',
                                             password='')

        cursor = connection.cursor()
        sql_select_Query = """SELECT * from license_info where owner_nid_card_number = %s"""

        cursor.execute(sql_select_Query, (nid_card_number,))
        record = cursor.fetchall()
        for row in record:
            owner_nid_card_image = row[6]

            file = open(
                    f"License_Info_data/Info {row[5]}.txt", 'w', encoding='utf-8')
            
            expiry_dt_obj = datetime.datetime.strptime(
                str(row[1]), "%Y-%m-%d %H:%M:%S")
            date_time_formal = expiry_dt_obj.strftime(
                "%A, %d %B %Y at %I:%M %p")
            file.write(
                "Number Plate is: \n"+row[0]+"\n"
                "Date of expiry: "+date_time_formal+"\n" +
                "Owner name: "+row[2]+"\n" +
                "Owner phone number: "+str(row[3])+"\n" +
                "Owner email address: "+row[4]+"\n" +
                "Owner NID card number: "+str(row[5])+"\n"
            )

            print("Storing NID card image on disk \n")
            write_file(owner_nid_card_image,
                        f"License_Info_data/ID card {row[5]}.jpg")

    except mysql.connector.Error as error:
        print("Failed to read data from MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    return record

def get_due_data_from_dues_table(license_plate):
    print("Reading data from Dues table")

    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='license_plates',
                                             user='root',
                                             password='')

        cursor = connection.cursor()
        sql_select_Query = """SELECT * from dues where license_plate = %s"""

        cursor.execute(sql_select_Query, (license_plate,))
        record = cursor.fetchall()

    except mysql.connector.Error as error:
        print("Failed to read data from MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    return record

def get_due_data_by_epoch_time(epoch_time):
    print("Reading data from Dues table")

    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='license_plates',
                                             user='root',
                                             password='')

        cursor = connection.cursor()
        sql_select_Query = """SELECT * from dues where epoch_time = %s"""

        cursor.execute(sql_select_Query, (epoch_time,))
        record = cursor.fetchall()

    except mysql.connector.Error as error:
        print("Failed to read data from MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    return record

def get_plate_data_by_epoch_time(epoch_time):
    print("Reading data from Plate table")

    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='license_plates',
                                             user='root',
                                             password='')

        cursor = connection.cursor()
        sql_select_Query = """SELECT * from plate where epoch_time = %s"""

        cursor.execute(sql_select_Query, (epoch_time,))
        record = cursor.fetchall()
        for row in record:
            image = row[3]

            file = open(
                    f"Plate_data/Plate {row[0]}.txt", 'w', encoding='utf-8')
            dt_object = datetime.datetime.fromtimestamp(row[0])
            date_time_formal = dt_object.strftime("%A, %d %B %Y at %I:%M %p")
            file.write("Timestamp: "+date_time_formal+"\n" +
                       "Number Plate is: \n"+row[2]+"\n")

            print("Storing plate image on disk \n")
            write_file(image, f"Plate_data/Plate {row[0]}.png")

    except mysql.connector.Error as error:
        print("Failed to read data from MySQL table {}".format(error))

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    return record


# dues table modify function
def modify_dues_table_data(license_plate, epoch_time, last_fined_date, amount_of_fine, times_fined_for_expiry, times_fined_for_unregistered):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='license_plates',
                                             user='root',
                                             password='')

        cursor = connection.cursor()

        print("Before updating a record ")
        sql_select_query = """select * from dues where license_plate = %s"""
        cursor.execute(sql_select_query, (license_plate,))
        record = cursor.fetchone()
        print_single_due_data(record)

        # Update single record now
        sql_update_query = """Update dues set epoch_time = %s, last_fined_date = %s, amount_of_fine = %s, times_fined_for_expiry = %s, times_fined_for_unregistered = %s where license_plate = %s"""
        cursor.execute(sql_update_query, (epoch_time, last_fined_date,amount_of_fine, times_fined_for_expiry,
                       times_fined_for_unregistered, license_plate,))
        connection.commit()
        print("Record Updated successfully ")

        print("After updating record ")
        cursor.execute(sql_select_query, (license_plate,))
        record = cursor.fetchone()
        print_single_due_data(record)

    except mysql.connector.Error as error:
        print("Failed to update table record: {}".format(error))
    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")


# dues table delete function
def delete_dues_table_data(license_plate):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='license_plates',
                                             user='root',
                                             password='')

        cursor = connection.cursor()

        print("Before deleting a record ")
        sql_select_query = """select * from dues where license_plate = %s"""
        cursor.execute(sql_select_query, (license_plate,))
        record = cursor.fetchone()
        print_single_due_data(record)

        # Delete single record now
        sql_delete_query = """Delete from dues where license_plate = %s"""
        cursor.execute(sql_delete_query, (license_plate,))
        connection.commit()
        print('number of rows deleted', cursor.rowcount)

        # Verify using select query (optional)
        cursor.execute(sql_select_query, (license_plate,))
        records = cursor.fetchall()
        if len(records) == 0:
            print("Record Deleted successfully ")

    except mysql.connector.Error as error:
        print("Failed to delete table record: {}".format(error))
    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed")



# send message functions
def send_sms(phone_number, message):
    # send sms
    import requests
    import json

    url = "https://api.smsq.global/api/v2/SendSMS"

    querystring = {
        "SenderId": "8804445649826",
        "Is_Unicode": True,
        "Is_Flash": False,
        "SchedTime": "",
        "GroupId": "",
        "Message": message,
        "MobileNumbers": phone_number,
        "ApiKey": "WDoKYJPIUu/5jVnfTwR1tTb5z46ZQ3fsYzqlCkg6mTI=",
        "ClientId": "24502137-4ea0-4be2-8db8-02e087f84118"
    }

    headers = {
        'cache-control': "no-cache"
    }

    try:
        response = requests.request("GET", url,
                                    headers=headers,
                                    params=querystring)
        if(response.status_code == 200):
            print("Connected to the SMS API")

        result = response.json()

        print("SMS Successfully Sent to the API")

        dt_object = datetime.datetime.fromtimestamp(int(time.time()))
        date_time_formal = dt_object.strftime("%A, %d %B %Y at %I:%M %p")

        file = open("sent_sms_log.txt", 'a', encoding='utf-8')
        file.write("Sent message at: "+date_time_formal+"\n" +
                    "Phone Number is:"+str(phone_number)+"\n" +
                    "Message:"+message+"\n")
        file.close()
    except Exception as e:
        print(f"Exception has occured: {e}")
def send_whatsapp_message(phone_number, message):
    # send whatsapp message

    # whatsapp message module
    import pywhatkit
    import pyautogui as pg

    pywhatkit.sendwhatmsg_instantly(
        phone_number, message, 23)
    for i in range(10):
        pg.press("tab")
    pg.press("enter")

def send_email_with_attachment(email_address, sender_name, subject, message_text, attachment_file):
    from envelopes import Envelope, GMailSMTP

    print(f"Sending email to {sender_name}")
    envelope = Envelope(
        from_addr=(u'sakib4@live.com', u'License Management Department'),
        to_addr=(email_address, sender_name),
        subject=subject,
        text_body=message_text
    )
    if attachment_file != '':
        envelope.add_attachment(attachment_file)
    
    # Send the envelope using an ad-hoc connection...
    envelope.send('smtp.office365.com', login='sakib4@live.com',
                password='theMGFboys01', tls=True)

    showinfo(
        title='Email',
        message=f"Email sent successfully to {sender_name}"
    )

    print(f"Email sent successfully to {sender_name}")

    dt_object = datetime.datetime.fromtimestamp(int(time.time()))
    date_time_formal = dt_object.strftime("%A, %d %B %Y at %I:%M %p")

    file = open("sent_email_log.txt", 'a', encoding='utf-8')
    file.write("Sent email at: "+date_time_formal+"\n" +
                "Name of sender is:"+sender_name+"\n" +
                "Email address is:"+email_address+"\n" +
                "Subject is:"+subject+"\n" +
                "Message: \n"+message_text+"\n" +
                "Attached file: "+attachment_file+"\n" )
    file.close()

def send_bulk_email_with_template_and_attachment(contacts_file, starting_template_file, attachment_file, attachment_file_name, subject, message_content):
    # email modules

    # template module
    from string import Template

    # import the smtplib module.
    import email
    import smtplib
    import ssl

    # import necessary packages
    from email import encoders
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    # email functions

    def read_template(filename):
        with open(filename, 'r', encoding='utf-8') as template_file:
            template_file_content = template_file.read()
        return Template(template_file_content)

    # Function to read the contacts from a given contact file and return a
    # list of names and email addresses

    def get_contacts(filename):
        names = []
        emails = []
        with open(filename, mode='r', encoding='utf-8') as contacts_file:
            for a_contact in contacts_file:
                names.append(a_contact.split(",")[0])
                emails.append(a_contact.split(",")[1])
        return names, emails

    print("Setting up email")
    # set up the SMTP server
    s = smtplib.SMTP(host='smtp.office365.com', port=587)
    s.starttls()

    MY_ADDRESS = "sakib4@live.com"
    PASSWORD = "theMGFboys01"
    s.login(MY_ADDRESS, PASSWORD)
    print("Set up complete")

    names, emails = get_contacts(contacts_file)  # read contacts
    message_template = read_template(starting_template_file)

    # For each contact, send the email:
    for name, email in zip(names, emails):
        msg = MIMEMultipart()       # create a message

        # add in the actual person name to the message template
        message = message_template.substitute(PERSON_NAME=name.title())

        content = message_content
        message = message + content
        content = ''

        # setup the parameters of the message
        msg['From'] = MY_ADDRESS
        msg['Bcc'] = email  # Recommended for mass emails
        msg['Subject'] = subject

        # add in the message body
        msg.attach(MIMEText(message, 'plain'))

        filename = attachment_file

        # Open file in binary mode
        with open(filename, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

            # Encode file in ASCII characters to send by email
            encoders.encode_base64(part)

            # Add header as key/value pair to attachment part
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {attachment_file_name}",
            )

            # Add attachment to message
            msg.attach(part)

            # send the message via the server set up earlier.
            s.send_message(msg)

            print("Email has been sent to " + name)

            del msg
    
    showinfo(
        title='Success',
        message="Emails have been successfully sent"
    )

# numberplate recognition function
def recognise_numberplate(img, frame_name, plate_name):
    #img = imutils.resize(img, width=500)
    text = ''

    cv2.imwrite(frame_name, img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert to grey scale
    gray = cv2.bilateralFilter(gray, 11, 17, 17)  # Blur to reduce noise
    edged = cv2.Canny(gray, 30, 200)  # Perform Edge detection (170, 200)
    keypoints = cv2.findContours(
        edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # cnts,new, cv2.RETR_LIST
    img1 = img.copy()

    cnts = keypoints[0] if len(keypoints) == 2 else keypoints[1]
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]  # :30
    cv2.drawContours(img1, cnts, -1, (0, 255, 0), 3)

    NumberPlateCount = None
    img2 = img.copy()
    cv2.drawContours(img2, cnts, -1, (0, 255, 0), 3)

    for i in cnts:
        perimeter = cv2.arcLength(i, True)
        approx = cv2.approxPolyDP(i, 0.018 * perimeter, True)  # 0.2    10
        if len(approx) == 4:
            NumberPlateCount = approx
            #x, y, w, h = cv2.boundingRect(i)
            #crp_img = img[y:y+h, x:x+w]
            #plate_image = f"Detected_Plates\Plate {epoch_time}.png"
            #cv2.imwrite(plate_image, crp_img)
            break
    mask = np.zeros(gray.shape, np.uint8)
    try:
        new_image = cv2.drawContours(mask, [NumberPlateCount], 0, 255, -1)
        new_image = cv2.bitwise_and(img, img, mask=mask)
    except:
        showerror(
            title='Error',
            message="Cannot draw contours"
        )
    

    if NumberPlateCount is None:
        showerror(
            title='Error',
            message="No contour detected"
        )

    else:
        (x, y) = np.where(mask == 255)
        (x1, y1) = (np.min(x), np.min(y))
        (x2, y2) = (np.max(x), np.max(y))
        cropped_image = gray[x1:x2+1, y1:y2+1]
        cv2.imshow("Cropped Image", cropped_image)
        cv2.imwrite(plate_name, cropped_image)

        # operations for image enhancement if required
        #im = Image.open(plate_image)
        #im = im.filter(ImageFilter.MedianFilter())
        #enhancer = ImageEnhance.Contrast(im)
        #im = enhancer.enhance(2)
        #im = im.convert('1')
        # im.save(plate_image)
        if sys.platform == 'win32':
            pytesseract.pytesseract.tesseract_cmd = (
                r"C:\Program Files\Tesseract-OCR\tesseract")

        text = pytesseract.image_to_string(
            Image.open(plate_name), lang="ben")  # if required: config='--psm 11'

        #font = cv2.FONT_HERSHEY_SIMPLEX
        #res = cv2.putText(img, text=license_plate, org=(approx[0][0][0], approx[1][0][1]+60), fontFace=font, fontScale=1, color=(0,255,0), thickness=2, lineType=cv2.LINE_AA)
        res = cv2.rectangle(img, tuple(approx[0][0]), tuple(approx[2][0]), (0, 255, 0), 3)
        cv2.imshow("Result", res)
        return text

    """
    if NumberPlateCount is None:
        print("No contour detected")
    else:
        cv2.drawContours(img, [NumberPlateCount], -1, (0, 255, 0), 3)
        cv2.imshow("Frame", img)
        frame_image = f"Frames\Frame {epoch_time}.png"
        cv2.imwrite(frame_image, img)
        cv2.imshow("Cropped Image", crp_img)

        # operations for image enhancement if required
        #im = Image.open(plate_image)
        #im = im.filter(ImageFilter.MedianFilter())
        #enhancer = ImageEnhance.Contrast(im)
        #im = enhancer.enhance(2)
        #im = im.convert('1')
        # im.save(plate_image)

        text = pytesseract.image_to_string(
            Image.open(plate_image), lang="ben")  # if required: config='--psm 11'
        license_plate = text
        print("Detected Plate Number is:", license_plate)

        # cv2.putText(img, "DETECTED", (200, 465),
        #            cv2.FONT_HERSHEY_COMPLEX, 2, (49, 118, 255), 2)
    cv2.waitKey(500)
    """


# html to pdf convert function
def html_to_pdf(input_file_name):
    import pdfkit
    if sys.platform == 'win32':
        path_wkthmltopdf = "C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe"
        config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)

    options = {
        'page-size': 'Letter',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
        'custom-header': [
                    ('Accept-Encoding', 'gzip')
        ],
        'no-outline': None
    }
    if sys.platform == 'win32':
        pdfkit.from_file(f"{input_file_name}.html", f"{input_file_name}.pdf",
                        configuration=config, options=options)
    elif sys.platform == 'linux':
        pdfkit.from_file(f"{input_file_name}.html", f"{input_file_name}.pdf",
                        options=options)


# text file reading function
def read_text_file(file):
    file = open(file, 'r', encoding='utf-8')
    lines = ''
    for line in file.readlines():
        lines = lines + line + '\n'
    file.close()
    return lines


camera = False
closed = False

# create the root window
root = tk.Tk()
root.title('Number Plate Recognition System')
root.resizable(False, False)
root.geometry('420x300')


def camera_recognize():
    global camera
    camera = True
    global root
    root.destroy()

def image_recognize():
    global img
    filetypes = (
        ('JPG files', '*.jpg *.jpeg'),
        ('BMP files', '*.bmp'),
        ('PNG files', '*.png'),
        ('Other image files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Select an image file for number plate recognition',
        initialdir='/sample/test/',
        filetypes=filetypes
    )

    if filename != '':
        img = cv2.imread(filename)
        global root
        root.destroy()
    else:
        close()

def list_data():
    new_root = tk.Tk()
    # config the root window
    new_root.geometry('380x120')
    new_root.resizable(False, False)
    new_root.title('Show data from database')

    # label
    label = ttk.Label(new_root,text="Please select a database to show all data:")
    label.pack(fill=tk.X, padx=5, pady=5)

    # create a combobox
    selected_database = tk.StringVar()
    database_cb = ttk.Combobox(new_root, textvariable=selected_database)
    database_cb['values'] = ('plate', 'license_info', 'dues')

    # prevent typing a value
    database_cb['state'] = 'readonly'
    # place the widget
    database_cb.pack(fill=tk.X, padx=5, pady=5)

    def get_data():
        selected = database_cb.get()
        dt_object = datetime.datetime.fromtimestamp(int(time.time()))
        date_time_formal = dt_object.strftime("%A, %d %B %Y at %I:%M %p")
        found = False

        if selected == "plate":
            print("Getting plate data from database")
            records = get_all_data_from_plate_table()
            if(len(records) != 0):
                found = True
                print_plate_data(records)
                heading = '--------------Plate data--------------'

                date = f"Date: {date_time_formal}"

                table = PrettyTable(
                    ['Epoch Time', 'Date', 'License Plate'])

                for row in records:
                    epoch_time = row[0]
                    date_of_detection = row[1]
                    license_plate = row[2]

                    table.add_row([epoch_time, date_of_detection, license_plate])
            else:
                showerror(
                    title='Error',
                    message="No data in table"
                )
        elif selected == "dues":
            print("Getting due data from database")
            records = get_all_data_from_dues_table()
            if(len(records) != 0):
                found = True
                heading = '--------------Due data--------------'

                date = f"Date: {date_time_formal}"

                table = PrettyTable(
                    ['License Plate', 'Epoch Time', 'Last fined Date', 'Amount of Fine', 'Times fined for expiry', 'Times fined for unregistered'])
                for row in records:
                    print_single_due_data(row)

                    license_plate = row[0]
                    epoch_time = row[1]
                    last_fined_date = row[2]
                    amount_of_fine = row[3]
                    times_fined_for_expiry = row[4]
                    times_fined_for_unregistered = row[5]

                    table.add_row(
                        [license_plate, epoch_time, last_fined_date, amount_of_fine, times_fined_for_expiry, times_fined_for_unregistered])
            else:
                showerror(
                    title='Error',
                    message="No data in table"
                )
            
        elif selected == "license_info":
            print("Getting license info data from database")
            records = get_all_data_from_license_info_table()
            if(len(records) != 0):
                found = True
                print_license_info_data(records)

                heading = '--------------License info data--------------'

                date = f"Date: {date_time_formal}"

                table = PrettyTable(
                    ['License Plate', 'Date of Expiry', 'Owner Name', 'Owner Phone Number', 'Owner Email', 'Owner NID card number'])

                for row in records:
                    license_plate = row[0]
                    date_of_expiry = row[1]
                    owner_name = row[2]
                    owner_phone_number = row[3]
                    owner_email = row[4]
                    owner_nid_card_number = row[5]

                    table.add_row([license_plate, date_of_expiry, owner_name,
                                   owner_phone_number, owner_email, owner_nid_card_number])
            else:
                showerror(
                    title='Error',
                    message="No data in table"
                )
                time.sleep(3)

        if found == True:
            table_starting = "<html>\n<head>\n<title>Database Records</title>\n<style>\ntr > * + * {\n\tpadding-left: 4em;\n}\ntable, th, td {\n\tborder: 1px solid black;\n\tborder-collapse: collapse;\n}\n</style>\n</head>\n<body>\n"

            report = table_starting + f"<h1>{heading}</h1><br>\n" + f"<h2>{date}</h2>\n" + table.get_html_string() + "\n</body>\n</html>"

            file = open("records.html", 'w', encoding='utf-8')
            file.write(report)
            file.close()
            os.system("records.html")

    def close():
        new_root.destroy()

    list_button = ttk.Button(
        new_root,
        text='List records',
        command=get_data
    )
    quit_button = ttk.Button(
        new_root,
        text='Close',
        command=close
    )
    list_button.pack(expand=True)
    quit_button.pack(expand=True)
    new_root.mainloop()

def find_data():
    new_root = tk.Tk()

    # config the root window
    new_root.geometry('380x250')
    new_root.resizable(False, False)
    new_root.title('Search for data in database')

    # label
    label = ttk.Label(new_root,text="Please select an option to search data:")
    label.pack(fill=tk.X, padx=5, pady=5)

    # create a combobox
    selected_query_option = tk.StringVar()
    option_cb = ttk.Combobox(new_root, textvariable=selected_query_option)
    option_cb['values'] = ('plate by epoch_time', 'license_info by nid_card_number', 'dues by epoch_time')

    # prevent typing a value
    option_cb['state'] = 'readonly'

    # place the widget
    option_cb.pack(fill=tk.X, padx=5, pady=5)

    # label
    label = ttk.Label(new_root,text="Enter query: ")
    label.pack(fill=tk.X, padx=5, pady=5)

    query_field = ttk.Entry(new_root)

    query_field.pack(ipadx=120)

    def search():
        global selected_query
        selected_query = option_cb.get()
        query = query_field.get()

        global epoch_time, date_time, license_plate, plate_image, attachment_file, query_result

        if selected_query == "plate by epoch_time":
            print("Getting plate data from database")
            records = get_all_data_from_plate_table()

            if(len(records) != 0):
                results = get_plate_data_by_epoch_time(query)

                if (len(results) != 0):
                    print_plate_data(results)

                    epoch_time = results[0][0]
                    date_time = results[0][1]
                    license_plate = results[0][2]
                    plate_image = f"Plate_data\Plate {epoch_time}.png"
                    
                    attachment_file = plate_image

                    output = read_text_file(
                        f"Plate_data\Plate {epoch_time}.txt")
                    
                    query_result = output

                    output = output + \
                        f"\nPlate image is saved at:\n{plate_image}"

                    showinfo(
                        title='Record found',
                        message=output
                    )
                else:
                    showerror(
                        title='Error',
                        message="Cannot find data"
                    )
                    time.sleep(3)
            else:
                showerror(
                    title='Error',
                    message="No data in table"
                )
                time.sleep(3)

        elif selected_query == 'dues by epoch_time':
            print("Getting due data from database")
            records = get_all_data_from_dues_table()

            if(len(records) != 0):
                results = get_due_data_by_epoch_time(query)

                if (len(results) != 0):
                    for row in results:
                        output = print_single_due_data(row)

                        query_result = output

                    showinfo(
                        title='Record found',
                        message=output
                    )

                else:
                    showerror(
                        title='Error',
                        message="Cannot find data"
                    )
                    time.sleep(3)
            else:
                showerror(
                    title='Error',
                    message="No data in table"
                )
                time.sleep(3)

        elif selected_query == 'license_info by nid_card_number':
            print("Getting license info data from database")
            records = get_all_data_from_license_info_table()
            if(len(records) != 0):
                results = get_license_info_data_by_nid_card_number(query)
                if (len(results) != 0):
                    print_license_info_data(results)

                    output = read_text_file(
                        f"License_Info_data\Info {results[0][5]}.txt")

                    attachment_file = f"License_Info_data\ID card {results[0][5]}.jpg"
                    query_result = output

                    output = output + \
                        f"\nNID card image is saved at:\n License_Info_data\ID card {results[0][5]}.jpg"

                    showinfo(
                        title='Record found',
                        message=output
                    )
                else:
                    showerror(
                        title='Error',
                        message="Cannot find data"
                    )
                    time.sleep(3)
            else:
                showerror(
                    title='Error',
                    message="No data in table"
                )
                time.sleep(3)

    def send_mail():
        if query_result != '':
            global sys_manager_name, sys_manager_email
            subject = "Query Result"
            
            message = f"Hello {sys_manager_name},\nThis is to let you know the results of the query given below:\n{query_result}."

            send_email_with_attachment(
                sys_manager_email, sys_manager_name, subject, message, attachment_file)
        else:
            showerror(
                    title='Error',
                    message="No query has been made"
                )

    def convert_date_time():
        # create a GUI window
        new_root = tk.Tk()

        # set the title of GUI window
        new_root.title("Convert date time")

        # set the configuration of GUI window
        new_root.geometry("500x200")

        new_root.resizable(False, False)

        # create a Date label
        date = ttk.Label(
            new_root, text="Please enter a Date (as dd-mm-yyyy hh:mm:ss AM/PM)", justify=tk.LEFT, padding=10)
        
        date.grid(row=0, column=0)

        date_field = ttk.Entry(new_root)

        date_field.grid(row=1, column=0, ipadx="70")

        # create a Date label
        result = ttk.Label(
            new_root, text="The epoch time is: ", justify=tk.LEFT, padding=10)
        
        result.grid(row=2, column=0)

        result_field = ttk.Entry(new_root)

        result_field.grid(row=3, column=0, ipadx="70")

        def convert():
            date = date_field.get()

            try:
                dt_object = datetime.datetime.strptime(
                        date, "%d-%m-%Y %I:%M:%S %p") 
                result = int(time.mktime(dt_object.timetuple()))
            except ValueError:
                result_field.delete(0,"end")
                result_field.insert(0, "<Format is incorrect>")
            else:
                result_field.delete(0,"end")
                result_field.insert(0, result)

        convert = ttk.Button(new_root, text="Convert", command=convert)
        convert.grid(row=4, column=1)

        # start the GUI
        new_root.mainloop()

    def close():
        new_root.destroy()

    search_button = ttk.Button(
        new_root,
        text='Search',
        command=search
    )
    
    send_mail_button = ttk.Button(
        new_root,
        text='Send email',
        command=send_mail
    )

    date_time_to_epoch_time_button = ttk.Button(
        new_root,
        text='Convert date time to epoch_time',
        command=convert_date_time
    )

    close_button = ttk.Button(
        new_root,
        text='Close',
        command=close
    )

    search_button.pack(expand=True)
    send_mail_button.pack(expand=True)
    date_time_to_epoch_time_button.pack(expand=True)
    close_button.pack(expand=True)
    
    new_root.mainloop()

def generate_money_receipt_and_send_bulk_mail():
    print("Getting due data from database")

    records = get_all_data_from_dues_table()
    if(len(records) != 0):
        heading = '--------------Money Receipt--------------'

        dt_object = datetime.datetime.fromtimestamp(int(time.time()))
        date_time_formal = dt_object.strftime("%A, %d %B %Y at %I:%M %p")

        date = f"Date: {date_time_formal}"

        table = PrettyTable(
            ['License Plate', 'Owner Name', 'Owner NID', 'Last fined Date', 'Amount of Fine'])
        total = 0

        for row in records:
            print_single_due_data(row)

            license_plate = row[0]
            last_fined_date = row[2]
            amount_of_fine = row[3]

            owner_info = get_car_data_from_license_info_table(
                license_plate)

            if(len(owner_info) == 0):
                owner_name = "<unregistered>"
                owner_nid = "<unregistered>"
            else:
                owner_name = owner_info[0][2]
                owner_nid = owner_info[0][5]

            total += amount_of_fine

            table.add_row([license_plate, owner_name,
                           owner_nid, last_fined_date, amount_of_fine])

        table.add_row(['TOTAL', '--', '--', '--', f"Tk. {total}"])

        table_starting = "<html>\n<head>\n<title>Money Receipt</title>\n<style>\ntr > * + * {\n\tpadding-left: 4em;\n}\ntable, th, td {\n\tborder: 1px solid black;\n\tborder-collapse: collapse;\n}\n</style>\n</head>\n<body>\n"

        receipt = table_starting + f"<h1>{heading}</h1><br>\n" + f"<h2>{date}</h2>\n" + table.get_html_string() + f"\n<h3>Total amount due is Tk. {total}</h3>\n" + "\n</body>\n</html>"

        file_name = "receipt"

        file = open(f"{file_name}.html", 'w', encoding='utf-8')
        file.write(receipt)
        file.close()

        html_to_pdf(file_name)

        print("Receipt generated successsfully")

        attachment = f"{file_name}.pdf"
        attachment_file_name = f"Money Receipt {int(time.time())}.pdf"
        subject = "Money Receipt"
        message = "the money receipt of all the dues are attached. Please take necessary actions."

        send_bulk_email_with_template_and_attachment(
            "email contacts.txt", "email template.txt", attachment, attachment_file_name, subject, message)
    else:
        showerror(
            title='No data',
            message="No data in table"
        )
        time.sleep(3)

def run_sftp_server():
    showinfo(
        title='SFTP server',
        message="Running SFTP server"
    )
    os.system("RebexTinySftpServer-Binaries-Latest\\RebexTinySftpServer.exe")

def show_help():
    global img
    img = cv2.imread("help image.jpg")
    global root
    root.destroy()

def close():
    global root
    root.destroy()
    global closed
    closed = True
    global img
    img = cv2.imread("help image.jpg")


camera_button = ttk.Button(
    root,
    text='Recognize from camera',
    command=camera_recognize
)
image_button = ttk.Button(
    root,
    text='Recognize from image',
    command=image_recognize
)
list_data_button = ttk.Button(
    root,
    text='Show all data from database',
    command=list_data
)
search_data_button = ttk.Button(
    root,
    text='Find data from database',
    command=find_data
)
generate_money_receipt_and_send_bulk_mail_button = ttk.Button(
    root,
    text='Generate money receipt of dues and send bulk email',
    command=generate_money_receipt_and_send_bulk_mail
)
run_sftp_server_button = ttk.Button(
    root,
    text='Run SFTP server',
    command=run_sftp_server
)
help_button = ttk.Button(
    root,
    text='Show help',
    command=show_help
)
quit_button = ttk.Button(
    root,
    text='Close',
    command=close
)

camera_button.pack(expand=True)
image_button.pack(expand=True)
list_data_button.pack(expand=True)
search_data_button.pack(expand=True)
generate_money_receipt_and_send_bulk_mail_button.pack(expand=True)
if sys.platform == 'win32':
    run_sftp_server_button.pack(expand=True)
help_button.pack(expand=True)
quit_button.pack(expand=True)

root.protocol("WM_DELETE_WINDOW", close)

# run the app
root.mainloop()

if(is_raspberrypi() and camera == True):
    from picamera.array import PiRGBArray
    from picamera import PiCamera

    camera = PiCamera()
    camera.resolution = (640, 480)
    camera.framerate = 30
    rawCapture = PiRGBArray(camera, size=(640, 480))
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            img = frame.array
            rawCapture.truncate(0)

while True:
    if camera == True:
        if(not(is_raspberrypi())):
            success, img = cap.read()

    if closed == True:
        print("Closing...")
        cv2.destroyAllWindows()
        break
    else:
        cv2.imshow("Output", img)

    # press 's' to take still image from camera and recognise number plate
    if cv2.waitKey(1) & keyboard.is_pressed("s"):
        frame_image = f"Frames/Frame {epoch_time}.png"
        plate_image = f"Detected_Plates/Plate {epoch_time}.png"

        license_plate = recognise_numberplate(img, frame_image, plate_image)

        if license_plate != '':
            showinfo(
                title='Number Plate',
                message=f"Detected Number Plate is:\n {license_plate}"
            )

    # press 'h' to show keyboard shortcuts
    if keyboard.is_pressed("h"):
        shortcuts = read_text_file("keyboard shortcuts.txt")
        showinfo(
            title='Keyboard Shortcuts',
            message=shortcuts
        )

    # press 't' to write the detected number plate to text file
    if keyboard.is_pressed("t"):
        # text file operations
        #create_license_info_table()
        
        if license_plate != '':
            dt_object = datetime.datetime.fromtimestamp(epoch_time)
            date_time_formal = dt_object.strftime("%A, %d %B %Y at %I:%M %p")

            file = open("numberPlates.txt", 'a', encoding='utf-8')
            file.write("Detected: "+date_time_formal+"\n" +
                       "Number Plate is: \n"+license_plate+"\n")
            file.close()
            showinfo(
                title='Text file',
                message="Written to text file successfully"
            )

        else:
            showerror(
                title='Error',
                message="Nothing to write. Please recognize nameplate or search from plate table"
            )

    # press 'd' to write the detected number plate to database
    if keyboard.is_pressed("d"):
        # database operations
        #create_plate_table()
        if license_plate != '':
            insert_data_into_plate_table(epoch_time, date_time, license_plate,
                                         f"Detected_Plates\Plate {epoch_time}.png")
            print_plate_data(get_all_data_from_plate_table())
        else:
            showerror(
                title='Error',
                message="Nothing to write. Please recognize a number plate from camera or image"
            )
            
    # press 'l' to show all data from database
    if keyboard.is_pressed("l"):
        #create_dues_table()
        list_data()

    # press 'f' to find data from database and save to hard disk
    if keyboard.is_pressed("f"):
        find_data()

    # press 'r' to register the detected number plate
    if keyboard.is_pressed("r"):
        # database operations
        #create_license_info_table()

        if license_plate != '':
            paid_due = ""
            registered = False
            due_record = get_due_data_from_dues_table(license_plate)

            register_record = get_car_data_from_license_info_table(
                license_plate)

            if(len(due_record) != 0):
                due_amount = due_record[0][3]
                paid_due = askquestion(
                    "Query about dues", f"Has the owner paid his due of Tk.{due_amount}?")
            
            if(len(register_record) != 0):
                showerror(
                    title='Cannot register',
                    message='Sorry, cannot be registered into the system. Already registered'
                )
                registered = True
            else:
                if paid_due == "":
                    paid_due = "yes"


            if(paid_due == "yes" and registered == False):
                showinfo(
                    title='Registration',
                    message='Please enter the requested information on the registration form'
                )

                # create a GUI window
                root = tk.Tk()

                # set the title of GUI window
                root.title("Registration form")

                # set the configuration of GUI window
                root.geometry("750x400")

                root.resizable(False, False)

                # create a Owner Name label
                owner_name = ttk.Label(
                    root, text="Owner Name", justify=tk.LEFT, padding=10)

                # create a Owner Contact No. label
                owner_contact_no = ttk.Label(
                    root, text="Owner Contact No.\n(as 880xxxxxxxxxx)", justify=tk.LEFT, padding=10)

                # create a Owner Email id label
                owner_email_id = ttk.Label(
                    root, text="Owner Email id", justify=tk.LEFT, padding=10)

                # create a Date of License Expiry label
                date_of_license_expiry = ttk.Label(
                    root, text="Date of License Expiry\n(as dd-mm-yyyy hh:mm:ss AM/PM)", justify=tk.LEFT, padding=10)

                # create a Owner NID card No. label
                owner_nid_card_no = ttk.Label(
                    root, text="Owner NID card No.", justify=tk.LEFT, padding=10)

                # create a Owner NID card image label
                owner_nid_card_image = ttk.Label(
                    root, text="Owner NID card image\n(both front and back)\n(image would be resized if needed)", justify=tk.LEFT, padding=10)

                # grid method is used for placing
                # the widgets at respective positions
                # in table like structure .
                owner_name.grid(row=1, column=0)
                owner_contact_no.grid(row=2, column=0)
                owner_email_id.grid(row=3, column=0)
                date_of_license_expiry.grid(row=4, column=0)
                owner_nid_card_no.grid(row=5, column=0)
                owner_nid_card_image.grid(row=6, column=0)

                nid_card_image_file = ''

                def choose_image():
                    filetypes = (
                        ('JPG files', '*.jpg *.jpeg'),
                        ('BMP files', '*.bmp'),
                        ('PNG files', '*.png'),
                        ('Other image files', '*.*')
                    )

                    owner_nid_card_image = fd.askopenfilename(
                        title='Choose an image of the NID card of owner',
                        initialdir='/',
                        filetypes=filetypes
                    )

                    #file_stat = os.stat(C)
                    #file_size = file_stat.st_size

                    if owner_nid_card_image != '':
                        img = Image.open(owner_nid_card_image)
                        width, height = img.size

                        if (width > 600) or (height > 600):
                            img.thumbnail((600, 600))
                            img.save('nid_image_resized.jpg')
                            owner_nid_card_image = 'nid_image_resized.jpg'
                        showinfo(
                            title='Success',
                            message=f"Image has been selected"
                        )

                    """
                    while file_size > 204800:
                        showerror(
                            title='File size too big',
                            message='File size is greater than 200 KB or resolution greater than 1500x1500'
                        )
                        flush_input()
                        owner_nid_card_image = fd.askopenfilename(
                            title='Choose an image of the NID card of owner',
                            initialdir='/',
                            filetypes=filetypes
                        )
                        file_stat = os.stat(owner_nid_card_image)
                        file_size = file_stat.st_size

                        img = Image.open(owner_nid_card_image)
                        width, height = img.size
                    """
                    global nid_card_image_file
                    nid_card_image_file = owner_nid_card_image

                def insert():
                    date_of_expiry = date_of_license_expiry_field.get()

                    try:
                        expiry_dt_obj = datetime.datetime.strptime(
                        date_of_expiry, "%d-%m-%Y %I:%M:%S %p")

                        expiry_dt_timestamp = expiry_dt_obj.strftime(
                        "%Y-%m-%d %H:%M:%S")
                    except:
                        showerror(
                            title='Error',
                            message="Date time format is incorrect"
                        )

                    global license_plate
                    owner_name = owner_name_field.get()
                    owner_phone_num = owner_contact_no_field.get()
                    owner_email = owner_email_id_field.get()
                    owner_nid_card_num = owner_nid_card_no_field.get()

                    global nid_card_image_file
                    owner_nid_card_image = nid_card_image_file

                    try:
                        insert_data_into_license_info_table(
                            license_plate, expiry_dt_timestamp, owner_name, owner_phone_num, owner_email, owner_nid_card_num, owner_nid_card_image)
                    except:
                        showerror(
                            title='Error',
                            message="Format is incorrect"
                        )

                    global due_record

                    if(len(due_record) != 0):
                        delete_dues_table_data(license_plate)

                    records = get_all_data_from_license_info_table()
                    if(len(records) != 0):
                        print_license_info_data(records)
                    else:
                        showerror(
                            title='Error',
                            message="Nothing to write"
                        )

                    global root
                    root.destroy()

                # create a text entry box
                # for typing the information
                owner_name_field = ttk.Entry(root)
                owner_contact_no_field = ttk.Entry(root)
                owner_email_id_field = ttk.Entry(root)
                date_of_license_expiry_field = ttk.Entry(root)
                owner_nid_card_no_field = ttk.Entry(root)

                owner_nid_card_image_button = ttk.Button(
                    root, text="Select file", command=choose_image)

                # grid method is used for placing
                # the widgets at respective positions
                # in table like structure .
                owner_name_field.grid(row=1, column=1, ipadx="70")
                owner_contact_no_field.grid(row=2, column=1, ipadx="70")
                owner_email_id_field.grid(row=3, column=1, ipadx="70")
                date_of_license_expiry_field.grid(row=4, column=1, ipadx="70")
                owner_nid_card_no_field.grid(row=5, column=1, ipadx="70")
                owner_nid_card_image_button.grid(row=6, column=1)

                submit = ttk.Button(root, text="Submit", command=insert)
                submit.grid(row=8, column=2)

                # start the GUI
                root.mainloop()
            elif paid_due == "no":
                showerror(
                    title='Cannot register',
                    message='Sorry, cannot be registered into the system. Dues needed to be cleared'
                )
        else:
            showinfo(
                title='No data',
                message='Nothing to register'
            )

    # press 'c' to check if the detected number plate is registered or expired
    if keyboard.is_pressed("c"):
        if license_plate != '':
            record = get_car_data_from_license_info_table(license_plate)

            current_epoch_time = int(time.time())
            dt_object = datetime.datetime.fromtimestamp(current_epoch_time)

            date_time_formal = dt_object.strftime("%A, %d %B %Y at %I:%M %p")
            timestamp = dt_object.strftime("%Y-%m-%d %H:%M:%S")

            if len(record) != 0:
                showinfo(
                    title='Status',
                    message="License plate is Registered"
                )

                owner_name = record[0][2]
                owner_phone_number = record[0][3]
                owner_email = record[0][4]

                dt_object = datetime.datetime.fromtimestamp(epoch_time)
                expiry_dt_obj = datetime.datetime.strptime(
                    str(record[0][1]), "%Y-%m-%d %H:%M:%S")

                diff = dt_object - expiry_dt_obj
                diffMonths = diff.days // 30
                diffDays = diff.days % 30

                expiry_dt = int(expiry_dt_obj.timestamp())
                if epoch_time > expiry_dt:
                    showinfo(
                        title='Expiry',
                        message=f"License plate is expired by {diffMonths} months and {diffDays} days"
                    )
                    
                    date_time_formal = expiry_dt_obj.strftime(
                        "%A, %d %B %Y at %I:%M %p")

                    record = get_due_data_from_dues_table(license_plate)

                    fine_amount = 5000
                    fine_factor = 0

                    if(diffMonths >= 0 and diffMonths <= 1):
                        fine_factor = 1
                    if(diffMonths > 1 and diffMonths <= 2):
                        fine_factor = 2
                    elif(diffMonths > 2 and diffMonths <= 3):
                        fine_factor = 3
                    elif(diffMonths > 3 and diffMonths <= 4):
                        fine_factor = 4
                    elif(diffMonths > 4 and diffMonths <= 5):
                        fine_factor = 5
                    elif(diffMonths >= 5):
                        fine_factor = 5

                    if(len(record) == 0):
                        # create_dues_table()

                        times_fined_for_expiry = 1
                        times_fined_for_unregistered = 0

                        fined = fine_amount * fine_factor
                        amount_of_fine = fined

                        insert_data_into_dues_table(
                            license_plate, current_epoch_time, timestamp, amount_of_fine, times_fined_for_expiry, times_fined_for_unregistered)

                    else:
                        times_fined_for_expiry = record[0][2] + 1
                        times_fined_for_unregistered = 0

                        fined = fine_amount * fine_factor
                        amount_of_fine = record[0][1] + fined

                        modify_dues_table_data(
                            license_plate, current_epoch_time, timestamp, amount_of_fine, times_fined_for_expiry, times_fined_for_unregistered)

                        # 1 month eh 5k fine, 2 month 10k, 3 month 15k, 4 month 20k 5 month 25k
                        # for expiry increase fine by 5k for each successive offense and for 5th month and above keep 25k

                    print("Currently fined Tk.", fined)
                    
                    message = f"Hello {owner_name},\nYour car's license plate of\n{license_plate}expiry was on {date_time_formal} and it has been expired for {diffMonths} months and {diffDays} days. You have also been currently fined Tk. {fined} with a total fine of Tk. {amount_of_fine} and in total fined {times_fined_for_expiry} times. Please renew your license plate and pay the fine as soon as possible."

                    subject = "Fined for license plate expiry"

                    #send_whatsapp_message(owner_phone_number, message)
                    send_sms(owner_phone_number, message)
                    send_email_with_attachment(
                        owner_email, owner_name, subject, message, plate_image)
                    print(message)
                    showinfo(
                        title='Fined',
                        message=f"Currently fined Tk. {fined}\nTotal fine Tk. {amount_of_fine}\nTotal Fined {times_fined_for_expiry} times."
                    )

                else:
                    showinfo(
                        title='License Valid',
                        message="License is not expired"
                    )
            else:
                showinfo(
                        title='Status',
                        message="License Plate is not Registered"
                )

                record = get_due_data_from_dues_table(license_plate)
                if(len(record) == 0):
                    # create_dues_table()
                    amount_of_fine = 10000
                    currently_fined = amount_of_fine
                    times_fined_for_expiry = 0
                    times_fined_for_unregistered = 1
                    insert_data_into_dues_table(
                        license_plate, current_epoch_time, timestamp, amount_of_fine, times_fined_for_expiry, times_fined_for_unregistered)
                else:
                    currently_fined = 0
                    times_fined_for_expiry = 0
                    times_fined_for_unregistered = record[0][5] + 1
                    if(times_fined_for_unregistered < 5):
                        currently_fined = 10000 * times_fined_for_unregistered
                    else:
                        currently_fined = 50000

                    amount_of_fine = record[0][3] + currently_fined
                    modify_dues_table_data(
                        license_plate, current_epoch_time, timestamp, amount_of_fine, times_fined_for_expiry, times_fined_for_unregistered)

                # for unregistered increase fine by 10k for each successive offense and for 5th offence and above keep 50k

                subject = "License Plate fined for unregistered"

                message = f"Hello {sys_manager_name},\nThis is to let you know that the car with license plate\n{license_plate}is currently fined Tk. {currently_fined} on {date_time_formal} with a total fine of Tk. {amount_of_fine} and previously fined {times_fined_for_unregistered} times because the car is not registered. Please take necessary actions as soon as possible."

                #send_whatsapp_message(sys_manager_phone_number, message)
                send_sms(sys_manager_phone_number, message)
                send_email_with_attachment(
                    sys_manager_email, sys_manager_name, subject, message, plate_image)
                print(message)
                showinfo(
                        title='Fined',
                        message=f"Currently fined Tk. {currently_fined}\nTotal fine Tk. {amount_of_fine}\nTotal Fined {times_fined_for_unregistered} times."
                    )

        else:
            showerror(
                title='No data',
                message="Nothing to check"
            )

    # press 'e' to send bulk email of the detected number plate with plate image as attachment
    if keyboard.is_pressed("e"):
        if license_plate != '' and plate_image != '':
            dt_object = datetime.datetime.fromtimestamp(epoch_time)
            date_time_formal = dt_object.strftime("%A, %d %B %Y at %I:%M %p")

            attachment_file_name = str(epoch_time)+'.png'
            subject = "License Plate Detected"
            message = f"a license plate\n{license_plate}was detected on {date_time_formal}."

            send_bulk_email_with_template_and_attachment(
                "email contacts.txt", "email template.txt", plate_image, attachment_file_name, subject, message)
        else:
            showerror(
                title='Error',
                message="Nothing to send"
            )

    # press 'm' to generate money receipt of all dues and send bulk email
    if keyboard.is_pressed("m"):
        generate_money_receipt_and_send_bulk_mail()

    # press 'g' to run sftp server
    if keyboard.is_pressed("g"):
        if sys.platform == 'win32':
            run_sftp_server()

    # press 'q' to exit
    if keyboard.is_pressed("q"):
        print("Closing...")
        break
cv2.destroyAllWindows()