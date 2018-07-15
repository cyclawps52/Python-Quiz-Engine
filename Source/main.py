# STANDARD IMPORTS
#import os

# CUSTOM IMPORTS
from modules import *

# global variables
global carryID
carryID = ["NULL"]

permissionLevel = checkIfFirstRun();

while True:
	clear()
	menuChoice = 0
	if(permissionLevel == -2):
		clear()
		permissionLevel = checkIfFirstRun()
	elif(permissionLevel == -1):
		# setup menu options
		menu = {}
		menu['1'] = "Login"
		menu['0'] = "Exit Program"
		menu['D1'] = "DEBUG - Dump Database"
		menu['D2'] = "DEBUG - classCheck()"
		menu['D3'] = "DEBUG - classRegister()"
		menu['D4'] = "DEBUG - classDrop()"
		menu['D5'] = "DEBUG - classCreate()"
		while True:
			# print menu
			options = menu.keys()
			os.system('cls')
			for entry in options:
				print("{0}: {1}".format(entry, menu[entry]))
			print("------------------------------")
			selection = input("Selection: ")
			
			if(selection == '1'):
				permissionLevel = login(carryID)
				break

			elif(selection == '0'):
				exit(0)

			elif(selection == 'D1'):
				debugDumpDatabase()
				break

			elif(selection == 'D2'):
				classList = classCheck()
				break

			elif(selection == 'D3'):
				classRegister()
				break
			
			elif(selection == 'D4'):
				classDrop()
				break

			elif(selection == 'D5'):
				classCreate()
				break

			else:
				print('Invalid option!')
				print('Press ENTER to retry.')
				input()
				break

	elif(permissionLevel == 0):
		

		# setup menu options
		menu = {}
		menu['1'] = "Take Quiz"
		menu['2'] = "Check Grade"
		menu['3'] = "View Quiz Dump"
		menu['4'] = "Change Password"
		menu['0'] = "Logout"
		while True:
			# print menu
			options = menu.keys()
			os.system('cls')
			print('Logged in as {0}'.format(carryID[0]))
			line()
			for entry in options:
				print("{0}: {1}".format(entry, menu[entry]))
			print("------------------------------")
			selection = input("Selection: ")

			if(selection == '1'):
				takeQuiz(carryID)
				break
			elif(selection == '2'):
				gradeViewer(carryID)
				break
			elif(selection == '3'):
				dumpViewer(carryID)
				break
			elif(selection == '4'):
				permissionLevel = changeStudentPassword(carryID)
				break
			elif(selection == '0'):
				permissionLevel = -1
				carryID[0] = "NULL"
				break
			else:
				print('Invalid option!')
				print('Press ENTER to retry.')
				input()
				break

	elif(permissionLevel == 1):

		# setup menu options
		menu = {}
		menu['1'] = "Create Quiz"
		menu['2'] = "Grade and Dump Quiz"
		menu['3'] = "View Quiz Dump"
		menu['4'] = "View Overall Quiz Grade"
		menu['5'] = "Check Student Grade"
		menu['6'] = "Create User"
		menu['7'] = "Retrieve User Password"
		menu['8'] = "Change User Password"
		menu['9'] = "Promote User to Teacher"
		menu['10'] = "Open Delete Console"
		menu['0'] = "Logout"
		while True:
			# print menu
			options = menu.keys()
			os.system('cls')
			print('Logged in as {0} | Teacher mode enabled!'.format(carryID[0]))
			line()
			for entry in options:
				print("{0}: {1}".format(entry, menu[entry]))
			print("------------------------------")
			selection = input("Selection: ")
		
			if(selection == '1'):
				maker()
				break
			elif(selection == '2'):
				grader()
				break
			elif(selection == '3'):
				dumpViewerTeacher()
				break
			elif(selection == '4'):
				overallViewerTeacher()
				break
			elif(selection == '5'):
				gradeViewerTeacher()
				break
			elif(selection == '6'):
				addUser()
				break
			elif(selection == '7'):
				retrievePasswordManual()
				break
			elif(selection == '8'):
				permissionLevel = changeUserPassword(carryID);
				break
			elif(selection == '9'):
				promoteUser()
				break
			elif(selection == '10'):
				permissionLevel = teacherDelete(carryID)
				break
			elif(selection == '0'):
				permissionLevel = -1
				carryID[0] = "NULL"
				break
			else:
				print('Invalid option!')
				print('Press ENTER to retry.')
				input()
				break
exit(0)
