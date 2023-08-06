'''Created by Kev O Malley August 7th 2021 
This will hold all code related to assignments. 
'''

from pathlib import Path
import pandas as pd
import numpy as np
import xlwings as xlw
import chardet as ch




class Assignment:
   '''A class that allows us to work with assignments''' 
   def __init__(self, location):
      try:   
         if Path(f'{location}').exists() or Path(f'{location}/ Assignments').exists():
            self.location = Path(location)     
         else:
            raise FileNotFoundError('No folder')
      except FileNotFoundError:
            print(f'''There is no assignments folder at {location} you can 
            1. check the spelling
            2. manually make the folder and try again
            3. run the module set_up function for this module *if you have not done so already*
            ''')
            pass

   def sulis_import(self, name, filetype = '.csv'):
      """This function imports the grades sheet once it has been downloaded from sulis"""
      if str.lower(filetype) == '.csv':
         t = self.location / str(name) / 'grades.csv'
         if t.exists():
            with open(t, 'rb') as f:
               enc = ch.detect(f.read())  # or readline if the file is large
            grades = pd.read_csv(t,skiprows = [0,1], encoding = enc['encoding'])
      elif str.lower(filetype) == '.xlsx':
         t = self.location / str(name) / 'grades.xlsx'
         if t.exists():
            grades = pd.read_excel(t)
      elif str.lower(filetype) ==  '.xls':
         t = self.location / str(name) / 'grades.xls'
         if t.exists():
            grades = pd.read_excel(t)
      return(grades)


   def prep_groups(self, df):
      '''This function is meant to take in groups sheets
      and structure the grades file so that groups can be assigned to a grader
      built with PS4034/6022 in mind but needs to expand. '''

   def distribute(self, graders, df):
      '''Take in the grades file and distribute
      students to the graders'''
      if type(graders) != list:
         print('Please give a list of grading assistant names')
      else:
         split = len(df)/len(graders)
         m_graders = np.repeat(graders, np.ceil(len(df) / len(graders)))
         np.random.shuffle(m_graders)
         df['grader'] = m_graders[:len(df)]
         for i in graders:
            s = df[df['grader'] == i]
            s.to_excel(Path(f'{self.location}/{i}.xlsx'), index=False)
         # This needs to be expanded to accomodate group assignments where people would be grouped together. 


         
         
         
      



