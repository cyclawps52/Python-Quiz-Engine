#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <conio.h>

#include "../custom/custom.h"
#include "auth.h"


//prompts for addUser
int addUser()
{
	clear();

	FILE* newUser;

	//Get user ID
	char userID[100];
	printf("Enter user ID (max 100 char): ");
	fflush(stdin);
	fgets(userID, 100, stdin);
	char userIDLen = strlen(userID);
	userID[userIDLen-1] = '\0';

	//check if userID is blank
	if(strcmp(userID, "") == 0)
	{
		printf("User ID cannot be blank!\n");
		pete();
		return 1;
	}

	//attempt to make user directory
	make_directory("users");

	//create userID string
	char userPath[110] = "users/";
	strcat(userPath, userID);
	strcat(userPath, ".user");

	//check if user ID exists
	newUser = fopen(userPath, "rb");
	if(newUser != NULL)
	{
		printf("User already exists!\n");
		pete();
		fclose(newUser);
		return 1;
	}

	//create user file
	newUser = fopen(userPath, "wb");

	//get password
	char indChar;
    char password[32];
    int passLen=0, i, boCheck=0;
    clear();
    printf("Creating user: %s\n", userID);
    printf("Please enter a password (max 32 char): ");
    while (1) 
    {
        indChar = getch();
        if (indChar == 0)
        {
            return 1;
        }
        
        if (indChar != '\r' && indChar != '\n' && indChar != '\b')
        {
        	password[passLen] = indChar;
        	passLen++;
        	boCheck++;
        }

        if(indChar == '\b')
        {
        	if(passLen>0)
        	{
        		passLen--;
        	}
        	if(boCheck>0)
        	{
        		boCheck--;
        	}
        }

        clear();
        printf("Creating user: %s\n", userID);
    	printf("Please enter a password (max 32 char): ");
        for (i = 0; i < passLen; i++)
        {
            printf("*");
        }
        if (indChar == '\n' || indChar == '\r')
        {
            break;
        }
        if(boCheck>=32)
        {
        	printf("\nOverflow detected, cutting password here!\n");
        	break;
        }

    }
    password[passLen] = '\0';

    //write password to file
    fwrite(password, sizeof(char), 50, newUser);

    //promote teacher if chosen
    int promoteUser;
    printf("\nWill this user be for a teacher?\n");
    printf("1. Yes\n");
    printf("2. No\n");
    printf("Choice: ");
    if( scanf("%d", &promoteUser) == 0)
    {
    	printf("Invalid option, defaulting to standard user.\n");
    	promoteUser = 2;
    }

    if(promoteUser == 1)
    {
    	//create teacher directory
    	make_directory("teachers");

    	//get teacher string
    	char teacherPath[110] = "teachers/";
		strcat(teacherPath, userID);
		strcat(teacherPath, ".teacher");

		//writing teacher file
		FILE* teacherFile;
		teacherFile = fopen(teacherPath, "wb");
		if(teacherFile == NULL)
		{
			printf("There was an error creating %s.\n", teacherPath);
			pete();
			return 1;
		}
		fwrite("abc123", sizeof(char), 6, teacherFile);
		fclose(teacherFile);
    }

	pete();

	fclose(newUser);
	return 0;
}

//stores inputted user's password in passed-in passwordBox
int retrievePassword(char userID[], char passwordBox[])
{
	clear();

	FILE* userFile;

	//attempt to make user directory
	make_directory("users");

	//create userID string
	char userPath[110] = "users/";
	strcat(userPath, userID);
	strcat(userPath, ".user");

	//check to see if user does not exist
	userFile = fopen(userPath, "rb");
	if(userFile == NULL)
	{
		printf("The user %s does not exist!\n", userID);
		pete();
		return 1;
	}

	//retrieve password
	fread(passwordBox, sizeof(char), 32, userFile);

	fclose(userFile);
	return 0;
}

//asks for user and displays password
int retrievePasswordManual()
{
	clear();

	FILE* userFile;

	//Get user ID
	char userID[100];
	printf("Enter user ID (max 100 char): ");
	fflush(stdin);
	fgets(userID, 100, stdin);
	char userIDLen = strlen(userID);
	userID[userIDLen-1] = '\0';

	//check if choice is empty
	if(strcmp(userID, "") == 0)
	{
		printf("User ID cannot be empty!\n");
		pete();
		return 1;
	}

	//attempt to make user directory
	make_directory("users");

	//create userID string
	char userPath[110] = "users/";
	strcat(userPath, userID);
	strcat(userPath, ".user");

	//check to see if user does not exist
	userFile = fopen(userPath, "rb");
	if(userFile == NULL)
	{
		printf("The user %s does not exist!\n", userID);
		pete();
		return 1;
	}

	//retrieve password
	char passwordBox[32];
	fread(passwordBox, sizeof(char), 32, userFile);

	printf("The password for %s is: %s\n", userID, passwordBox);
	pete();
	fclose(userFile);
	return 0;
}

//returns 1 if passed in user is teacher, 0 otherwise
int checkTeacher(char toCheck[])
{
	clear();

	//prepare user path
	char toCheckPath[150] = "users/";
	strcat(toCheckPath, toCheck);
	strcat(toCheckPath, ".user");

	//checking if user exists
	FILE* basicUser;
	basicUser = fopen(toCheckPath, "rb");
	if(basicUser == NULL)
	{
		printf("No user with the name %s is in the system!\n", toCheck);
		pete();
		return -1;
	}

	//check if user is teacher
	char toCheckTeach[150] = "teachers/";
	strcat(toCheckTeach, toCheck);
	strcat(toCheckTeach, ".teacher");
	FILE* teacherUser;
	teacherUser = fopen(toCheckTeach, "rb");
	if(teacherUser == NULL)
	{
		return 0;
	}

	fclose(teacherUser);
	fclose(basicUser);

	return 1;
}

//promotes student account to teacher
int promoteUser()
{
	clear();

	//get userID to promote
	char userID[100];
	printf("What user account do you wish to promote (max 100 char): ");
	fflush(stdin);
	fgets(userID, 100, stdin);
	strtok(userID, "\n");

	//check if choice is empty
	if(strcmp(userID, "\n") == 0)
	{
		printf("User ID cannot be empty!\n");
		pete();
		return 1;
	}

	//check if user file exists
	FILE* accountCheck;
	char accountCheckPath[150] = "users/";
	strcat(accountCheckPath, userID);
	strcat(accountCheckPath, ".user");
	accountCheck = fopen(accountCheckPath, "rb");
	if(accountCheck == NULL)
	{
		printf("User %s does not exist in the system!\n", userID);
		pete();
		return 1;
	}

	//create teacher directory
	make_directory("teachers");

	//get teacher string
	char teacherPath[110] = "teachers/";
	strcat(teacherPath, userID);
	strcat(teacherPath, ".teacher");

	//check if user is already a teacher
	FILE* teacherFile;
	teacherFile = fopen(teacherPath, "rb");
	if(teacherFile != NULL)
	{
		printf("User %s is already a teacher!\n", userID);
		fclose(teacherFile);
		pete();
		return 1;
	}

	//writing teacher file
	teacherFile = fopen(teacherPath, "wb");
	if(teacherFile == NULL)
	{
		printf("There was an error creating %s.\n", teacherPath);
		pete();
		return 1;
	}
	fwrite("abc123", sizeof(char), 6, teacherFile);
	fclose(teacherFile);

	printf("User %s successfully promoted to teacher!\n", userID);
	pete();

	fclose(teacherFile);
	fclose(accountCheck);
	return 0;
}

//demotes teacher account to user account
int demoteUser(char carryID[])
{
	clear();

	printf("Which user do you wish to demote: ");
	char userID[100];
	fflush(stdin);
	fgets(userID, 100, stdin);
	strtok(userID, "\n");

	//check if choice is empty
	if(strcmp(userID, "\n") == 0)
	{
		printf("User ID cannot be empty!\n");
		return 1;
	}

	//check if user inputted is the current logged in user
	if(strcmp(userID, carryID) == 0)
	{
		printf("Cannot demote currently logged in user.\n");
		printf("If you wish to delete all teacher accounts, please factory reset.\n");
		return 1;
	}

	//check if user exists
	FILE* userCheck;
	char userCheckPath[150] = "users/";
	strcat(userCheckPath, userID);
	strcat(userCheckPath, ".user");
	userCheck = fopen(userCheckPath, "rb");
	if(userCheck == NULL)
	{
		printf("User %s does not exist in the system!\n", userID);
		return 1;
	}
	fclose(userCheck);

	//create string for teacher file deletion
	char teacherDeletePath[150] = "teachers/";
	strcat(teacherDeletePath, userID);
	strcat(teacherDeletePath, ".teacher");
	if (remove(teacherDeletePath) == 0)
	{
      printf("User %s has been successfully demoted.\n");
      return 0;
	}
   else
   {
      printf("User %s is already a student!\n");
      return 0;
   }

   return 0;
}

//removes user account and teacher account
int removeUser(char carryID[])
{
	clear();

	printf("Which user do you wish to delete: ");
	char userID[100];
	fflush(stdin);
	fgets(userID, 100, stdin);
	strtok(userID, "\n");

	//check if choice is empty
	if(strcmp(userID, "\n") == 0)
	{
		printf("User ID cannot be empty!\n");
		return 1;
	}

	//check if user inputted is the current logged in user
	if(strcmp(userID, carryID) == 0)
	{
		printf("Cannot delete currently logged in user.\n");
		printf("If you wish to delete all accounts, please factory reset.\n");
		return 1;
	}

	//check if user exists
	FILE* userCheck;
	char userCheckPath[150] = "users/";
	strcat(userCheckPath, userID);
	strcat(userCheckPath, ".user");
	userCheck = fopen(userCheckPath, "rb");
	if(userCheck == NULL)
	{
		printf("User %s does not exist in the system!\n", userID);
		return 1;
	}
	fclose(userCheck);

	//create string for teacher file deletion (if it exists)
	char userDeletePath[150] = "teachers/";
	strcat(userDeletePath, userID);
	strcat(userDeletePath, ".teacher");
	if (remove(userDeletePath) == 0)
	{
      printf("User %s's teacher file has been removed.\n");
	}
    
    //create string for user file deletion
    strcpy(userDeletePath, "users/");
    strcat(userDeletePath, userID);
    strcat(userDeletePath, ".user");
    if (remove(userDeletePath) == 0)
	{
    	printf("User %s has been removed.\n", userID);
	}
	else
	{
		printf("User %s could not be deleted.\n", userID);
		return 1;
	}

	return 0;
}

int changeUserPassword(char carryID[])
{
	clear();

	//get user to change credentials
	printf("Which user's password would you like to change: ");
	char userToChange[100];
	fflush(stdin);
	fgets(userToChange, 100, stdin);
	strtok(userToChange, "\n");

	//check if choice is empty
	if(strcmp(userToChange, "\n") == 0)
	{
		printf("User ID cannot be empty!\n");
		pete();
		return 1;
	}

	//check if user exists
	char userToChangePath[150] = "users/";
	strcat(userToChangePath, userToChange);
	strcat(userToChangePath, ".user");
	FILE* userCheck;
	userCheck = fopen(userToChangePath, "rb");
	if(userCheck == NULL)
	{
		printf("User %s does not exist in the system!\n", userToChange);
		pete();
		return 1;
	}
	fclose(userCheck);

	//get new user password
	char indChar;
    char password[32];
    int passLen=0, i, boCheck=0;
    clear();
    printf("Changing password for user: %s\n", userToChange);
    printf("Please enter a password (max 32 char): ");
    while (1) 
    {
        indChar = getch();
        if (indChar == 0)
        {
            return 1;
        }
        
        if (indChar != '\r' && indChar != '\n' && indChar != '\b')
        {
        	password[passLen] = indChar;
        	passLen++;
        	boCheck++;
        }

        if(indChar == '\b')
        {
        	if(passLen>0)
        	{
        		passLen--;
        	}
        	if(boCheck>0)
        	{
        		boCheck--;
        	}
        }

        clear();
        printf("Changing password for user: %s\n", userToChange);
    	printf("Please enter a password (max 32 char): ");
        for (i = 0; i < passLen; i++)
        {
            printf("*");
        }
        if (indChar == '\n' || indChar == '\r')
        {
            break;
        }
        if(boCheck>=32)
        {
        	printf("\nOverflow detected, cutting password here!\n");
        	break;
        }

    }
    password[passLen] = '\0';

    //write password to file
    userCheck = fopen(userToChangePath, "wb");
	if(userCheck == NULL)
	{
		printf("\nNew user file could not be created.\n");
		printf("The password for %s will not change!\n", userToChange);
		pete();
		return 1;
	}
	fwrite(password, sizeof(char), 50, userCheck);
	fclose(userCheck);

	//check if changing own password
	if(strcmp(userToChange, carryID) == 0)
	{
		printf("\nYou changed your own password, logging out for security purposes!\n");
		pete();
		return -1;
	}

	printf("\nPassword for %s has been changed!\n", userToChange);
	pete();

	fclose(userCheck);
	return 1;
}

int changeStudentPassword(char carryID[])
{
	clear();

	//create path for user file
	char userToChangePath[150] = "users/";
	strcat(userToChangePath, carryID);
	strcat(userToChangePath, ".user");

	//get new user password
	char indChar;
    char password[32];
    int passLen=0, i, boCheck=0;
    clear();
    printf("Changing password for user: %s\n", carryID);
    printf("Please enter a password (max 32 char): ");
    while (1) 
    {
        indChar = getch();
        if (indChar == 0)
        {
            return 1;
        }
        
        if (indChar != '\r' && indChar != '\n' && indChar != '\b')
        {
        	password[passLen] = indChar;
        	passLen++;
        	boCheck++;
        }

        if(indChar == '\b')
        {
        	if(passLen>0)
        	{
        		passLen--;
        	}
        	if(boCheck>0)
        	{
        		boCheck--;
        	}
        }

        clear();
        printf("Changing password for user: %s\n", carryID);
    	printf("Please enter a password (max 32 char): ");
        for (i = 0; i < passLen; i++)
        {
            printf("*");
        }
        if (indChar == '\n' || indChar == '\r')
        {
            break;
        }
        if(boCheck>=32)
        {
        	printf("\nOverflow detected, cutting password here!\n");
        	break;
        }

    }
    password[passLen] = '\0';

    //write password to file
    FILE* userCheck;
    userCheck = fopen(userToChangePath, "wb");
	if(userCheck == NULL)
	{
		printf("\nNew user file could not be created.\n");
		printf("The password for %s will not change!\n", carryID);
		pete();
		return 1;
	}
	fwrite(password, sizeof(char), 50, userCheck);
	fclose(userCheck);

	printf("\nYou changed your own password, logging out for security purposes!\n");
	pete();
	return -1;
}