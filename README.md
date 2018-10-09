# Python Quiz Engine

This project consists of five modules: 

 1. Authentication
 2. Classes
 3. Grader
 4. Maker
 5. Taker

## Authenticatiom

The authentication module uses a SQLite backend to create users. The database holds their username, hashed password, and a string that lists the classes they are enrolled in (including teacher status for every class).
Functions included:

* connectToDatabase (for getting database cursors in other modules)
* checkIfFirstRun (first time setup)
* login (proper authentication)
* changeClass (to ensure the student is enrolled in the class they want to view)
* addUser (creating new users and ensuring they are added to at least one class)

[The source code for the authentication module can be found here.](https://github.com/cyclawps52/Python-Quiz-Engine/blob/master/Source/modules/auth.py)

## Classes

The classes module controls the various class folders that are expanded into mini versions of the original quiz engine. Teachers can create classes and add or drop students to said classes. Students also have the ability to control their own class schedules.

Functions included:

* classCheck (for getting lists of classes to other functions such as login)
* classRegister (adding a class to a user)
* classDrop (removing a class from a user)
* classCreate (creating a new class folder)

[The source code for the classes module can be found here.](https://github.com/cyclawps52/Python-Quiz-Engine/blob/master/Source/modules/classes.py)


## Grader
The quiz grader will generate individual grade files as well as an overall file for the selected quiz. It will create a subdirectory inside the grades/ folder per quiz. 

The individual grade file will display whether the student got the question right or wrong. If wrong, the file will display what answer was expected as well as the user's inputted answer. The student grade files will also display the questions and answers so the student can recall what the quiz was.

The overall grade file will display all user IDs with their scores displayed as straight numbers as well as percentages. At the end of the file, a table will be outputted with statistics per question. This table includes how many students got the question right, wrong, and the percentage correct for each question. The file will also include the total quiz average across all students.

The grader also outputs a file with the questions and answers from the quiz. This can be used if the teachers or students wants to read the quiz in an easier format.

Functions included:

* gradeMenu (shows teachers which quizzes require grading)
* gradeQuiz (actually grading the quizzes)
* gradedQuizMenu (options for already-graded quizzes)
* deleteQuiz (removing all aspects of quizzes)
* lockQuiz (toggles the locked status for the given quiz)

[The source code for the grader module can be found here.](https://github.com/cyclawps52/Python-Quiz-Engine/blob/master/Source/modules/classes.py)

## Maker

The maker module allows teachers to easily create multiple-choice quizzes for the students to take. It walks through the entire process step by step, even allowing the teacher to add the quiz to multiple classes at once. Additionally, it will prompt the teacher for an optional flag if a student scores high enough.

By default, quizzes will start locked and must be unlocked from the teacher menu in order for them to become accessible by the students.

Functions included:

* makeQuiz (step by step quiz creation engine)

[The source code for the maker module can be found here.](https://github.com/cyclawps52/Python-Quiz-Engine/blob/master/Source/modules/maker.py)

## Taker

The taker module allows students to take a given quiz in a distraction-free environment. It will automatically pull the questions and answers from the given quiz format file and grade while the student answers, allowing for an instant result upon completion. In addition, it will also display a flag if the student's score is high enough.

Functions included:

* quizMenu (shows the students which quizzes need to be taken, are awaiting grades, or are graded)
* viewer (allows students to view grade files or test dumps)
* takeQuiz (distraction free quiz taking platform)

[The source code for the taker module can be found here.](https://github.com/cyclawps52/Python-Quiz-Engine/blob/master/Source/modules/takeQuiz.py)
