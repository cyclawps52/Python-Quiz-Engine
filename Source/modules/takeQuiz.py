# standard imports
from pathlib import Path
import os

# custom imports 
from modules.custom import *
from modules.auth import *
from modules.classes import *

def quizMenu(carryID, carryClass):
    clear()
    # get all quizes for current user in current class
    quizPath = str(os.getcwd() + "\\classes\\" + carryClass + "\\quizzes")
    filesList = os.listdir(quizPath)
    quizFolders = []
    for file in filesList:
        if Path(file).is_dir:
            quizFolders.append(file)

    # list status of all quizes
    while True:
        clear()
        i = 1
        for quiz in quizFolders:
            resultPath = Path(quizPath + "\\" + quiz + "\\results\\" + carryID + ".result")
            gradePath = Path(quizPath + "\\" + quiz + "\\grades\\" + carryID + ".grade")
        
            try:
                open(gradePath, "r")
                print(str(i) + ": " + quiz + " | GRADED")
            except:
                try:
                    open(resultPath, "r")
                    print(str(i) + ": " + quiz + " | NOT GRADED")
                except:
                    print(str(i) + ": " + quiz + " | NOT TAKEN")
            i += 1

        line()
        selection = input("Selection: ")
        try:
            selection = int(selection)
            if(selection >=1 and selection <=i):
                break
            else:
                print("Invalid selection, press ENTER to retry.")
                input()
        except:
            print("Invalid selection, press ENTER to retry.")
            input()

    # get next function call from selection
    selectedQuiz = quizFolders[selection-1]
    resultPath = Path(quizPath + "\\" + selectedQuiz + "\\results\\" + carryID + ".result")
    gradePath = Path(quizPath + "\\" + selectedQuiz + "\\grades\\" + carryID + ".grade")
    selectedQuizPath = Path(quizPath + "\\" + selectedQuiz + "\\" + selectedQuiz + ".quizfile")
    selectedQuizDump = Path(quizPath + "\\" + selectedQuiz + "\\" + selectedQuiz + ".quizdump")

    clear()

    # graded quiz menu
    try:
        open(gradePath, "r")
        # see result or quiz dump
        while True:
            print("1. See result for {0}".format(selectedQuiz))
            print("2. See quiz dump for {0}".format(selectedQuiz))
            selection = input("Selection: ")
            try:
                selection = int(selection)
            except:
                print("Invalid selection, press ENTER to retry.")
                input()
            if(selection == 1):
                viewer(gradePath)
                return
            elif(selection == 2):
                # view dump if it exists
                try:
                    open(selectedQuizDump, "r")
                    viewer(selectedQuizDump)
                    return
                except:
                    print("Your teacher has locked the quiz dump.")
                    print("Press ENTER to exit the quiz menu.")
                    input()
                    return
            else:
                print("Invalid selection, press ENTER to retry.")
                input()

        return

    # taken but not graded menu
    except:
        try:
            open(resultPath, "r")
            print("Your teacher has not graded " + selectedQuiz + ".")
            print("Press ENTER to exit quiz menu.")
            input()
            return

        # not taken, proceed to quiz engine
        except:
            takeQuiz(selectedQuizPath)
            return

def viewer(filePath):
    clear()
    f = open(filePath)
    content = f.read()
    print(content)
    line()
    print("Press ENTER to continue.")
    input()
    return

def takeQuiz(filePath):
    print("TAKING THINGY")
    return