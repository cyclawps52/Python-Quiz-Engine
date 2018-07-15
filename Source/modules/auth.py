# standard imports
import os
import sqlite3
from pathlib import Path
import getpass
import hashlib
import uuid
import importlib.util
# custom imports
from modules.custom import *

# global variables
global db, dbCursor

def debugDumpDatabase():
    clear()
    db, dbCursor = connectToDatabase()
    for user in dbCursor.execute("SELECT rowid, * FROM users"):
	    print(user)
    db.close()
    print("\nPress ENTER to continue.")
    input()
    return


def connectToDatabase():
    """
    call as 'db, dbcursor = connectToDatabase()'
    """
    # carry through global variables
    global db, dbCursor

    pathToDatabase = str(os.getcwd() + "\\Source\\database\\auth.db")
    try:
        db = sqlite3.connect(pathToDatabase)
    except:
        checkIfFirstRun()
    dbCursor = db.cursor()
    return db, dbCursor

def checkIfFirstRun():
    # carry through global variables
    global db, dbCursor

    pathToDatabase = str(os.getcwd() + "\\Source\\database\\auth.db")
    # check if database needs to be created
    my_file = Path(pathToDatabase)
    if my_file.is_file():
        # file exists
        db = sqlite3.connect(pathToDatabase)
        dbCursor = db.cursor()
        # now connected to database

        # make sure database is not empty
        checkAccount = dbCursor.execute("SELECT * FROM users WHERE username=?", [("checkUser")])
        checkAccount = dbCursor.fetchall()
        try:
            checkPass = checkAccount[0][0]
        except:
            clear()
            print("ERROR: Setup is corrupted. Please delete the /database and /classes directories and rerun the program.")
            print("Please note this will erase all users, quizes, and grades from the system if they exist.")
            print("Press ENTER to exit program.")
            input()
            quit(1)
        
    else:
        # file does not exist, entering setup
        os.chdir("Source")
        make_directory("database")
        os.chdir("../")

        db = sqlite3.connect(pathToDatabase) # creates database file
        dbCursor = db.cursor() # creates database connection

        # create table setup
        dbCursor.execute("""
            CREATE TABLE users
            (username text, password text, isTeacher int, classCodes text)
            """)
        db.commit()
        # database is now created

        # create initial teacher account
        clear()
        print("FIRST TIME SETUP")
        line()
        while True: # get username until not blank
            clear()
            print("FIRST TIME SETUP")
            line()
            username = input("Enter a username for the default teacher account: ")
            if(len(username)==0):
                print("Username cannot be empty. Press ENTER to try again.")
                input()
            else:
                break
        while True: # get passwords until they match
            while True: # get first password until empty
                clear()
                print("FIRST TIME SETUP")
                line()
                password = getpass.getpass("Enter new password for {0}: ".format(username))
                if(len(password)==0):
                    print("Password cannot be empty. Press ENTER to try again.")
                    input()
                else:
                    break
            password2 = getpass.getpass("Comfirm new password for {0}: ".format(username))
            if(password == password2):
                break # passwords match
            else:
                print("Passwords did not match, press ENTER to try again.")
                input()

        # hash password to store in database
        hashedPassword = hashlib.sha512(password.encode('utf-8')).hexdigest()

        while True:  # get class name until not blank, no commas, and no exclamation points
            clear()
            print("FIRST TIME SETUP")
            line()
            initialClass = input("Enter a name for the first class: ")
            if(len(initialClass) == 0):
                print("Class name cannot be empty. Press ENTER to try again.")
                input()
            if("," in initialClass or "!" in initialClass):
                print("Class name cannot contain \' or !. Press ENTER to try again.")
                input()
            else:
                break
        
        # create initial class folder
        os.chdir("Source")
        make_directory("classes")
        os.chdir("classes")
        make_directory(initialClass)
        os.chdir("../")
        os.chdir("../")
        
        # add teacher to database
        newUser = [(username, hashedPassword, 1, str("," + initialClass + "!"))]
        dbCursor.executemany("INSERT INTO users VALUES(?,?,?,?)", newUser)
        db.commit()

        # add database completion check
        checkUser = [('checkUser', 'SuperSecurePassword', '0', ',TEST101!,TEST202!,TEST303!,TEST404!')]  # creating setup completed user
        dbCursor.executemany("INSERT INTO users VALUES(?,?,?,?)", checkUser)
        db.commit()
   
    return -1

def login(carryID):

    attempts = 0
    while (attempts < 3): # repeat until logged in or three incorrect tries
        accountLookupFailed = False
        clear()
        username = input("Username: ")
        password = getpass.getpass()

        dbAccount = dbCursor.execute("SELECT * FROM users WHERE username=?", [(username)])
        dbAccount = dbCursor.fetchall()

        # check if account exists
        try:
            dbUsername = dbAccount[0][0]
        except:  # no user found with given username
            accountLookupFailed = True
            attempts = attempts + 1
            if(attempts < 3):
                print("Invalid username/password combination!")
                if(attempts == 2):
                    ocdText = "attempt"
                else:
                    ocdText = "attempts"
                print("Press ENTER to try again ({0} {1} until returned to main menu).".format(3 - attempts, ocdText))
                input()
        
        # check if user is the checkUser and display easter egg
        if(username == "checkUser"):
            clear()
            print("01000101 01111000 01100011 01110101 01110011 01100101 00100000 01101101 01100101 00101100 00100000")
            print("01101000 01100101 01110010 01100101 00100111 01110011 00100000 01111001 01101111 01110101 01110010")
            print("00100000 01101110 01101111 01110011 01100101 00101110 00100000 01001001 00100000 01100110 01101111")
            print("01110101 01101110 01100100 00100000 01101001 01110100 00100000 01101001 01101110 00100000 01101101")
            print("01111001 00100000 01100010 01110101 01110011 01101001 01101110 01100101 01110011 01110011 00101110")
            print("\t\tERROR: Access to \"checkUser\" is disabled for security purposes.")
            print("\t\t\t Nice attempt at beating the system though  ;)")
            print("\t\t\t    Press ENTER to return to the main menu.")
            print("01010011 01110100 01100001 01111001 00100000 01101111 01110101 01110100 00100000 01101111 01100110")
            print("00100000 01101101 01111001 00100000 01100011 01101111 01100100 01100101 00100000 01100110 01110010")
            print("01101111 01101101 00100000 01101110 01101111 01110111 00100000 01101111 01101110 00100000 01101101")
            print("01101011 01100001 01111001 00100000 01110100 01101000 01100001 01101110 01101011 01110011 00100000")
            print("00101101 01000011 01111001 01100011 01101100 01100001 01110111 01110000 01110011 00110101 00110010")
            input()
            return -1

        if(not accountLookupFailed): # skips code if account was not found
            # user found, continuing
            dbPassword = dbAccount[0][1]
            dbIsTeacher = bool(dbAccount[0][2])

            #hash given password to see if it matches database
            hashedPassword = hashlib.sha512(password.encode('utf-8')).hexdigest()

            if(dbPassword == hashedPassword):  # passwords match
                carryID[0] = username  # updates currently logged on user
                print("Logged in!")
                if(dbIsTeacher):
                    print("Teacher mode enabled!")
                    return 1 # logged in, activate teacher mode
                return 0 # logged in, activate student mode

            else:  # passwords did not match
                attempts = attempts + 1
                if(attempts < 2):
                    print("Invalid username/password combination!")
                    if(attempts == 2):
                        ocdText = "attempt"
                    else:
                        ocdText = "attempts"
                    print("Press ENTER to try again ({0} {1} until returned to main menu).".format(3 - attempts, ocdText))
                    input()

    clear()
    print("Three failed attempts, press ENTER to return to main menu.")
    input()
    return -1
