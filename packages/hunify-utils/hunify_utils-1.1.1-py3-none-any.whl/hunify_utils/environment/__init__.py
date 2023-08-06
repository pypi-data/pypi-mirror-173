import os
import sys


def get_current_path() -> str:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return dir_path


def get_main_dir() -> str:
    dir_path = os.path.dirname(os.path.realpath(sys.argv[0]))
    return dir_path


def get_work_dir() -> str:
    dir_path = os.getcwd()
    return dir_path
