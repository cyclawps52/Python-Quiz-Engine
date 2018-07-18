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
from modules.auth import *


def classCheck(silent=0, username="NULL"):
    clear()
    db, dbCursor = connectToDatabase()

    if(username=="NULL"):
        username = input("Username to check: ")
    dbAccount = dbCursor.execute("SELECT * FROM users WHERE username=?", [(username)])
    dbAccount = dbCursor.fetchall()

    try: # see if account exists
        account = dbAccount[0]
    except:
        print("User {0} not found. Press ENTER to return to main menu.".format(username))
        input()
        return 1
    
    #get classes and split string
    classList = account[3]
    if(not bool(silent)):
        i = 0
        menu = {}
        for classCode in classList.split(','):
            menu[i] = classCode[:-1]
            i += 1
        menu.pop(0)
        options = menu.keys()
        for entry in options:
            if(menu[entry][0] == "$"):
                print("{0}: {1} | TEACHER MODE ENABLED".format(entry, menu[entry][1:]))
            else:
                print("{0}: {1}".format(entry, menu[entry]))
        input()

    return classList

def classRegister():
    clear()

    username = input("Username to enroll: ")
    classList = classCheck(silent=1, username=username)
    if(classList == 1):
        return
    
    toRegister = input("Class code to add: ")

    # check if user is in class
    if str("," + toRegister + "!") in classList or str(",$" + toRegister + "!") in classList:
        print("User \"{0}\" is already enrolled in \"{1}\". Press ENTER to return to main menu.".format(username, toRegister))
        input()
        return

    classPath = Path(str(os.getcwd() + "\\Source\\\\classes\\" + toRegister + "\\"))
    if(classPath.is_dir()):
        # class is valid

        #check if user will be teaching the class
        classTeacherFlag = int(input("Will {0} be teaching {1} (1=yes, 0=no): ".format(username, toRegister)))
        if(classTeacherFlag == 1):
            toRegister = "$" + toRegister
        elif(classTeacherFlag == 0):
            pass
        else:
            classTeacherFlag = 0
            print("Invalid option, defaulting to student. Press ENTER to continue.")
            input()

        db, dbCursor = connectToDatabase()
        classList += str("," + toRegister + "!")
        dbCursor.execute("UPDATE users SET classCodes=? WHERE username=?", [(classList), (username)])
        db.commit()
        db.close()
        if(classTeacherFlag == 1):
            print("User {0} registered for {1} as teacher. Press ENTER to return to main menu.".format(username, toRegister[1:]))
        else:
            print("User {0} registered for {1}. Press ENTER to return to main menu.".format(username, toRegister))
        input()
        return

    else:
        # class is not valid
        print("Class code not found! Press ENTER to return to main menu.")
        input()
        return

def classDrop():
    clear()

    username = input("Username to drop: ")
    classList = classCheck(silent=1, username=username)
    if(classList == 1):
        return

    while True: # Remain in drop mode until exit is selected
        goToDrop = False
        invalidSelection = False

        # get updated class list and update menu
        classList = classCheck(silent=1, username=username)
        i = 0
        menu = {}
        for classCode in classList.split(','):
            menu[i] = classCode[:-1]
            i += 1
        menu.pop(0)
        options = menu.keys()

        clear()
        print("User \"{0}\" is registered for the following classes:".format(username))
        for entry in options:
            if(menu[entry][0] == "$"):
                print("{0}: {1} | TEACHER MODE ENABLED".format(entry, menu[entry][1:]))
            else:
                print("{0}: {1}".format(entry, menu[entry]))
        print("0: Return to Main Menu")
        line()
        try:
            selection = int(input("Selection: "))
        except:
            print("Invalid selection. Press ENTER to try again.")
            input()
            invalidSelection = True

        if(invalidSelection == False):
            if(selection == 0): # exits if chosen
                return

            # selection validation
            try:
                toDrop = menu[selection]
                goToDrop = True  
            except:
                print("Invalid selection. Press ENTER to try again.")
                input()
                invalidSelection = True

            if(goToDrop): # if the selection was valid
                # drop the class
                db, dbCursor = connectToDatabase()
                
                toDrop = "," + toDrop + "!"
                classList = classList.replace(toDrop, "")

                dbCursor.execute("UPDATE users SET classCodes=? WHERE username=?", [(classList), (username)])
                db.commit()
                db.close()

                print("User \"{0}\" dropped \"{1}\". Press ENTER to continue.".format(username, toDrop.replace(',', '').replace('!','').replace('$','')))
                input()

def classCreate(toCreate="NULL"):
    clear()
    
    while True:  # get class name until not blank, no commas, and no exclamation points
        clear()
        if(toCreate == "NULL"):
            toCreate = input("Class code to create: ")
        if(len(toCreate) == 0):
            print("Class name cannot be empty. Press ENTER to try again.")
            input()
        if("," in toCreate or "!" in toCreate or "$" in toCreate):
            print("Class name cannot contain \' or ! or $. Press ENTER to try again.")
            input()
        else:
            break
    
    classPath = Path(str(os.getcwd() + "\\Source\\\\classes\\" + toCreate + "\\"))
    if(classPath.is_dir()):
        # class is already made
        print("Class code \"{0}\" already exists. Press ENTER to continue.")
        input()
        return

    else:
        # class does not exist, create
        os.chdir("Source")
        os.chdir("classes")
        make_directory(toCreate)
        os.chdir("../")
        os.chdir("../")
        print("Class \"{0}\" created. Press ENTER to exit class creation.".format(toCreate))
        input()
        return
