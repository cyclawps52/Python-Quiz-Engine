# standard imports
from pathlib import Path
import os

# custom imports 
from modules.custom import *
from modules.auth import *
from modules.classes import *

def quizMenu(carryID, carryClass):
    clear()
    # get all quizes for current user in class and status
    quizPath = str(os.getcwd() + "\\classes\\" + carryClass + "\\quizes")
