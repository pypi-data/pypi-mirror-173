import os
import subprocess
import sys

print("Installing gitpython package")
subprocess.check_call([sys.executable, "-m", "pip", "install", "GitPython"])
print("Git package installed")

from git import Repo

def print_my_name():
    print("My name is Geri, I made this package")

def simple_addition(a=5,b=4):
    return a+b

def do_a_flip():
    print("Sorry I can't do that right now")

def uninstall_git():
    subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "GitPython"])

def run_game():
    print("Installing game")
    Repo.clone_from("https://github.com/gregoryhornyak/python_package_test.git","/py_game")
    print("Running game:")
    os.startfile("C:/py_game/game/SortTheCourt.exe")