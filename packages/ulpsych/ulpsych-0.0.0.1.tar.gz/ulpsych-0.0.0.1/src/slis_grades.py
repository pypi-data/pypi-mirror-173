import pandas as pd
import pathlib as pl
import xlwings as xl

s = pl.WindowsPath(r'C:\Users\kevin.omalley\OneDrive - University of Limerick\Teaching\PS4041-2021(2)\Assignments\Assignment 2\Assignment 2 Due 6th December\grades.xls')
r = pl.WindowsPath(r'C:\Users\kevin.omalley\OneDrive - University of Limerick\Teaching\PS4041-2021(2)\Assignments\Assignment 2\Assignment 2 Due 6th December\recollected.xlsx')


dfs = pd.read_excel(s, header = 0, usecols = 'A:G')
dfr = pd.read_excel(r, header = 0, usecols = 'A:H')

dfs.to
