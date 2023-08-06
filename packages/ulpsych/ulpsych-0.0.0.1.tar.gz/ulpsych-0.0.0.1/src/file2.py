import pandas as pd
import pathlib as pl
from shutil import copy

add = input('Address please!')
add.encode('unicode_escape')

folder = pl.Path(add)

recs = [e.name for e in folder.iterdir()]

for (i,file) in enumerate(recs):
    print(f'{i}: {file}')

choice = input('Please select the folder containing the student records \n(press "n" to cancel)')

if int(choice) <=  len(recs):
    sub_folder = folder / recs[int(choice)]
    print(f'You have selected {sub_folder}')
    j = [e.name for e in sub_folder.iterdir()]
    for i in j:
        print(f'{i}\n')
    
elif choice == 'n': 
    print("No choice made, ending process. Please rerun file")
    quit()
    
    