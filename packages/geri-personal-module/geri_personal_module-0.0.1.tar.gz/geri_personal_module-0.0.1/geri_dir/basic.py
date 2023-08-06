import os
import subprocess
import sys

def help():
    print("\n1) download_games()\n2) Choose which one to run: game1, game2 or game3  [run_gameX()]\n")

def print_my_name():
    print("My name is Geri, I made this package")

def simple_addition(a=5,b=4):
    return a+b

def one_liner(string="Well, this is really crazy"):
    """rotates each word"""
    return ''.join( (string.split()[0][::-1]) + ' ' + one_liner(' '.join(string.split()[1:])) ) if len(string) != 0 else ''

def do_a_flip():
    print("Sorry I can't do that right now")

def uninstall_git():
    subprocess.check_call([sys.executable, "-m", "pip", "uninstall", "GitPython"])

def download_games():
    print("Installing gitpython package")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "GitPython"])
    print("Git package installed")
    from git import Repo
    print("Installing games")
    Repo.clone_from("https://github.com/gregoryhornyak/python_package_test.git","/py_games")
    print("Successfully installed")
    
def run_game1():
    """superfighters - multiplayer fight"""
    os.startfile("C:/py_games/games/superfighters_win/Superfighters.exe")

def run_game2():
    """sort the court - singleplayer decision"""
    os.startfile("C:/py_games/games/sort_the_court_win/SortTheCourt.exe")

def run_game3():
    """eggnogg - multiplayer fight"""
    subprocess.run(["C:\Windows\explorer.exe", "C:\py_games\games\eggnogg_plus_win"])
    print("Open source folder")
    os.startfile("C:/py_games/games/eggnogg_plus_win/eggnoggplus.exe")
