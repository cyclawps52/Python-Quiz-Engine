#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "viewer.h"
#include "../custom/custom.h"

int gradeViewer(char carryID[])
{
	clear();

	FILE* gradeFile;
	FILE* testFile;
	FILE* resultsFile;

	//get quizID
	printf("What quiz do you want to check the grade for(100 char max): ");
	fflush(stdin);
	char testID[100];
	fgets(testID, 100, stdin);
	strtok(testID, "\n");

	//check if choice is empty
	if(strcmp(testID, "\n") == 0)
	{
		printf("Quiz name cannot be empty!\n");
		pete();
		return 1;
	}

	//check if quiz is valid
	char testFilePath[150] = "quizes/";
	strcat(testFilePath, testID);
	strcat(testFilePath, ".quizfile");
	testFile = fopen(testFilePath, "r");
	if(testFile == NULL)
	{
		printf("Quiz %s does not exist!\n", testID);
		pete();
		return 1;
	}

	//check if student has taken quiz
	char resultsFilePath[300] = "results/";
	strcat(resultsFilePath, testID);
	strcat(resultsFilePath, "/");
	strcat(resultsFilePath, carryID);
	strcat(resultsFilePath, ".quizresults");
	resultsFile = fopen(resultsFilePath, "r");
	if(resultsFile == NULL)
	{
		printf("You have not taken %s yet!\n", testID);
		pete();
		return 1;
	}


	//get string for gradeFile
	char gradeFilePath[150] = "grades/";
	strcat(gradeFilePath, testID);
	strcat(gradeFilePath, "/");
	strcat(gradeFilePath, carryID);
	strcat(gradeFilePath, ".grade");

	//check if grade file exists
	gradeFile = fopen(gradeFilePath, "r");
	if(gradeFile == NULL)
	{
		printf("Grades have not been released for %s yet!\n", testID);
		pete();
		return 1;
	}

	//display grade file
	clear();
	char c = fgetc(gradeFile);
    while (c != EOF)
    {
        printf ("%c", c);
        c = fgetc(gradeFile);
    }

    line();
    pete();
    fclose(resultsFile);
	fclose(gradeFile);
	fclose(testFile);
	return 0;
}

int gradeViewerTeacher()
{
	clear();

	FILE* gradeFile;
	FILE* testFile;
	FILE* resultsFile;
	FILE* studentFile;

	char carryID[100];

	//get studentID and save as carryID
	printf("Which student's grade file do you want to check(100 char max): ");
	fflush(stdin);
	fgets(carryID, 100, stdin);
	strtok(carryID, "\n");

	//check if choice is empty
	if(strcmp(carryID, "\n") == 0)
	{
		printf("Student ID cannot be empty!\n");
		pete();
		return 1;
	}

	//check if valid student
	char studentIDPath[150] = "users/";
	strcat(studentIDPath, carryID);
	strcat(studentIDPath, ".user");
	studentFile = fopen(studentIDPath, "rb");
	if(studentFile == NULL)
	{
		printf("Student %s does not exist!\n");
		pete();
		return 1;
	}
	
	//get quizID
	printf("What quiz do you want to check the grade for(100 char max): ");
	fflush(stdin);
	char testID[100];
	fgets(testID, 100, stdin);
	strtok(testID, "\n");

	//check if choice is empty
	if(strcmp(testID, "\n") == 0)
	{
		printf("Quiz name cannot be empty!\n");
		pete();
		return 1;
	}

	//check if quiz is valid
	char testFilePath[150] = "quizes/";
	strcat(testFilePath, testID);
	strcat(testFilePath, ".quizfile");
	testFile = fopen(testFilePath, "r");
	if(testFile == NULL)
	{
		printf("Quiz %s does not exist!\n", testID);
		pete();
		return 1;
	}

	//check if student has taken quiz
	char resultsFilePath[300] = "results/";
	strcat(resultsFilePath, testID);
	strcat(resultsFilePath, "/");
	strcat(resultsFilePath, carryID);
	strcat(resultsFilePath, ".quizresults");
	resultsFile = fopen(resultsFilePath, "r");
	if(resultsFile == NULL)
	{
		printf("%s has not taken %s yet!\n", carryID, testID);
		pete();
		return 1;
	}

	//get string for gradeFile
	char gradeFilePath[150] = "grades/";
	strcat(gradeFilePath, testID);
	strcat(gradeFilePath, "/");
	strcat(gradeFilePath, carryID);
	strcat(gradeFilePath, ".grade");

	//check if grade file exists
	gradeFile = fopen(gradeFilePath, "r");
	if(gradeFile == NULL)
	{
		printf("Grades have not been released for %s yet!\n", testID);
		pete();
		return 1;
	}

	//display grade file
	clear();
	char c = fgetc(gradeFile);
    while (c != EOF)
    {
        printf ("%c", c);
        c = fgetc(gradeFile);
    }

    line();
    pete();
    fclose(studentFile);
    fclose(resultsFile);
	fclose(gradeFile);
	fclose(testFile);
	return 0;
}

int dumpViewer(char carryID[])
{
	clear();

	FILE* resultsFile;
	FILE* testFile;
	FILE* dumpFile;

	//get quizID
	printf("What quiz do you want to view the dump of(100 char max): ");
	fflush(stdin);
	char testID[100];
	fgets(testID, 100, stdin);
	strtok(testID, "\n");

	//check if choice is empty
	if(strcmp(testID, "\n") == 0)
	{
		printf("Quiz name cannot be empty!\n");
		pete();
		return 1;
	}

	//check if quiz is valid
	char testFilePath[150] = "quizes/";
	strcat(testFilePath, testID);
	strcat(testFilePath, ".quizfile");
	testFile = fopen(testFilePath, "r");
	if(testFile == NULL)
	{
		printf("Quiz %s does not exist!\n", testID);
		pete();
		return 1;
	}

	//check if student has taken quiz
	char resultsFilePath[300] = "results/";
	strcat(resultsFilePath, testID);
	strcat(resultsFilePath, "/");
	strcat(resultsFilePath, carryID);
	strcat(resultsFilePath, ".quizresults");
	resultsFile = fopen(resultsFilePath, "r");
	if(resultsFile == NULL)
	{
		printf("You have not taken %s yet!\n", testID);
		pete();
		return 1;
	}

	//check if dump has been posted yet
	char dumpFilePath[300] = "quizDump/";
	strcat(dumpFilePath, testID);
	strcat(dumpFilePath, ".dump");
	dumpFile = fopen(dumpFilePath, "r");
	if(dumpFile == NULL)
	{
		printf("%s has not been graded yet!\n", testID);
		printf("Dump files will be avaliable after the quiz has been graded.\n");
		pete();
		return 1;
	}

	//display dump file
	clear();
	char c = fgetc(dumpFile);
    while (c != EOF)
    {
        printf ("%c", c);
        c = fgetc(dumpFile);
    }

    line();
    pete();
    fclose(resultsFile);
	fclose(dumpFile);
	fclose(testFile);
	return 0;
}

int dumpViewerTeacher()
{
	clear();
	
	FILE* testFile;
	FILE* dumpFile;

	//get quizID
	printf("What quiz do you want to view the dump of(100 char max): ");
	fflush(stdin);
	char testID[100];
	fgets(testID, 100, stdin);
	strtok(testID, "\n");

	//check if choice is empty
	if(strcmp(testID, "\n") == 0)
	{
		printf("Quiz name cannot be empty!\n");
		pete();
		return 1;
	}

	//check if quiz is valid
	char testFilePath[150] = "quizes/";
	strcat(testFilePath, testID);
	strcat(testFilePath, ".quizfile");
	testFile = fopen(testFilePath, "r");
	if(testFile == NULL)
	{
		printf("Quiz %s does not exist!\n", testID);
		pete();
		return 1;
	}

	//check if dump has been posted yet
	char dumpFilePath[300] = "quizDump/";
	strcat(dumpFilePath, testID);
	strcat(dumpFilePath, ".dump");
	dumpFile = fopen(dumpFilePath, "r");
	if(dumpFile == NULL)
	{
		printf("%s has not been graded yet!\n", testID);
		printf("Dump files will be avaliable after the quiz has been graded.\n");
		pete();
		return 1;
	}

	//display dump file
	clear();
	char c = fgetc(dumpFile);
    while (c != EOF)
    {
        printf ("%c", c);
        c = fgetc(dumpFile);
    }

    line();
    pete();
	fclose(dumpFile);
	fclose(testFile);
	return 0;
}

int overallViewerTeacher()
{
	clear();
	
	FILE* testFile;
	FILE* overallFile;

	//get quizID
	printf("What quiz do you want to view the overall grade file of(100 char max): ");
	fflush(stdin);
	char testID[100];
	fgets(testID, 100, stdin);
	strtok(testID, "\n");

	//check if choice is empty
	if(strcmp(testID, "\n") == 0)
	{
		printf("Quiz name cannot be empty!\n");
		pete();
		return 1;
	}

	//check if quiz is valid
	char testFilePath[150] = "quizes/";
	strcat(testFilePath, testID);
	strcat(testFilePath, ".quizfile");
	testFile = fopen(testFilePath, "r");
	if(testFile == NULL)
	{
		printf("Quiz %s does not exist!\n", testID);
		pete();
		return 1;
	}

	//check if overall file has been generated yet
	char overallFilePath[300] = "grades/";
	strcat(overallFilePath, testID);
	strcat(overallFilePath, "/overall.grade");
	overallFile = fopen(overallFilePath, "r");
	if(overallFile == NULL)
	{
		printf("%s has not been graded yet!\n", testID);
		printf("Overall grade file will be avaliable after the quiz has been graded.\n");
		pete();
		return 1;
	}

	//display dump file
	clear();
	char c = fgetc(overallFile);
    while (c != EOF)
    {
        printf ("%c", c);
        c = fgetc(overallFile);
    }

    line();
    pete();
	fclose(overallFile);
	fclose(testFile);
	return 0;
}