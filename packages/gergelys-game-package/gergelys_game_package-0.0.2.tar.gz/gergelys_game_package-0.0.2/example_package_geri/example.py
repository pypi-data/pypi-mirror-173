import os
from git import Repo
import subprocess
import sys

def install():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "GitPython"])

def print_my_name():
    print("My name is Geri, I made this package")

def simple_addition(a,b):
    return a+b

def run_game():
    install()
    Repo.clone_from("https://github.com/gregoryhornyak/python_package_test.git","/py_game")
    os.startfile("C:/py_game/game/SortTheCourt.exe")