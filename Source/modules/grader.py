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
        print("{0} is already graded for this class.".format(selectedQuiz))
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

    # get number of questions in quiz
    quizStreamBuffer = quizStream.readline()

    #get number of questions
    quizStreamBuffer = quizStream.readline()
    quizStreamBuffer = quizStreamBuffer.split(".")
    quizStreamBuffer.pop(0)
    numQs = int(quizStreamBuffer[0])

    # create array to store results while grading
    w, h = 4, numQs+1;
    questionStats = [[0 for x in range(w)] for y in range(h)] 

    # get results directory
    resultsPath = Path(selectedQuizFolder + "\\results\\")
    numStudents = 0
    for file in os.listdir(resultsPath):
        filename = os.fsdecode(file)
        if(filename.endswith(".result")):
            # this loops through all .result files
            print("Now grading {0}!".format(filename))
            
            # get name of student
            studentName = os.path.basename(file)
            studentName = studentName[:-7]

            # open student grade filestream
            studentStreamPath = selectedQuizFolder + "\\grades\\" + studentName + ".grade"
            studentStream = open(studentStreamPath, "w")

            # open student results filestream
            studentResultStreamPath = selectedQuizFolder + "\\results\\" + studentName + ".result"
            studentResultStream = open(studentResultStreamPath, "r")

            # trim B: line off results
            buffer = studentResultStream.readline()

            # declaring needed counter variables
            studentCorrect = 0
            studentAverage = 0
            questionNum = 1

            # loop until EOF
            while True:
                buffer = studentResultStream.readline()
                if not buffer: # if nothing read
                    break

                if(buffer[0] == "Q"):
                    # get question number
                    questionNum = int(buffer[3:])
                    # write to table
                    questionStats[0][questionNum] = questionNum

                elif(buffer[0] == "C"):
                    # get answer status
                    questionStatus = int(buffer[3:])
                    if(questionStatus == 1):
                        questionStats[1][questionNum] += 1
                        studentStream.write("Question {0}: Correct!\n".format(questionNum))
                        # chop off expected and actual answer lines
                        buffer = studentResultStream.readline()
                        buffer = studentResultStream.readline()
                        studentCorrect += 1
                    else:
                        # get student answer and expected answer
                        buffer = studentResultStream.readline()
                        studentAns = int(buffer[3:])
                        buffer = studentResultStream.readline()
                        expectedAns = int(buffer[3:])
                        questionStats[2][questionNum] += 1
                        studentStream.write("Question {0}: Wrong! Expected {1} but got {2}.\n".format(questionNum, expectedAns, studentAns))  
                    studentStream.write("--------------------------------\n")
                
                else:
                    pass

            #print score and percent to individual file
            studentAverage = round(studentCorrect / numQs * 100, 2)
            studentStream.write("Score: {0} out of {1}\n".format(studentCorrect, numQs))
            studentStream.write("Percentage: {0}\n".format(studentAverage))

            #print user and percent to overall file
            overallStream.write("ID:{0} - {1}/{2} - {3}%\n".format(studentName, studentCorrect, numQs, studentAverage))

            numStudents += 1

    #calculate question averages
    for i in range(1, numQs+1):
        questionStats[3][i] = round(questionStats[1][i] / numStudents * 100, 2)

    #print questionStats to overall.grade in list format
    overallStream.write("--------------------\n")
    for i in range(1, numQs+1):
        overallStream.write("Question: {0}\n".format(questionStats[0][i]))
        overallStream.write("\tCorrect: {0}\n".format(questionStats[1][i]))
        overallStream.write("\tWrong: {0}\n".format(questionStats[2][i]))
        overallStream.write("\tPercent: {0}\n\n".format(questionStats[3][i]))

    #get total average
    classAverage = 0
    for i in range (1, numQs+1):
        classAverage += questionStats[3][i]
    classAverage /= numQs
    classAverage = round(classAverage, 2)
    from modules.custom import line
    line()
    print("Quiz average was {0}%.\n".format(classAverage))
    overallStream.write("--------------------\n")
    overallStream.write("Quiz average was: {0}%.\n".format(classAverage))

    #create test dump
    answerCount = 1
    questionCount = 1
    for line in quizStream:
        if(line[0] == "Q"):
            dumpStream.write("--------------------\n")
            answerCount = 1
            dumpStream.write("Question {0}: {1}".format(questionCount, line[3:]))
            questionCount += 1
        elif(line[0] == "A"):
            dumpStream.write("\t{0}: {1}".format(answerCount, line[3:]))
            answerCount += 1


    print("Finshed grading! Press ENTER to return to teacher menu.")
    input()
    return
