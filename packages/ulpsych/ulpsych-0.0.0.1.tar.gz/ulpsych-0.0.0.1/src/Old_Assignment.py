'''Created by Kevin O'Malley 12/04/2022 
This holds the old Assignment function code incase it is needed in future.
'''



from pathlib import Path
import pandas as pd
from shutil import copy, move
import xlwings as xlw


class Assignment:
   '''A class that allows us to work with assignments''' 
   def __init__(self, location):
      try:   
         if Path(f'{location}').exists() or Path(f'{location}/ Assignments').exists():
            self.location = location         
         else:
            raise FileNotFoundError('No folder')
      except FileNotFoundError:
            print(f'''There is no assignments folder at {location} you can 
            1. check the spelling
            2. manually make the folder and try again
            3. run the module set_up function for this module *if you have not done so already*
            ''')
            pass

   def import_subs(self):
      """This function imports the submissions once they have been downloaded from sulis"""
      sub_dir = input('Please enter the location of the downloaded submissions: \n')
      sub_dir.encode('unicode escape')
      try:
         if Path(f'{sub_dir}').is_dir():
            move(sub_dir, self.location)
            e = Path(f'{Path(self.location)}/{Path(sub_dir).name}')
            e = e.rename(f'{self.location}\\submissions')
            print(f"\nSubmissions moved to: \n {str(e)}\n please verify the move by checking the assignment folder.\n")
            return(Path(e))
         else:
            raise FileNotFoundError('No folder')
      except FileNotFoundError:
         print("""There is no folder here, check the location you have enetered again""")
         pass

   def mk_grading_sheets(self):
      """This reads the submissions folder and takes the names of the students """
      students = [e.name for e in Path(f'{self.location}\submissions').iterdir()]
      df = pd.DataFrame({'col1':students})
      df[['Last', 'First', 'Number']] = df.col1.str.split(r"\(|," , expand=True)
      df['Number'] = df['Number'].str.rstrip(')')
      df['Grader'] = ''
      df['Mark'] = ''
      df['Letter Grade'] = ''
      df = df.drop(['col1'], axis = 1)

      df.to_excel(Path(f'{self.location}\\submissions\\class list grading sheet.xlsx'), index=False)