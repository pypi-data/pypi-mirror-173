import pandas as pd
import xlwings as xl
import pathlib as pl

rt = pl.WindowsPath(r'C:\Users\kevin.omalley\OneDrive - University of Limerick\Teaching\PS4041-2021(2)\Assignments\Assignment 2\Assignment 2 Due 6th December')

rts = [e for e in rt.iterdir() if '.xlsx'  in e.name]



for i in rts:
    print(i)

del rts[1]
del rts[2]
print('deleting unneeded')


for i in rts:
    print(i)

df = pd.DataFrame()

for f in rts:
    data=pd.read_excel(f)
    df = df.append(data)

#df.to_excel(r'C:\Users\kevin.omalley\OneDrive - University of Limerick\Teaching\PS4041-2021(2)\Assignments\Assignment 2\Assignment 2 Due 6th December\recollected.xlsx', index = False)

