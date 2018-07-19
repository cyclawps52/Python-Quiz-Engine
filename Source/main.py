# STANDARD IMPORTS
#import os

# CUSTOM IMPORTS
from modules import *

# global variables
global carryID
carryID = ["NULL"]
global carryClass
carryClass = ["NULL"]

permissionLevel = checkIfFirstRun()

while True:
	clear()
	menuChoice = 0
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
				exit(0)

			else:
				print('Invalid option!')
				print('Press ENTER to retry.')
				input()
				break

	elif(permissionLevel == 0): # student permissions
		# setup menu options
		menu = {}
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

			if(selection == 'CR'):
				classRegister(student=1, username=carryID[0])
				break
			elif(selection == 'CV'):
				classCheck(username=carryID[0])
				break
			elif(selection == 'CD'):
				classDrop(carryID[0])
				break

			elif(selection == 'CC'):
				permissionLevel = changeClass(carryID[0], carryClass[0])
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
		
		menu['CR'] = "Register Self for Class"
		menu['CV'] = "View Registered Classes for Self"
		menu['CD'] = "Drop Class for Self"

		menu['CRO'] = "Register Class for Other User"
		menu['CVO'] = "View Registered Classes for Other User"
		menu['CDO'] = "Drop Class for Other User"

		menu['CC'] = "Change Class"
		menu['LO'] = "Logout"

		menu['DB1'] = "DEBUG: Dump Database"

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
			
			elif(selection == 'CR'):
				classRegister(student=1, username=carryID[0])
				break
			elif(selection == 'CV'):
				classCheck(username=carryID[0])
				break
			elif(selection == 'CD'):
				classDrop(carryID[0])
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
				permissionLevel = changeClass(carryID[0], carryClass[0])
				break
			elif(selection == 'LO'):
				permissionLevel = -1
				carryID[0] = "NULL"
				carryClass[0] = "NULL"
				break

			elif(selection == 'DB1'): # DEBUG
				debugDumpDatabase() # DEBUG
				break #DEBUG

			else:
				print('Invalid option!')
				print('Press ENTER to retry.')
				input()
				break
exit(0)
