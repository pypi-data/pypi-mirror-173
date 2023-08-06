'''This file is for taking all the completed grading sheets and moving them into the respective students records to be reuploaded to SULIS'''
import pathlib as pl
from shutil import copy

add = input('Address please!')
add.encode('unicode_escape')


rt = pl.Path(add)
dr = rt / 'student records'
gr = rt / 'grading sheets'

recs = [e.name for e in dr.iterdir()]

for folder in dr.iterdir():
    # We're only interested in folders
    if not folder.is_dir():
        continue

    target_file = f"{folder.name} grading sheet.xlsx"
    for file in gr.rglob(target_file):
        #copy(file, folder)
        print(f'{file.name} copied to {folder}')