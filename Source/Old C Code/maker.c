#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "../custom/custom.h"
#include "maker.h"

int maker()
{
	clear();
	
	//declaring file pointer
	FILE *fp;

	//getting name of file
	char quizName[140]="quizes/";
	printf("What will you call your quiz (100 char max): ");
	char temp[100];
	fflush(stdin);
	fgets(temp, 100, stdin);
	strtok(temp, "\n");
	strcat(quizName, temp);

	//check if quizID is blank
	if(strcmp(temp, "\n") == 0)
	{
		printf("Quiz name cannot be blank!\n");
		pete();
		return 1;
	}

	//add .quizfile extension to string
	strcat(quizName, ".quizfile");

	//make quiz directory
	make_directory("quizes");

	//opening file stream r/w
	fp = fopen(quizName, "w+");
	if(fp==NULL)
	{
		printf("There was an error creating the quiz file.\n");
		printf("Press ENTER to close Maker.\n");
		fflush(stdin);
		getchar();
		return 1;
	}
	
	//get number of questions
	int numQs;
	printf("How many questions (max 99): ");
	scanf("%d", &numQs);
	if(numQs>99)
	{
		printf("Number of questions must be at most 99.\n");
		printf("Press ENTER to close Maker.\n");
		fflush(stdin);
		getchar();
		fclose(fp);
		return 1;
	}

	//write number of questions to file
	fprintf(fp, "N: %d\n", numQs);
	//fwrite();

	//loop for number of questions
	int i;
	for(i=1;i<=numQs;i++)
	{
		clear();
		printf("You are creating question %d of %d\n", i, numQs);
		line();

		//write question begin mark to file
		fprintf(fp, "B: \n");

		//get question
		char question[200];
		printf("Please enter question #%d (max 200 characters).\n", i);
		fflush(stdin);
		fgets(question, 200, stdin);

		//write question to file
		fprintf(fp, "Q: %s", question);

		line();

		//get number of answers for question
		int numAs;
		printf("How many answers for question %d (max 99): ", i);
		scanf("%d", &numAs);
		
		//loop for number of answers
		for(int j=1;j<=numAs;j++)
		{
			char answer[200];
			printf("Option #%d for question %d (max 200 characters).\n", j, i);
			fflush(stdin);
			fgets(answer, 200, stdin);

			//write answer to file
			fprintf(fp, "A. %d. %s", j, answer);
		}

		line();

		//get correct answer
		int correctAs;
		printf("Which option # is the correct answer: ");
		scanf("%d", &correctAs);

		//write correct answer to file
		fprintf(fp, "C: %d\n", correctAs);

		//write question end mark to file
		fprintf(fp, "E: \n");
	}

	//put flag information
	int flagChoice;
	clear();
	printf("Would you like to have a flag displayed if the score is over a certain amount?\n");
	printf("1. Yes\n");
	printf("2. No\n");
	printf("\tChoice: ");
	scanf("%d", &flagChoice);
	int flagMin;
	switch(flagChoice)
	{
		case 1:
			
			fprintf(fp, "F: 1\n");
			printf("What is the minimum amount of questions the user must get right?\n");
			printf("Number between 0 and %d\n", numQs);
			printf("\tChoice: ");
			scanf("%d", &flagMin);
			if(flagMin > numQs)
			{
				printf("Choice must be below the number of questions, defaulting to zero.\n");
				fprintf(fp, "V: 0\n");
			}
			else
			{
				fprintf(fp, "V: %d\n", flagMin);
			}
			char flagBox[250];
			printf("What is the flag (max 250 characters with spaces): ");
			fflush(stdin);
			fgets(flagBox, 250, stdin);
			fprintf(fp, "T: %s", flagBox);
			break;
		case 2:
			fprintf(fp, "F: 0\n");
			break;
		default:
			printf("Not a valid option, defaulting to no flag.\n");
			fprintf(fp, "F: 0\n");
	}

	//print end mark to quiz
	fprintf(fp, "EEE");

	clear();
	printf("Test file created and saved as: %s\n", quizName);
	printf("Press ENTER to close Maker.\n");
	fflush(stdin);
	getchar();

	//closing file stream
	fclose(fp);
	return 0;
}