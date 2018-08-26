# STANDARD IMPORTS
import os

# CUSTOM IMPORTS
from modules import *

try:
	# global variables
	global carryID
	carryID = ["NULL"]
	global carryClass
	carryClass = ["NULL"]

	permissionLevel = checkIfFirstRun()

	while True:
		clear()
		menuChoice = 0

		if(carryClass[0] == "!DROP!"): # user dropped currently logged in class
			while True:  # until valid class is chosen
				validChoice = False
				classList = classCheck(silent=1, username=carryID[0])
				i = 0
				menu = {}
				for classCode in classList.split(','):
					menu[i] = classCode[:-1]
					i += 1
				menu.pop(0)
				options = menu.keys()

				if(len(menu) == 1):  # only one class, login to it
					if(menu[1][0] == "$"):
						print("Dropped current class, switching to only remaining class \"{0}\".".format(menu[1][1:]))
					else:
						print("Dropped current class, switching to only remaining class \"{0}\".".format(menu[1]))
					print("Press ENTER to continue.")
					input()
					classChoice = menu[1]
					carryClass[0] = classChoice
					break

				elif(len(menu) == 0):
					# no classes registered, begin registration
					print("You have dropped all your currently registered classes.".format(username))
					print("Press ENTER to register for a class.")
					input()
					classRegister(student=1, username=username)

				else:
					clear()
					print("You dropped your currently logged in class.")
					print("Please select a class to login to: ")
					line()
					for entry in options:
						if(menu[entry][0] == "$"):
							print("{0}: {1} | TEACHER MODE ENABLED".format(entry, menu[entry][1:]))
						else:
							print("{0}: {1}".format(entry, menu[entry]))
					try:
						classChoice = int(input("Selection: "))
					except:
						print("Invalid selection. Press ENTER to try again.")
						input()
					try:
						classChoice = menu[classChoice]
						validChoice = True
					except:
						print("Invalid selection. Press ENTER to try again.")
						input()
					if(validChoice):
						carryClass[0] = classChoice
						break

		if(permissionLevel == -2):
			clear()
			permissionLevel = checkIfFirstRun()
		elif(permissionLevel == -1): # not logged in
			# setup menu options
			menu = {}
			menu['LI'] = "Login"
			menu['EP'] = "Exit Program"

			while True:
				# print menu
				options = menu.keys()
				clear()
				for entry in options:
					print("{0}: {1}".format(entry.ljust(3), menu[entry]))
				line()
				selection = input("Selection: ").upper()
				
				if(selection == 'LI'):
					permissionLevel = login(carryID, carryClass)
					break

				elif(selection == 'EP'):
					os.system('exit')
					exit(0)

				else:
					print('Invalid option!')
					print('Press ENTER to retry.')
					input()
					break

		elif(permissionLevel == 0): # student permissions
			# setup menu options
			menu = {}
			menu['QM'] = "Quiz Menu"

			menu['CR'] = "Register for Class"
			menu['CV'] = "View Registered Classes"
			menu['CD'] = "Drop Class"
			
			menu['CC'] = "Change Class"
			menu['LO'] = "Logout"
			while True:
				# print menu
				options = menu.keys()
				clear()
				print('Logged in as \"{0}\" | Class: \"{1}\"'.format(carryID[0], carryClass[0]))
				line()
				for entry in options:
					print("{0}: {1}".format(entry.ljust(3), menu[entry]))
				line()
				selection = input("Selection: ").upper()

				if(selection == 'QM'):
					quizMenu(carryID=carryID[0], carryClass=carryClass[0])
					break
				elif(selection == 'CR'):
					classRegister(student=1, username=carryID[0])
					break
				elif(selection == 'CV'):
					classCheck(username=carryID[0])
					break
				elif(selection == 'CD'):
					classDrop(username=carryID[0], carryClass=carryClass[0])
					break

				elif(selection == 'CC'):
					permissionLevel, carryClass[0] = changeClass(carryID[0], carryClass[0])
					break

				elif(selection == 'LO'):
					permissionLevel = -1
					carryID[0] = "NULL"
					carryClass[0] = "NULL"
					break
				else:
					print('Invalid option!')
					print('Press ENTER to retry.')
					input()
					break

		elif(permissionLevel == 1): # teacher permissions
			# setup menu options
			menu = {}
			menu['NU'] = "New User"
			menu['NC'] = "New Class"
			menu['NQ'] = "New Quiz"

			menu['QG'] = "Quiz Grade" 
			menu['QM'] = "Graded Quiz Menu"
			menu['DQ'] = "Delete Quiz"
			menu['QL'] = "Quiz Locking"
			
			menu['CR'] = "Register Self for Class"
			menu['CV'] = "View Registered Classes for Self"
			menu['CD'] = "Drop Class for Self"

			menu['CRO'] = "Register Class for Other User"
			menu['CVO'] = "View Registered Classes for Other User"
			menu['CDO'] = "Drop Class for Other User"

			menu['CC'] = "Change Class"
			menu['LO'] = "Logout"

			while True:
				# print menu
				options = menu.keys()
				clear()
				print('Logged in as \"{0}\" | Class: \"{1}\" | Teacher mode enabled!'.format(carryID[0], carryClass[0][1:]))
				line()
				for entry in options:
					print("{0}: {1}".format(entry.ljust(4), menu[entry]))
				line()
				selection = input("Selection: ").upper()
			
				if(selection == 'NU'):
					addUser()
					break
				elif(selection == 'NC'):
					classCreate(username=carryID[0])
					break
				elif(selection == 'NQ'):
					makeQuiz(carryID)
					break

				elif(selection == "QG"):
					gradeMenu(carryClass=carryClass[0])
					break
				elif(selection == "QM"):
					gradedQuizMenu(carryClass=carryClass[0])
					break
				elif(selection == "DQ"):
					deleteQuiz(carryClass=carryClass[0])
					break
				elif(selection == 'QL'):
					lockQuiz(carryClass=carryClass[0])
					break
				
				elif(selection == 'CR'):
					classRegister(student=1, username=carryID[0])
					break
				elif(selection == 'CV'):
					classCheck(username=carryID[0])
					break
				elif(selection == 'CD'):
					carryClass[0] = classDrop(username=carryID[0], carryClass=carryClass[0])
					break

				elif(selection == 'CRO'):
					classRegister()
					break
				elif(selection == 'CVO'):
					classCheck()
					break
				elif(selection == 'CDO'):
					classDrop()
					break

				elif(selection == 'CC'):
					permissionLevel, carryClass[0] = changeClass(carryID[0], carryClass[0])
					break
				elif(selection == 'LO'):
					permissionLevel = -1
					carryID[0] = "NULL"
					carryClass[0] = "NULL"
					break

				else:
					print('Invalid option!')
					print('Press ENTER to retry.')
					input()
					break
	exit(0)
except KeyboardInterrupt:
	print("Keyboard interrupt detected, closing SSH session.")
	exit(0)