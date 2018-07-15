#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>

#include "../custom/custom.h"
#include "takeQuiz.h"

int takeQuiz(char studentID[])
{
	clear();

	//declaring file pointers
	FILE *quiz;
	FILE *results;

	//get name of quiz to run
	char quizName[140]="quizes/";
	char temp[100];
	printf("What quiz do you want to run(100 char max): ");
	fflush(stdin);
	fgets(temp, 100, stdin);
	strtok(temp, "\n");
	strcat(quizName, temp);

	//check if choice is empty
	if(strcmp(temp, "\n") == 0)
	{
		printf("Quiz name cannot be empty!\n");
		pete();
		return 1;
	}
	

	//add .quizfile extension to string
	strcat(quizName, ".quizfile");

	//opening quiz file stream r+
	quiz = fopen(quizName, "r+");
	if(quiz==NULL)
	{
		printf("There was an error opening the quiz file.\n");
		pete();
		return 1;
	}

	//create results directory
	make_directory("results");

	//create subdirectory for results
	char resultsDir[250] = "results/";
	strcat(resultsDir, temp);
	strcat(resultsDir, "/");
	make_directory(resultsDir);

	//fix passed in student name (in case a newline is still stuck in the buffer)
	strtok(studentID, "\n");

	//prefix results/quizname/ to studentID and append .quizresults
	char resultsName[300];
	strcpy(resultsName, resultsDir);
	strcat(resultsName, studentID);
	strcat(resultsName, ".quizresults");

	//check if student has taken the test already
	//if so, will exit with error
	results = fopen(resultsName ,"r");
	if(results!=NULL)
	{
		printf("A results file already exists for:\n");
		printf("\tStudentID: %s\n", studentID);
		printf("\tQuiz: %s\n", temp);
		printf("If this is in error, please contact the administrator.\n");
		pete();
		fclose(results);
		return 1;
	}

	//opening results file stream w
	results = fopen(resultsName, "w");
	if(results==NULL)
	{
		printf("There was an error creating a file to store results.\n");
		pete();
		return 1;
	}

	//get number of questions in quiz
	int numQs;
	char buffer[225];
	fseek(quiz, 3, SEEK_SET);
	fgets(buffer, 225, quiz);
	numQs = atoi(buffer);
	
	//loop for number of questions in quiz
	int i;
	int correctCount=0;
	long cPos; //saves positions in file pointers
	for(i=1;i<=numQs;i++)
	{
		clear();
		//display question
		fgets(buffer, 225, quiz);
		fseek(quiz, 3, SEEK_CUR);
		fgets(buffer, 225, quiz);
		if(i==1)
		{
			printf("Question %d of %d:\n%s", i, numQs, buffer);
		}
		else
		{
			printf("Question %d of %d: %s", i, numQs, buffer);
		}
		
		//Display answer options
		fgets(buffer, 225, quiz);
		do
		{
			cPos = ftell(quiz); //catches position of C: line
			char *answerBuffer = buffer + 3;
			printf("%s", answerBuffer); 
			fgets(buffer, 225, quiz);
		} while(strstr(buffer, "C: ") == NULL);

		//get correct answer number
		int correctAns;
		fseek(quiz, cPos+3, SEEK_SET);
		fgets(buffer, 225, quiz);
		correctAns = atoi(buffer);

		//get user answer
		int userAns;
		char userAnsTemp[5];
		printf("Select an answer: ");
		fflush(stdin);
		fgets(userAnsTemp, 5, stdin);
		userAns = atoi(userAnsTemp);

		//compare answers and write to document
		fprintf(results, "B: \n"); //question begin mark
		fprintf(results, "Q: %d\n", i);
		if(userAns==correctAns)
		{
			fprintf(results, "C: 1\n");
			correctCount++;
		}
		else
		{
			fprintf(results, "C: 0\n");
		}

		fprintf(results, "A: %d\n", userAns); //prints user answer to file
		fprintf(results, "X: %d\n", correctAns); //prints expected answer to file

		fprintf(results, "E: \n"); //question end mark
	}

	//get flag information
	fgets(buffer, 250, quiz);
	cPos = ftell(quiz);
	fgets(buffer, 250, quiz);
	fseek(quiz, cPos+3, SEEK_SET);
	int containsFlag = atoi(fgets(buffer, 250, quiz));
	char flagBox[250];
	int flagMin=100; //max 99 questions, if no flag this should override
	if(containsFlag==1)
	{
		//get flag threshold
		cPos=ftell(quiz);
		fgets(buffer, 250, quiz);
		fseek(quiz, cPos+3, SEEK_SET);
		flagMin = atoi(fgets(buffer, 250, quiz));
		
		//get flag
		cPos=ftell(quiz);
		fgets(buffer, 250, quiz);
		fseek(quiz, cPos+3, SEEK_SET);
		fgets(flagBox, 250, quiz);
	}

	//display final results and flag if eligible
	clear();
	printf("Your score was: %d/%d.\n", correctCount, numQs);
	float finalPercent = (float) correctCount / numQs * 100;
	printf("This is a %.2f%%.\n", finalPercent);
	if(correctCount >= flagMin)
	{
		line();
		printf("You scored high enough to see the flag!\n");
		printf("Flag:\t%s\n", flagBox);
		line();
	}
	pete();

	fclose(quiz);
	fclose(results);
	return 0;
}