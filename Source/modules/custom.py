# STANDARD IMPORTS
import os

# CUSTOM IMPORTS

def line():
    print('------------------------------------------------------------------------')

def make_directory(name):
    os.makedirs(name)

def clear():
    if os.name == 'nt':
        mask = os.system('cls')
    else:
        mask = os.system('clear')

def pete():
    line()
    print('Press ENTER to exit.')
    input()
