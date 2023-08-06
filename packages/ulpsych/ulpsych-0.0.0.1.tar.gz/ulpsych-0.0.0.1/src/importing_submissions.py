'''This file is built to allow faculty to quickly generate records of student submission upon downloading them from sulis.'''

import pathlib as pl
import pandas as pd
from shutil import copy

dir_name = input('Please specify the folder address of the Sulis download')
dir_name.encode('unicode_escape')

main_directory = pl.Path(dir_name)
choices = [e.name for e in main_directory.iterdir()]

for (i,file) in enumerate(choices):
    print(f'{i}: {file}')


choice = input('Please select the folder containing the student records \n(press "n" to cancel)')


if int(choice) <=  len(choices):
    sub_folder = main_directory / choices[int(choice)]
    print(f'You have selected {sub_folder}')
    
elif choice == 'n': 
    print("No choice made, ending process. Please rerun file")
    quit()

students = [e.name for e in sub_folder.iterdir()]

df = pd.DataFrame({'col1':students})


df[['Last', 'First', 'Number']] = df.col1.str.split(r"\(|," , expand=True)
df['Number'] = df['Number'].str.rstrip(')')
df['Grader'] = ''
df['Mark'] = ''
df['Letter Grade'] = ''
df = df.drop(['col1'], axis = 1)

df.to_excel(main_directory / 'class list grading sheet.xlsx', index=False)

print(df.head()) 
