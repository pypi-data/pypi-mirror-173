import os
import subprocess
import sys
subprocess.check_call([sys.executable, "pip", "install", "GitPython"])

from git import Repo

def print_my_name():
    print("My name is Geri, I made this package")

def simple_addition(a=5,b=4):
    return a+b

def run_game():
    Repo.clone_from("https://github.com/gregoryhornyak/python_package_test.git","/py_game")
    os.startfile("C:/py_game/game/SortTheCourt.exe")