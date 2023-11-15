import os

current_working_directory = os.getcwd()
entries = os.scandir(current_working_directory)

entries = os.scandir(os.getcwd())
