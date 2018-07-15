#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <dirent.h>
#include <sys/stat.h>

#include "delete.h"
#include "../custom/custom.h"
#include "../auth/auth.h"

int teacherDelete(char carryID[])
{
	clear();
	
	int newPerm;
	char toDeletePath[350];

	//display deletion menu
	printf("1. Demote User (turn teacher account into student)\n");
	printf("2. Remove User Completely\n");
	printf("\n");
	printf("3. Remove Test Dump (Prevent students from looking at quiz)\n");
	printf("4. Remove Results (Removes non-graded quiz attempts)\n");
	printf("5. Remove grades (Ex: graded too early)\n");
	printf("NOTICE: REMOVING RESULTS WITHOUT ALSO REMOVING GRADES WILL ALLOW STUDENTS TO VIEW OLD GRADES!\n");
	printf("NOTICE: REMOVING RESULTS WITHOUT ALSO REMOVING TEST DUMP WILL ALLOW STUDENTS TO VIEW THE DUMP!\n");
	printf("\n");
	printf("6. Soft Delete Quiz (No one can take the quiz, but grades/dumps persist)\n");
	printf("7. Hard Delete Quiz (Destroys quiz, grades, dumps, everything)\n");
	printf("\n");
	printf("8. Factory Reset (first time run/OOBE)\n");
	printf("\n");
	printf("0. Return to main menu\n");
	printf("\tWhat do you want to do: ");
	int menuChoice;
	fflush(stdin);
	if(scanf("%d", &menuChoice) == 0)
	{
		printf("Invalid option!\n");
		pete();
		return 1;
	}

	switch(menuChoice)
	{
		case 1: /* Demote User (turn teacher account into student) */
			demoteUser(carryID);
			break;
		case 2: /* Remove User Completely */
			removeUser(carryID);
			break;
		case 3: /* Remove Test Dump (Prevent students from looking at quiz) */
			removeDump();
			break;
		case 4: /* Remove Results (Removes non-graded quiz attempts) */
			removeResults();
			break;
		case 5: /* Remove grades (Ex: graded too early) */
			removeGrades();
			break;
		case 6: /* Soft Delete Quiz (No one can take the quiz, but grades/dumps persist) */
			softDelete();
			break;
		case 7: /* Hard Delete Quiz (Destroys quiz, grades, dumps, everything) */
			hardDelete();
			break;
		case 8: /* Factory Reset (first time run/OOBE) */
			newPerm = factoryReset();
			pete();
			return newPerm;
		case 0:
			return 1;
		default:
			printf("Invalid option!\n");
			pete();
			return 1;
	}

    pete();
	return 1;
}

int remove_directory(const char *path)
{
	/*
	I take no credit for this function. This was found at 
	https://stackoverflow.com/questions/2256945/removing-a-non-empty-directory-programmatically-in-c-or-c
	and taken from the marked answer written by asveikau.
	*/

	DIR *d = opendir(path);
	size_t path_len = strlen(path);
	int r = -1;

	if (d)
	{
	  struct dirent *p;

	  r = 0;

	  while (!r && (p=readdir(d)))
	  {
	      int r2 = -1;
	      char *buf;
	      size_t len;

	      /* Skip the names "." and ".." as we don't want to recurse on them. */
	      if (!strcmp(p->d_name, ".") || !strcmp(p->d_name, ".."))
	      {
	         continue;
	      }

	      len = path_len + strlen(p->d_name) + 2; 
	      buf = malloc(len);

	      if (buf)
	      {
	         struct stat statbuf;

	         snprintf(buf, len, "%s/%s", path, p->d_name);

	         if (!stat(buf, &statbuf))
	         {
	            if (S_ISDIR(statbuf.st_mode))
	            {
	               r2 = remove_directory(buf);
	            }
	            else
	            {
	               r2 = unlink(buf);
	            }
	         }

	         free(buf);
	      }

	      r = r2;
	  }

	  closedir(d);
	}

	if (!r)
	{
	  r = rmdir(path);
	}
}

int removeDump()
{
	clear();

	//get quizID
	printf("What quiz's dump file would you like to remove: ");
	fflush(stdin);
	char dumpToDelete[100];
	fgets(dumpToDelete, 100, stdin);
	strtok(dumpToDelete, "\n");

	//check if choice is empty
	if(strcmp(dumpToDelete, "\n") == 0)
	{
		printf("Selection cannot be empty!\n");
		return 1;
	}

	//check if quiz exists
	FILE* quizCheck;
	char quizCheckPath[150] = "quizes/";
	strcat(quizCheckPath, dumpToDelete);
	strcat(quizCheckPath, ".quizfile");
	quizCheck = fopen(quizCheckPath, "r");
	if(quizCheck == NULL)
	{
		printf("Quiz %s does not exist!\n", dumpToDelete);
		return 1;
	}

	//make path for dumpFile
	char dumpDeletePath[150] = "quizDump/";
	strcat(dumpDeletePath, dumpToDelete);
	strcat(dumpDeletePath, ".dump");

	//check if dump exists
	FILE* dumpCheck;
	dumpCheck = fopen(dumpDeletePath, "r");
	if(dumpCheck == NULL)
	{
		printf("Quiz %s has not been graded yet!\n", dumpToDelete);
		printf("Dump file is not avaliable until the quiz is graded.\n");
		pete();
		return 1;
	}
	fclose(dumpCheck);

	if (remove(dumpDeletePath) == 0)
	{
    	printf("Quiz dump for %s has been removed.\n", dumpToDelete);
	}
	else
	{
		printf("Quiz dump for %s could not be deleted.\n", dumpToDelete);
		return 1;
	}

	fclose(dumpCheck);
	fclose(quizCheck);
	return 0;
}

int removeResults()
{
	clear();

	//get quizID
	printf("What quiz's results folder would you like to remove: ");
	fflush(stdin);
	char resultsToDelete[100];
	fgets(resultsToDelete, 100, stdin);
	strtok(resultsToDelete, "\n");

	//check if choice is empty
	if(strcmp(resultsToDelete, "\n") == 0)
	{
		printf("Selection cannot be empty!\n");
		return 1;
	}

	//check if quiz exists
	FILE* quizCheck;
	char quizCheckPath[150] = "quizes/";
	strcat(quizCheckPath, resultsToDelete);
	strcat(quizCheckPath, ".quizfile");
	quizCheck = fopen(quizCheckPath, "r");
	if(quizCheck == NULL)
	{
		printf("Quiz %s does not exist!\n", resultsToDelete);
		return 1;
	}
	fclose(quizCheck);

	//make results directory string
	char resultsDeletePath[150] = "results/";
	strcat(resultsDeletePath, resultsToDelete);

	remove_directory(resultsDeletePath);

	printf("The results/%s directory has been deleted (if it existed).\n", resultsToDelete);

	fclose(quizCheck);
	return 0;
}

int removeGrades()
{
	clear();

	//get quizID
	printf("What quiz's grades folder would you like to remove: ");
	fflush(stdin);
	char gradesToDelete[100];
	fgets(gradesToDelete, 100, stdin);
	strtok(gradesToDelete, "\n");

	//check if choice is empty
	if(strcmp(gradesToDelete, "\n") == 0)
	{
		printf("Selection cannot be empty!\n");
		return 1;
	}

	//check if quiz exists
	FILE* quizCheck;
	char quizCheckPath[150] = "quizes/";
	strcat(quizCheckPath, gradesToDelete);
	strcat(quizCheckPath, ".quizfile");
	quizCheck = fopen(quizCheckPath, "r");
	if(quizCheck == NULL)
	{
		printf("Quiz %s does not exist!\n", gradesToDelete);
		return 1;
	}
	fclose(quizCheck);

	//make grades directory string
	char gradesDeletePath[150] = "grades/";
	strcat(gradesDeletePath, gradesToDelete);

	remove_directory(gradesDeletePath);

	printf("The grades/%s directory has been deleted (if it existed).\n", gradesToDelete);

	fclose(quizCheck);
	return 0;
}

int softDelete()
{
	clear();

	//get quizID
	printf("What quiz would you like to soft delete: ");
	fflush(stdin);
	char quizToDelete[100];
	fgets(quizToDelete, 100, stdin);
	strtok(quizToDelete, "\n");

	//check if choice is empty
	if(strcmp(quizToDelete, "\n") == 0)
	{
		printf("Selection cannot be empty!\n");
		return 1;
	}

	//check if quiz exists
	FILE* quizCheck;
	char quizCheckPath[150] = "quizes/";
	strcat(quizCheckPath, quizToDelete);
	strcat(quizCheckPath, ".quizfile");
	quizCheck = fopen(quizCheckPath, "r");
	if(quizCheck == NULL)
	{
		printf("Quiz %s does not exist!\n", quizToDelete);
		return 1;
	}
	fclose(quizCheck);

	if (remove(quizCheckPath) == 0)
	{
    	printf("Quiz %s has been soft deleted.\n", quizToDelete);
	}
	else
	{
		printf("Quiz %s could not be soft deleted.\n", quizToDelete);
		printf("Students will still have access to this quiz.\n");
		return 1;
	}

	fclose(quizCheck);
	return 0;
}

int hardDelete()
{
	clear();

	//get quizID
	printf("What quiz would you like to hard delete: ");
	fflush(stdin);
	char quizToDelete[100];
	fgets(quizToDelete, 100, stdin);
	strtok(quizToDelete, "\n");

	//check if choice is empty
	if(strcmp(quizToDelete, "\n") == 0)
	{
		printf("Selection cannot be empty!\n");
		return 1;
	}

	//check if quiz exists
	FILE* quizCheck;
	char quizCheckPath[150] = "quizes/";
	strcat(quizCheckPath, quizToDelete);
	strcat(quizCheckPath, ".quizfile");
	quizCheck = fopen(quizCheckPath, "r");
	if(quizCheck == NULL)
	{
		printf("Quiz %s does not exist!\n", quizToDelete);
		return 1;
	}
	fclose(quizCheck);

	//destroy quiz
	if (remove(quizCheckPath) == 0)
	{
    	printf("Quiz file %s has been deleted.\n", quizToDelete);
	}
	else
	{
		printf("Quiz file for %s could not be deleted.\n", quizToDelete);
		printf("Aborting hard delete.\n");
		return 1;
	}

	fclose(quizCheck);

	//destroy results
	char resultsDeletePath[150] = "results/";
	strcat(resultsDeletePath, quizToDelete);
	strcat(resultsDeletePath, "/");

	remove_directory(resultsDeletePath);

	printf("The results/%s directory has been deleted (if it existed).\n", quizToDelete);

	//destroy grades
	char gradesDeletePath[150] = "grades/";
	strcat(gradesDeletePath, quizToDelete);
	strcat(gradesDeletePath, "/");

	remove_directory(gradesDeletePath);

	printf("The grades/%s directory has been deleted (if it existed).\n", quizToDelete);

	//destroy dump
	char dumpDeletePath[150] = "quizDump/";
	strcat(dumpDeletePath, quizToDelete);
	strcat(dumpDeletePath, ".dump");
	if (remove(quizCheckPath) == 0)
	{
    	printf("Dump file for %s has been deleted.\n", quizToDelete);
	}
	else
	{
		printf("Dump file did not exist for %s.\n", quizToDelete);
	}

	printf("All tasks finished successfully!\n");

	return 0;
}

int factoryReset()
{
	clear();

	printf("Are you sure? THIS ACTION CANNOT BE UNDONE!\n");
	int confirmDelete;
	printf("To confirm, please enter the number 1337.\n");
	printf("Anything else will cancel the reset process.\n");
	printf("\n\n");
	printf("\t\tConfirm: ");
	fflush(stdin);
	if(scanf("%d", &confirmDelete) == 0)
	{
		printf("Invalid input, cancelling factory reset!\n");
		return 1;
	}
	if(confirmDelete != 1337)
	{
		printf("Invalid input, cancelling factory reset!\n");
		return 1;
	}

	//begin deletion process
	
	//directories
	remove_directory("quizes/");
	remove_directory("grades/");
	remove_directory("quizDump/");
	remove_directory("results/");

	//remove default teacher file
	if(remove("teachers/default.teacher") != 0)
	{
		printf("Default teacher file could not be deleted.\n");
		printf("Please delete teachers/ directory manually.\n");
		printf("If this directory is not deleted, the automatic teacher creator will not appear.\n");
		pete();
	}

	remove_directory("teachers/");
	remove_directory("users/");

	clear();
	printf("Factory reset complete.\n");
	printf("Occasionally, certain files will deny automatic deletion. This is out of the quiz engine's control.\n");
	printf("If there are any files inside the install directory besides FQE, please delete them.\n");

	return -2;
}