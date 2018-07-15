//STANDARD
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//PUSHED FEATURES
#include "custom/custom.h"
#include "grader/grader.h"
#include "maker/maker.h"
#include "takeQuiz/takeQuiz.h"
#include "auth/auth.h"
#include "viewer/viewer.h"
#include "delete/delete.h"

//MAIN
int main()
{
	setbuf(stdout, NULL);
	int menu;
	char carryID[100]="NULL";

	int permissionLevel = -1;

	clear();
	permissionLevel = checkIfFirstRun();
	
	while(1)
	{
		clear();

		int menuChoice;
		if(permissionLevel == -2)
		{
			clear();
			permissionLevel = checkIfFirstRun();
		}
		else if(permissionLevel == -1)
		{
			printf("No user logged in!\n");
			line();

			printf("1. Login\n");
			printf("0. Exit Program\n");
			printf("\n\tChoice: ");
			if(scanf("%d", &menuChoice) == 0)
			{
				printf("Invalid option!\n");
				printf("Press ENTER to retry.\n");
				menuChoice = 1337;
				fflush(stdin);
				getchar();
			}
			switch(menuChoice)
			{
				case 1:
					permissionLevel = login(carryID);
					break;
				case 0:
					return 0;
				case 1337:
					break;
				default:
					printf("Invalid option!\n");
					printf("Press ENTER to retry.\n");
					fflush(stdin);
					getchar();
			}
		}
		else if(permissionLevel == 0)
		{
			printf("Logged in as: %s\n", carryID);
			line();

			printf("1. Take Quiz\n");
			printf("2. Check Grade\n");
			printf("3. View Quiz Dump\n");
			printf("\n");

			printf("4. Change Password\n");
			printf("0. Logout\n");
			printf("\n\tChoice: ");
			if(scanf("%d", &menuChoice) == 0)
			{
				printf("Invalid option!\n");
				printf("Press ENTER to retry.\n");
				menuChoice = 1337;
				fflush(stdin);
				getchar();
			}

			switch(menuChoice)
			{
				case 1:
					takeQuiz(carryID);
					break;
				case 2:
					gradeViewer(carryID);
					break;
				case 3:
					dumpViewer(carryID);
					break;
				case 4:
					permissionLevel = changeStudentPassword(carryID);
					break;
				case 0:
					permissionLevel = -1;
					strcpy(carryID, "NULL\0");
					break;
				case 1337:
					break;
				default:
					printf("Invalid option!\n");
					printf("Press ENTER to retry.\n");
					fflush(stdin);
					getchar();
			}
		}
		else if(permissionLevel == 1)
		{
			printf("Logged in as: %s\n", carryID);
			printf("Teacher mode enabled!\n");
			line();

			printf("1. Create Quiz\n");
			printf("\n");

			printf("2. Grade & Dump Quiz\n");
			printf("3. View Quiz Dump\n");
			printf("4. View Overall Quiz Grade\n");
			printf("5. Check Student Grade\n");
			printf("\n");

			printf("6. Create User\n");
			printf("7. Retrieve User Password\n");
			printf("8. Change User Password\n");
			printf("9. Promote User to Teacher\n");
			printf("\n");

			printf("10. Open Delete Console\n");
			printf("0. Logout\n");
			
			printf("\n\tChoice: ");
			if(scanf("%d", &menuChoice) == 0)
			{
				printf("Invalid option!\n");
				printf("Press ENTER to retry.\n");
				menuChoice = 1337;
				fflush(stdin);
				getchar();
			}

			switch(menuChoice)
			{
				case 1:
					maker();
					break;
				case 2:
					grader();
					break;
				case 3:
					dumpViewerTeacher();
					break;
				case 4:
					overallViewerTeacher();
					break;
				case 5:
					gradeViewerTeacher();
					break;
				case 6:
					addUser();
					break;
				case 7:
					retrievePasswordManual();
					break;
				case 8:
					permissionLevel = changeUserPassword(carryID);
					break;
				case 9:
					promoteUser();
					break;
				case 10:
					permissionLevel = teacherDelete(carryID);
					break;

				case 0:
					permissionLevel = -1;
					strcpy(carryID, "NULL\0");
					break;
				case 1337:
					break;
				default:
					printf("Invalid option!\n");
					printf("Press ENTER to retry.\n");
					fflush(stdin);
					getchar();
			}
		}
	}
	
	return 0;
}