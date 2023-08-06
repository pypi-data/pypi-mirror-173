import pathlib as pl 
import pandas as pd 
import xlwings as xl

#importing the main grades file. 
d = pl.WindowsPath(r'C:\Users\kevin.omalley\OneDrive - University of Limerick\Documents\GitHub\grading_colation\data\Assignment 2 Due 6th December')
if 'grades.xls' in [i.name for i in d.iterdir()]:
    df = pd.read_excel(d/'grades.xls', header = 0, usecols='A:G')
    df['Grader'] = ''
    df['Comments'] = ''

sn = df.shape[0] # the number of students in the grades sheet.
print(sn)

graders = ['Kev', 'Ryan', 'Aoife', 'Muireann', 'Joe'] #list of graders names
frames = dict.fromkeys(graders, pd.DataFrame())

sg = int(len(graders)) #number of graders
print(sg)

split = sn//sg # the amount of papers each grader gets if evenly distributed

# if sn % sg ==0: # noting what the distribution of papers would be, with leftovers listed if needed. 
#     print(f'Each TA can take {split}')
# else:
#     print(f'Each TA can take {split}, with {sn % sg} left over')



for i in df.index:
    print(i)