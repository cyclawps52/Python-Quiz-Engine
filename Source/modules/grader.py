# standard imports
from pathlib import Path
import os

# custom imports
from modules.custom import *
from modules.auth import *
from modules.classes import *

def gradeMenu(carryClass):
    carryClass = carryClass[1:]
    clear()
    # get all quizes for current class
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
            gradedPath = Path(quizPath + "\\" + quiz +"\\overall.grade")
            try:
                open(gradedPath, "r")
                print(str(i) + ": " + quiz + " | GRADED")
            except:
                print(str(i) + ": " + quiz + " | NOT GRADED")
            i += 1

        line()
        selection = input("Selection: ")
        try:
            selection = int(selection)
            if(selection >= 1 and selection <= i):
                break
            else:
                print("Invalid selection, press ENTER to retry.")
                input()
        except:
            print("Invalid selection, press ENTER to retry.")
            input()

    # get next function call from selection
    selectedQuiz = quizFolders[selection-1]
    gradedPath = Path(quizPath + "\\" + selectedQuiz + "\\overall.grade")
    selectedQuizPath = quizPath + "\\" + selectedQuiz + "\\" + selectedQuiz + ".quizfile"
    selectedQuizFolder = quizPath + "\\" + selectedQuiz + "\\"
    try:
        open(gradedPath, "r")
        print("{0} is already graded for this class.")
        print("Press ENTER to return to teacher menu.")
        input()
        return
    except:
        gradeQuiz(selectedQuizPath, selectedQuizFolder)
        return

def gradeQuiz(selectedQuizPath, selectedQuizFolder):
    # get generic file streams opened
    quizStream = open(selectedQuizPath, "r")
    overallStreamPath = selectedQuizFolder + "overall.grade"
    overallStream = open(overallStreamPath, "w")
    dumpStreamPath = selectedQuizFolder + "dump.dump"
    dumpStream = open(dumpStreamPath, "w")

    # get results directory
    resultsPath = Path(selectedQuizFolder + "\\results\\")
    for file in os.listdir(resultsPath):
        filename = os.fsdecode(file)
        if(filename.endswith(".results")):
            # this loops through all .results files
            
            # START GRADING HERE
            # OPEN INDIVIDUAL FILE STREAM
            # FILL OUT OVERALL FILE (UGH)
    
    # SHOW OVERALL STATS


    return