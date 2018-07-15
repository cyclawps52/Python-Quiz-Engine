#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <dirent.h>

#include "../custom/custom.h"
#include "grader.h"

int grader()
{
    clear();
    
	//variables used for directory reading
	DIR* FD;
    struct dirent* in_file;
    FILE* master_results;
    FILE* current_file;
    char buffer[250];
    FILE* quiz;

    //track number of student files ran through
    int numStudents=0;

    //get name of quiz to run
    char quizName[140]="quizes/";
    char temp[100];
    printf("What quiz do you want to grade(100 char max): ");
    //scanf("%s", temp);
    fflush(stdin);
    fgets(temp, 100, stdin);
    line();
    strcat(quizName, temp);

    //check if choice is empty
    if(strcmp(temp, "\n") == 0)
    {
        printf("Quiz name cannot be empty!\n");
        pete();
        return 1;
    }

    //add .quizfile extension to string
    strtok(quizName, "\n");
    strcat(quizName, ".quizfile");

    //opening quiz file stream r
    quiz = fopen(quizName, "r+");
    if(quiz==NULL)
    {
        printf("There was an error opening the quiz file.\n");
        printf("Press ENTER to close Grader.\n");
        fflush(stdin);
        getchar();
        return 1;
    }

    //get number of questions in quiz
    int numQs;
    char buffer2[225];
    fseek(quiz, 3, SEEK_SET);
    fgets(buffer2, 225, quiz);
    numQs = atoi(buffer2);

    //create array to store question statistics and fill with 0s
    float questionStats[4][numQs+1];
    int i, j;
    for(i=0;i<4;i++)
    {
        for(j=0;j<numQs+1;j++)
        {
            questionStats[i][j]=0;
        }
    }

    //create grades directory
    make_directory("grades");

	//create a grades/quizname/overall.grade file to store calculations
    char gradeFile[300]="grades/";
    strcat(gradeFile, temp);
    strtok(gradeFile, "\n");
    strcat(gradeFile, "/");
    make_directory(gradeFile);
    strcat(gradeFile, "overall.grade");
    master_results = fopen(gradeFile, "w");
    if (master_results == NULL)
    {
        fprintf(stderr, "Error: Failed to create %s\n", gradeFile);
        printf("Press ENTER to close Grader.\n");
        fflush(stdin);
        getchar();
        return 1;
    }

    //create a quizDump/quizName.dump file to store the test
    FILE* dumpFP;
    make_directory("quizDump");
    char dumpFile[300]="quizDump/";
    strcat(dumpFile, temp);
    strtok(dumpFile, "\n");
    strcat(dumpFile, ".dump");
    dumpFP = fopen(dumpFile, "w");
    if (dumpFP == NULL)
    {
        fprintf(stderr, "Error: Failed to create %s\n", dumpFile);
        printf("Press ENTER to close Grader.\n");
        fflush(stdin);
        getchar();
        return 1;
    }

    //creating string for results directory
    char resultsDir[300]="results/";
    strcat(resultsDir, temp);
    strtok(resultsDir, "\n");
    strcat(resultsDir, "/");

    //checking if results-quizname/ directory can open and opening if it exists
    if (NULL == (FD = opendir (resultsDir))) 
    {
        printf("Error: Failed to open %s directory\n", resultsDir);
        printf("This error is common if no one has taken the selected quiz yet.\n");
        printf("Press ENTER to close Grader.\n");
        fflush(stdin);
        getchar();
        fclose(master_results);
        return 1;
    }

    //looping through all files in results/ directory
    while ((in_file = readdir(FD))) 
    {
    	//remove parent directory listings
        if (!strcmp (in_file->d_name, "."))
        {
            continue; 
        }
        if (!strcmp (in_file->d_name, ".."))    
        {
            continue; //do not print
        }

        //get name of file with results/ dir prepended
        char fileString[150];
        strcpy(fileString, resultsDir);
        strcat(fileString, in_file->d_name);

        //open file in r+ mode and check
        current_file = fopen(fileString, "r+");
        if (current_file == NULL)
        {
            printf("Error: Failed to open file %s!\n", in_file->d_name);
            printf("Press ENTER to close Grader.\n");
            fflush(stdin);
            getchar();
            fclose(master_results);
            return 1;
        }
        else
        {
            printf("Now grading %s!\n", in_file->d_name);
        }

        //storing studentName for future use
        char studentName[150];
        strcpy(studentName, in_file->d_name);
        int studentNameLen = strlen(studentName);
        studentName[studentNameLen-12]='\0';

        //opening filestream for individual results
        char studentID[300]="grades/";
        strcat(studentID, temp);
        strtok(studentID, "\n");
        strcat(studentID, "/");
        strcat(studentID, in_file->d_name);
        int studentIDLen = strlen(studentID);
        studentID[studentIDLen-11] = '\0';
        strcat(studentID, "grade");
        FILE* lone_results;
        lone_results = fopen(studentID, "w+");
        if(lone_results == NULL)
        {
            printf("Error: Failed to create %s\n", studentID);
            printf("Press ENTER to close Grader.\n");
            fflush(stdin);
            getchar();
            fclose(lone_results);
            fclose(master_results);
            return 1;
        }

        //trim B: line off results file
        int cPos = ftell(current_file);
        fgets(buffer, 250, current_file);

        //declaring persistent counter variables
        int studentCorrect=0;
        float studentAverage=0;
        int questionNum=1;

        //loop through entire file and print to screen
        while (fgets(buffer, 250, current_file) != NULL)
        {
            //get question from quiz file
            char quizbuffer[300];
            while(strstr(quizbuffer, "Q: ") == NULL && strstr(quizbuffer, "EEE") == NULL)
            {
                fgets(quizbuffer, 250, quiz);  
            }
            if(strstr(quizbuffer, "Q: ") != NULL)
            {
                char *truebuffer = quizbuffer +3;
                fprintf(dumpFP, "--------------------------------\n");
                fprintf(dumpFP, "Question %d:\n", questionNum);
                questionNum++;
                fprintf(dumpFP, "%s", truebuffer);
                fgets(quizbuffer, 250, quiz);
            }

            //get answers from quiz file
            while(strstr(quizbuffer, "C: ") == NULL && strstr(quizbuffer, "EEE") == NULL)
            {
                while(strstr(quizbuffer, "A. ") == NULL && strstr(quizbuffer, "EEE") == NULL)
                {
                    fgets(quizbuffer, 250, quiz);  
                }
                if(strstr(quizbuffer, "A. ") != NULL)
                {
                    char *truebuffer = quizbuffer +3;
                    fprintf(dumpFP, "\t%s", truebuffer);
                    fgets(quizbuffer, 250, quiz);
                }
            }
            
            //get question number
            if (strstr(buffer, "Q: ") != NULL)
            {
                cPos = ftell(current_file);
                fseek(current_file, cPos-4, SEEK_SET);
                int questionNum = atoi(fgets(buffer, 225, current_file));
                cPos = ftell(current_file);

                //put question number into table
                questionStats[0][questionNum] = questionNum;

                //see if answer was right or wrong
                fgets(buffer, 250, current_file);
                fseek(current_file, -4, SEEK_CUR);
                int questionStatus = atoi(fgets(buffer, 225, current_file));

                if(questionStatus==1)
                {
                    questionStats[1][questionNum]++;
                    studentCorrect++;
                    fprintf(lone_results, "\tQuestion %d: Correct!\n", questionNum);
                }
                else
                {
                    //get studentAns and expectedAns
                    fgets(buffer, 250, current_file);
                    fseek(current_file, -4, SEEK_CUR);
                    int studentAns = atoi(fgets(buffer, 250, current_file));
                    fgets(buffer, 250, current_file);
                    fseek(current_file, -4, SEEK_CUR);
                    int expectedAns = atoi(fgets(buffer, 250, current_file));
                    questionStats[2][questionNum]++;
                    fprintf(lone_results, "\tQuestion %d: Wrong! Expected %d but received %d\n", questionNum, expectedAns, studentAns);
                }
                fprintf(lone_results, "--------------------------------\n");
            } 
        }

        //print score and percent to individual file
        studentAverage = (float) studentCorrect / numQs * 100;
        fprintf(lone_results, "Score: %d out of %d\n", studentCorrect, numQs);
        fprintf(lone_results, "Percentage: %.2f%%\n", studentAverage);

        //print user and percent to overall file
        fprintf(master_results, "ID:%s - %d/%d - %.2f%%\n", studentName, studentCorrect, numQs, studentAverage);

	    //closing current file to move onto next one
        printf("Completed grading %s!\n", in_file->d_name);
        printf("Individual grade file saved to %s!\n", studentID);
        line();
	    fclose(current_file);
        fclose(lone_results);
        numStudents++;
    }

    //calculate question averages
    for(i=1;i<numQs+1;i++)
    {
        questionStats[3][i] = questionStats[1][i] / numStudents * 100;
    }

    //print questionStats to overall.grade in table format if questions <=10
    if(numQs<=10)
    {
        fprintf(master_results, "--------------------\n");
        for(i=0;i<4;i++)
        {
            switch(i)
            {
                case 0:
                    fprintf(master_results, "Question:\t"); 
                    break;
                case 1: 
                    fprintf(master_results, "Correct :\t"); 
                    break;
                case 2: 
                    fprintf(master_results, "Wrong   :\t"); 
                    break;
                case 3: 
                    fprintf(master_results, "Percent :\t"); 
                    break;
            }
            for(j=1;j<numQs+1;j++)
            {
                if(i==3)
                {
                    fprintf(master_results, "%.2f%%\t", questionStats[i][j]); 
                }
                else
                {
                    fprintf(master_results, "%.2f\t", questionStats[i][j]); 
                }
            }
            fprintf(master_results, "\n"); 
        }
    }
    else
    {
        //print questionStats to overall.grade in list format
        fprintf(master_results, "--------------------\n");
        for(i=1;i<numQs+1;i++)
        {
            fprintf(master_results, "Question: %.2f\n", questionStats[0][i]); 
            fprintf(master_results, "\tCorrect: %.2f\n", questionStats[1][i]); 
            fprintf(master_results, "\tWrong: %.2f\n", questionStats[2][i]); 
            fprintf(master_results, "\tPercent: %.2f%%\n", questionStats[3][i]); 
                    
            fprintf(master_results, "\n"); 
        }
    }
    

    //print questionStats to screen if questions <=10
    if(numQs<=10)
    {
       for(i=0;i<4;i++)
        {
            switch(i)
            {
                case 0: 
                    printf("Question:\t");
                    break;
                case 1: 
                    printf("Correct :\t"); 
                    break;
                case 2: 
                    printf("Wrong   :\t"); 
                    break;
                case 3: 
                    printf("Percent :\t"); 
                    break;
            }
            for(j=1;j<numQs+1;j++)
            {
                if(i==3)
                {
                    printf("%.2f%%\t", questionStats[i][j]);
                }
                else
                {
                    printf("%.2f\t", questionStats[i][j]);
                }
            }
            printf("\n");
        } 
    }
    else
    {
        printf("There is more than 10 questions in this quiz.\n");
        printf("Individual question results table printed to file only.\n");
    }

    //get total average
    float classAverage=0;
    for(i=1;i<=numQs;i++)
    {
    	classAverage += questionStats[3][i];
    }
    classAverage /= numQs;
    line();
    printf("Quiz average was %.2f%%.\n", classAverage);
    fprintf(master_results, "--------------------\n");
    fprintf(master_results, "Quiz average was: %.2f%%.\n", classAverage);

    line();
    printf("Overall results saved to %s!\n", gradeFile);
    printf("Test Dump saved to %s and will be visible to students!\n", dumpFile);
    printf("Press ENTER to exit Grader.\n");
    fflush(stdin);
    getchar();

    //closing streams
    fclose(dumpFP);
    fclose(master_results);
    fclose(quiz);
	return 0;
}