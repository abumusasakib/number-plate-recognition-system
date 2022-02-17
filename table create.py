import mysql.connector  # mysql-connector-python

# date and time modules
import time

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


create_plate_table()
create_license_info_table()
create_dues_table()