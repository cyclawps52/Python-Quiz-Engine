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
from modules.classes import *

# global variables
global db, dbCursor

def connectToDatabase():
    # carry through global variables
    global db, dbCursor

    pathToDatabase = Path(os.path.join(os.getcwd(), "database", "auth.db"))
    try:
        db = sqlite3.connect(pathToDatabase)
    except:
        # couldn't connect to db, is it made alrady?
        checkIfFirstRun()
    dbCursor = db.cursor()
    return db, dbCursor

def checkIfFirstRun():
    # carry through global variables
    global db, dbCursor

    pathToDatabase = os.path.join(os.getcwd(), "database", "auth.db")
    # check if database needs to be created
    my_file = Path(pathToDatabase)
    if my_file.is_file():
        # file exists
        db, dbcursor = connectToDatabase()
        # now connected to database, just make sure it isn't empty
        checkAccount = dbCursor.execute("SELECT * FROM users WHERE username=?", [("checkUser")])
        checkAccount = dbCursor.fetchall()
        try:
            checkPass = checkAccount[0][0]
        except:
            # check user didn't exist, database probably is corrupted
            clear()
            print("ERROR: Setup is corrupted. Please delete the /database and /classes directories and rerun the program.")
            print("Please note this will erase all users, quizes, and grades from the system if they exist.")
            print("Press ENTER to exit program.")
            input()
            quit(1)
        
    else:
        # file does not exist, entering setup
        make_directory("database")
        print(pathToDatabase)

        db, dbcursor = connectToDatabase()

        # create table setup
        dbCursor.execute(
            """
            CREATE TABLE users
            (username text, password text, classCodes text)
            """
        )
        db.commit()
        # database is now created

        # create initial teacher account
        clear()
        print("FIRST TIME SETUP")
        line()
        print("This setup will generate a default teacher account as well as a starting class.")
        print("This teacher user can create other teachers and students.")
        print("Please ensure this application is being set up by an authorized user and not a student.")
        print("Press ENTER to continue.")
        line()
        input()
        while True: 
            # get username until not blank
            clear()
            print("FIRST TIME SETUP")
            line()
            username = input("Enter a username for the default teacher account: ").upper()
            if(len(username)==0):
                print("Username cannot be empty. Press ENTER to try again.")
                input()
            else:
                break
        while True: 
            # get passwords until they match
            while True: 
                # get first password until not empty
                clear()
                print("FIRST TIME SETUP")
                line()
                password = getpass.getpass("Enter new password for \"{0}\": ".format(username))
                if(len(password)==0):
                    print("Password cannot be empty. Press ENTER to try again.")
                    input()
                else:
                    break
            password2 = getpass.getpass("Comfirm new password for \"{0}\": ".format(username))
            if(password == password2):
                # passwords match
                break 
            else:
                print("Passwords did not match, press ENTER to try again.")
                input()

        # hash password to store in database
        hashedPassword = hashlib.sha512(password.encode('utf-8')).hexdigest()

        while True:  
            # get class name until not blank, no commas, and no exclamation points
            clear()
            print("FIRST TIME SETUP")
            line()
            initialClass = input("Enter a name for the first class: ").upper()
            if(len(initialClass) == 0):
                print("Class name cannot be empty. Press ENTER to try again.")
                input()
            if("," in initialClass or "!" in initialClass or "$" in initialClass):
                print("Class name cannot contain , or ! or $. Press ENTER to try again.")
                input()
            else:
                print("Class code \"{0}\" will be created and \"{1}\" will be added as a teacher.".format(initialClass, username))
                print("Press ENTER to continue.")
                input()
                break
        
        # create initial class folder
        make_directory("classes")
        os.chdir("classes")
        make_directory(initialClass)
        os.chdir(initialClass)
        make_directory("quizzes")
        os.chdir("../")
        os.chdir("../")
        
        # add teacher to database
        newUser = [(username, hashedPassword, str(",$" + initialClass + "!"))]
        dbCursor.executemany("INSERT INTO users VALUES(?,?,?)", newUser)
        db.commit()

        # add database completion check
        checkUser = [('checkUser', 'SuperSecurePassword', ',$TEST101!,TEST202!,TEST303!,$TEST404!')]  # creating setup completed user
        dbCursor.executemany("INSERT INTO users VALUES(?,?,?)", checkUser)
        db.commit()
   
    return -1

def login(carryID, carryClass):
    db, dbCursor = connectToDatabase()

    clear()
    username = input("Username: ").upper()
    password = getpass.getpass()

    dbAccount = dbCursor.execute("SELECT * FROM users WHERE username=?", [(username)])
    dbAccount = dbCursor.fetchall()

    # check if account exists
    try:
        dbUsername = dbAccount[0][0]
    except:  
        # no user found with given username
        print("Invalid username/password combination!")
        print("Press ENTER to return to main menu.")
        input()
        return -1
    # user found, continuing
    dbPassword = dbAccount[0][1]

    #hash given password to see if it matches database
    hashedPassword = hashlib.sha512(password.encode('utf-8')).hexdigest()
    if(dbPassword == hashedPassword):  
        # passwords match, update currently logged on user
        carryID[0] = username
        
        # get class to login to
        from modules.classes import classCheck
        classList = classCheck(silent=1, username=username)
        if(classList == ""): 
            # no classes registered
            print("User \"{0}\" is not registered for any classes.".format(username))
            print("Press ENTER to register for a class.")
            input()
            from modules.classes import classRegister
            classRegister(student=1, username=username)

        while True:
            # loop until a valid class is chosen from the list
            validChoice = False
            classList = classCheck(silent=1, username=username)
            i = 0
            menu = {}
            for classCode in classList.split(','):
                menu[i] = classCode[:-1]
                i += 1
            menu.pop(0)
            options = menu.keys()

            if(len(menu) == 1): 
                # only one class, login to it
                classChoice = menu[1]
                carryClass[0] = classChoice
                break
            else:
                clear()
                print("Please select a class to login to: ")
                line()
                for entry in options:
                    # check if this entry is for a class the user is teaching
                    if(menu[entry][0] == "$"):
                        print("{0}: {1} | TEACHER MODE ENABLED".format(entry, menu[entry][1:]))
                    else:
                        print("{0}: {1}".format(entry, menu[entry]))
                try:
                    classChoice = int(input("Selection: "))
                except:
                    print("Invalid selection. Press ENTER to try again.")
                    input()
                try:
                    classChoice = menu[classChoice]
                    validChoice = True
                except:
                    print("Invalid selection. Press ENTER to try again.")
                    input()
                if(validChoice):
                    carryClass[0] = classChoice
                    break

        # select correct return value to determine teacher status
        if(carryClass[0][0] == "$"):
            isTeacher = True
        else:
            isTeacher = False
            
        # return permission level
        if(isTeacher):
            # activate teacher mode
            return 1
        return 0

    else:
        # password entry was not correct
        print("Invalid username/password combination!")
        print("Press ENTER to return to main menu.")
        input()
        return -1

def changeClass(carryID, carryClass):
    while True:
        # loop until a valid class is chosen from the list
        validChoice = False
        from modules.classes import classCheck
        classList = classCheck(silent=1, username=carryID)
        i = 0
        menu = {}
        for classCode in classList.split(','):
            menu[i] = classCode[:-1]
            i += 1
        menu.pop(0)
        options = menu.keys()
        clear()
        print("Please select a class to login to: ")
        line()
        for entry in options:
            # check if this entry is for a class the user is teaching
            if(menu[entry][0] == "$"):
                if(menu[entry] == carryClass):
                    print("{0}: {1} | TEACHER MODE ENABLED | (current class)".format(entry, menu[entry][1:]))
                else:
                    print("{0}: {1} | TEACHER MODE ENABLED".format(entry, menu[entry][1:]))
            else:
                if(menu[entry] == carryClass):
                    print("{0}: {1} | (current class)".format(entry, menu[entry]))
                else:
                    print("{0}: {1}".format(entry, menu[entry]))
        try:
            classChoice = int(input("Selection: "))
        except:
            print("Invalid selection. Press ENTER to try again.")
            input()
        try:
            classChoice = menu[classChoice]
            validChoice = True
        except:
            print("Invalid selection. Press ENTER to try again.")
            input()
        if(validChoice):
            carryClass = classChoice
            break

    if(carryClass[0][0] == "$"):
        isTeacher = True
    else:
        isTeacher = False
        
    # return permission level
    if(isTeacher):
        # activate teacher mode
        return 1, carryClass
    return 0, carryClass

def addUser(adminUsername="NULL"):
    db, dbCursor = connectToDatabase()
    while True:  
        # get username until not blank and not in database
        clear()
        username = input("Enter a username for the new account: ").upper()
        if(username == "!!"):
            return
        if(len(username) == 0):
            print("Username cannot be empty. Press ENTER to try again.")
            input()
        else:
            dbAccount = dbCursor.execute("SELECT * FROM users WHERE username=?", [(username)])
            dbAccount = dbCursor.fetchall()
            try:
                dbUsername = dbAccount[0][0]
                print("User \"{0}\" already exists. Press ENTER to try again.".format(username))
                input()
            except:  
                # no user found with given username
                break

    while True: 
        # get passwords until they match
        while True: 
            # get first password until empty
            clear()
            password = getpass.getpass("Enter new password for \"{0}\": ".format(username))
            if(len(password)==0):
                print("Password cannot be empty. Press ENTER to try again.")
                input()
            else:
                break
        password2 = getpass.getpass("Comfirm new password for \"{0}\": ".format(username))
        if(password == password2):
            # passwords match
            break 
        else:
            print("Passwords did not match, press ENTER to try again.")
            input()

    while True: 
        # get class until valid
        clear()
        initialClass = input("Enter a class to add new user \"{0}\" to: ".format(username)).upper()
        classPath = Path(os.path.join(os.getcwd(), "classes", initialClass))
        if(classPath.is_dir()):
            # class exists
            classTeacherFlag = int(input("Will \"{0}\" be teaching \"{1}\" (1=yes, 0=no): ".format(username, initialClass)))
            if(classTeacherFlag == 1):
                initialClass = "$" + initialClass
            elif(classTeacherFlag == 0):
                pass
            else:
                classTeacherFlag = 0
                print("Invalid option, defaulting to student. Press ENTER to continue.")
                input()
            break
        else:
            # class does not exist, create it
            while True: 
                # until class name is valid
                clear()
                print("Class code \"{0}\" does not exist, entering class creation...".format(initialClass))
                line()
                if("," in initialClass or "!" in initialClass or "$" in initialClass):
                    print("Class name cannot contain \' or ! or $. Press ENTER to rename class.")
                    input()
                    initialClass = input("Enter a class to add new user \"{0}\" to: ".format(username)).upper()
                else:
                    from modules.classes import classCreate
                    clear()
                    classCreate(toCreate=initialClass, username=adminUsername)
                    break

    # hash password to store in database
    hashedPassword = hashlib.sha512(password.encode('utf-8')).hexdigest()

    # add user to database
    newUser = [(username, hashedPassword, str("," + initialClass + "!"))]
    dbCursor.executemany("INSERT INTO users VALUES(?,?,?)", newUser)
    db.commit()

    clear()
    if(classTeacherFlag == 0):
        print("User \"{0}\" created and added to \"{1}\"! Press ENTER to exit user creation.".format(username, initialClass))
    else:
        print("User \"{0}\" created and added to \"{1}\" as a teacher! Press ENTER to exit user creation.".format(username, initialClass))
    input()
    return
