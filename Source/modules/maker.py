# standard imports
from pathlib import Path

# custom imports
from modules.custom import *
from modules.auth import *
from modules.classes import *

def makeQuiz(carryID):
    # get list of classes to assign
    classList = classCheck(silent=1, username=carryID[0])
    includedList = []

    # create intial class list
    initialList = []
    for classCode in classList.split(','):
        try:
            if(classCode[0] == "$"):
                initialList.append(classCode[1:-1])
        except:
            continue
    notIncludedList = initialList

    while True:
        clear()
        # print classes not in selection list
        i = 0
        for entry in notIncludedList:
            print("A{0}: {1}".format(i, entry))
            i += 1
        line()

        # print classes in selection list
        i = 0
        print("Classes to add quiz to:")
        for entry in includedList:
            print("R{0}: {1}".format(i, entry))
            i += 1
        line()

        print("QQ: CONFIRM SELECTION")
        classChoice = input("Selection: ").upper()
        if(classChoice == "QQ"):
            if(len(includedList) == 0):
                print("You must assign the quiz to at least one class.")
                print("Press ENTER to retry.")
                input()
            else:
                break
        elif(classChoice[0] == "A"):
            classInt = int(classChoice[1:])
            classChoice = notIncludedList[classInt]
            includedList.append(classChoice)
            notIncludedList.pop(classInt)
        elif(classChoice[0] == "R"):
            classInt = int(classChoice[1:])
            classChoice = includedList[classInt]
            notIncludedList.append(classChoice)
            includedList.pop(classInt)
        else:
            print("Invalid selection, press ENTER to try again.")
            input()

    # get quiz name
    while True:
        clear()
        quizName = input("Name for quiz: ")
        if(len(quizName) == 0):
            print("Quiz name cannot be empty. Press ENTER to retry.")
            input()
        else:
            break


    # open files for all classes
    i = 0
    quizFiles = []
    for classCode in includedList:
        classPath = Path(str(os.getcwd() + "\\Source\\\\classes\\" + classCode + "\\quizzes\\"))
        os.chdir("Source")
        os.chdir("classes")
        os.chdir(classCode)
        os.chdir("quizzes")
        try:
            make_directory(quizName)
        except:
            print("Class {0} already has a quiz named {1}".format(classCode, quizName))
            print("Aborting creation procedure for all classes. Press ENTER to continue.")
            input()
            return
        os.chdir(quizName)
        quizFiles.append(open("{0}.quiz".format(quizName), "w"))
        os.chdir("../")
        os.chdir("../")
        os.chdir("../")
        os.chdir("../")
        os.chdir("../")
        i += 1

    # write beginning mark for all files
    for file in quizFiles:
        file.write("B: \n")

    # Number of questions
    while True: # get num Qs until valid
        clear()
        numQs = input("How many questions (max 99): ")
        try:
            numQs = int(numQs)
            if(numQs <= 99):
                break
            else:
                print("Not a valid option, press ENTER to try again.")
                input()
        except:
            print("Not a valid option, press ENTER to try again.")
            input()
    # write number of questions
    for file in quizFiles:
        file.write("N. {0}\n".format(numQs))

    # get questions
    for i in range(1, numQs+1):
        clear()
        print("Please enter question #{0} of {1}".format(i, numQs))
        question = input("")
        # write question to all files
        for file in quizFiles:
            file.write("Q. {0}\n".format(question))
    
        # get number of answers
        while True: # get num As until valid
            clear()
            numAs = input("How many answers (max 99): ")
            try:
                numAs = int(numAs)
                if(numAs <= 99):
                    break
                else:
                    print("Not a valid option, press ENTER to try again.")
                    input()
            except:
                print("Not a valid option, press ENTER to try again.")
                input()
        # get answers
        line()
        for j in range(1, numAs+1):
            print("Option #{0} for question {1}".format(j, i))
            answer = input("")
            # write answer to all files
            for file in quizFiles:
                file.write("A. {0}\n".format(answer))
        # get correct answer
        line()
        correctAs = int(input("Which option # is the correct answer: "))
        # write correct answer and end of question mark to all files
        for file in quizFiles:
            file.write("C: {0}\n".format(correctAs))
            file.write("E: \n")

    # get flag information
    clear()
    print("Would you like to have a flag displayed if the score is over a certain amount?")
    flagChoice = input("1==yes, 0==no: ")
    if(flagChoice == "1"): # write flag
        for file in quizFiles:
            file.write("F: 1\n")
        line()
        print("What is the minimum amount of questions the user must get right?")
        print("Number between 0 and {0}".format(numQs))
        flagMin = int(input("Choice: "))
        if(flagMin > numQs):
            print("Choice must be below the number of questions, defaulting to zero.")
            for file in quizFiles:
                file.write("V: 0\n")
        elif(flagMin < 0):
            print("Choice must be above zero, defaulting to zero.")
            for file in quizFiles:
                file.write("V: 0\n")
        else:
            for file in quizFiles:
                file.write("F: {0}\n".format(flagMin))
        line()
        flagBox = input("What is the flag: ")
        for file in quizFiles:
            file.write("T: {0}\n".format(flagBox))
    elif(flagChoice == "0"): # no flag
        for file in quizFiles:
            file.write("F: 0\n")
    else:
        print("Not a valid option, defaulting to no flag.")
        for file in quizFiles:
            file.write("F: 0\n")
    
    # print end mark to quiz file
    for file in quizFiles:
        file.write("EEE")
    
    clear()
    print("Test file created and saved as: {0}".format(quizName))
    print("Press ENTER to close Maker")
    input()

	# close all file pointers
    for file in quizFiles:
        file.close()

    return
