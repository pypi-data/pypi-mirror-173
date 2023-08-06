import pandas as pd
import xlwings as xl
import pathlib as pl
import pyperclip as pc




file = pl.WindowsPath(r'C:\Users\kevin.omalley\OneDrive - University of Limerick\Teaching\PS4041-2021(2)\Assignments\Assignment 2\Assignment 2 Due 6th December\grades.xls')

df = pd.read_excel(file)

def find_lates(frame):
    """Find the lats submissions and prepare the email addresses"""
    lates = frame[frame['Late submission']== 'Unknown'].copy()
    emails =[]
    for i in lates['Display ID']:
        emails.append(f'{i}@studentmail.ul.ie')
    def list_to_clipboard(output_list):
        """ Check if len(list) > 0, then copy to clipboard """
        if len(output_list) > 0:
            pc.copy('\n'.join(output_list))
            print(f'{output_list} Copied to clipboard: ')
        else:
            print("There was nothing on the clipboard")
    
    list_to_clipboard(emails)


find_lates(df)