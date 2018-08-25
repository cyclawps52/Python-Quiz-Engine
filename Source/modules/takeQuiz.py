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
        