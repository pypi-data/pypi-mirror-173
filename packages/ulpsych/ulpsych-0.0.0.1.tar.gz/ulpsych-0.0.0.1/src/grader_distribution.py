import pandas as pd
import xlwings as xl
import pathlib as pl


# file = pl.WindowsPath(r'C:\Users\kevin.omalley\OneDrive - University of Limerick\Teaching\PS4041-2021(2)\Assignments\Assignment 2\Assignment 2 Due 6th December\grades.xls')

df = pd.read_excel(file)

graders = ['Kev', '', 'Ryan', '', 'Joe']



df['Grader'] = ''
df.loc[df.sample(n=30).index, 'Grader'] = 'Ryan'
r = df[df['Grader']=='Ryan'].copy()
r.to_csv(r'C:\Users\kevin.omalley\OneDrive - University of Limerick\Teaching\PS4041-2021(2)\Assignments\Assignment 2\Assignment 2 Due 6th December\ryan.csv', index = False)
df = df[df.Grader != 'Ryan']

df.loc[df.sample(n=25).index, 'Grader'] = 'Muirean'
m = df[df['Grader']=='Muirean'].copy()
m.to_csv(r'C:\Users\kevin.omalley\OneDrive - University of Limerick\Teaching\PS4041-2021(2)\Assignments\Assignment 2\Assignment 2 Due 6th December\Muirean.csv', index = False)
df = df[df.Grader != 'Muirean']

df.loc[df.sample(n=25).index, 'Grader'] = 'Aoife'
a = df[df['Grader']=='Aoife'].copy()
a.to_csv(r'C:\Users\kevin.omalley\OneDrive - University of Limerick\Teaching\PS4041-2021(2)\Assignments\Assignment 2\Assignment 2 Due 6th December\Aoife.csv', index = False)
df = df[df.Grader != 'Aoife']

df.loc[df.sample(n=10).index, 'Grader'] = 'Joe'
j = df[df['Grader']=='Joe'].copy()
j.to_csv(r'C:\Users\kevin.omalley\OneDrive - University of Limerick\Teaching\PS4041-2021(2)\Assignments\Assignment 2\Assignment 2 Due 6th December\Joe.csv', index = False)
df = df[df.Grader != 'Joe']
df['Grader'] = 'Kev'
df.to_csv(r'C:\Users\kevin.omalley\OneDrive - University of Limerick\Teaching\PS4041-2021(2)\Assignments\Assignment 2\Assignment 2 Due 6th December\kev.csv', index = False)


combined = pd.concat([j,df,m,a,r])
print(len(combined))
print(len(r))
print(len(m))
print(len(a))
print(len(j))
print(len(df))