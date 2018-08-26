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
            lockPath = Path(quizPath + "\\" + quiz + "\\lock.lock")
        
            try:
                open(gradePath, "r")
                print(str(i) + ": " + quiz + " | GRADED")
            except:
                try:
                    open(resultPath, "r")
                    print(str(i) + ": " + quiz + " | NOT GRADED")
                except:
                    try:
                        open(lockPath, "r")
                        print(str(i) + ": " + quiz + " | LOCKED")
                    except:
                        print(str(i) + ": " + quiz + " | NOT TAKEN")
            i += 1

        line()
        selection = input("Selection: ")
        if(selection == "!!"):
            return
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
    selectedQuizDump = Path(quizPath + "\\" + selectedQuiz + "\\" + "dump.dump")

    clear()

    # graded quiz menu
    try:
        open(gradePath, "r")
        # see result or quiz dump
        while True:
            clear()
            print("1. See result for {0}".format(selectedQuiz))
            print("2. See quiz dump for {0}".format(selectedQuiz))
            selection = input("Selection: ")
            if(selection == "!!"):
                return
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
        
        # locked menu
        except:
            try:
                open(lockPath, "r")
                print("Your teacher has this quiz locked.")
                print("Press ENTER to exit quiz menu.")
                input()
                return

            # not taken, proceed to quiz engine
            except:
                takeQuiz(selectedQuizPath, resultPath)
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

def takeQuiz(filePath, resultPath):
    quizStream = open(filePath, "r")
    resultStream = open(resultPath, "w")

    # chop off beginning marker
    buffer = quizStream.readline()

    #get number of questions
    buffer = quizStream.readline()
    buffer = buffer.split(".")
    buffer.pop(0)
    numQs = int(buffer[0])
    correctCount = 0

    # loop for every question
    for i in range(1, numQs+1):
        clear()
        print("Question {0} of {1}".format(i, numQs))
        line()
        # get question text
        questionText = quizStream.readline()
        print(questionText[3:])

        # get possible answers
        buffer = quizStream.readline()
        answerNum = 1
        while(buffer[:1] is not 'C'):
            print("{0}: {1}".format(answerNum, buffer[3:-1]))
            answerNum += 1
            buffer = quizStream.readline()
        line()
        
        # get selected answer
        selectedAnswer = input("Choose an answer number: ")
        try:
            int(selectedAnswer)
        except:
            selectedAnswer = 0
        correctAnswer = int(buffer[3:])

        # write info to file
        resultStream.write("B:\n")
        resultStream.write("Q: {0}\n".format(i))
        if(int(selectedAnswer) == int(correctAnswer)):
            resultStream.write("C: 1\n")
            correctCount += 1
        else:
            resultStream.write("C: 0\n")
        resultStream.write("A: {0}\n".format(selectedAnswer))
        resultStream.write("X: {0}\n".format(correctAnswer))
        resultStream.write("E: \n")

        # chop off end of question flag
        buffer = quizStream.readline()

    # get flag information
    while(buffer[:1] is not 'F'):
        buffer = quizStream.readline()
    containsFlag = int(buffer[3:])

    #if flag is present
    if(containsFlag == 1):
        buffer = quizStream.readline()
        threshold = int(buffer[3:])
        if(correctCount >= threshold):
            flagBox = quizStream.readline()
            flagBox = flagBox[3:-1]
    
    # display information to user
    clear()
    print("Your score was: {0}/{1}".format(correctCount, numQs))
    print("This is a {0}%".format(correctCount / numQs * 100))
    if(containsFlag):
        if(correctCount >= threshold):
            line()
            print("You scored high enough to see the flag!")
            print("Flag: {0}".format(flagBox))
            line()
    
    print("Press ENTER to return to student menu.")
    input()
    return
