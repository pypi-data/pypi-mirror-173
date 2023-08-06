''' Created by Kevin O'Malley, July 18 2021.
This file should hold the code for setting up the folder structure creating the module at the start of a semester. It will take the downloaded submissions from and create a "workspace"
for storing and working with the student files. Over time I hope to add functionality that will make creating extrn packs easier, faster and less bias prone.
'''

from pathlib import Path
from shutil import move




def module_setup():
    teaching_root_folder = input('Please copy and paste the full folder address of the folder where you store your teaching files\n')
    module_code = input('Please enter the module code for the class you are teaching (i.e. PS4000)\n')
    module_year = input('Please enter the accademic year for this module (i.e. 2021)\n')
    check_coursework = input("Does this module require students to submit coursework assignments?('y' = yes, 'n' = no)\n")
    
    while True:
        if str.lower(check_coursework) == 'y':
            count_coursework = input('Please enter the number of coursework assignments for this module (positive intergers only please)\n')
            coursework_number = int(count_coursework)
            print(f'OK {int(count_coursework)} coursework assignments\n')
            break
        elif str.lower(check_coursework) == 'n':
            print('OK no coursework')
            break
        else:
            print('Sorry I do not understand.')
            continue
    
    check_exams = input("Does this module have an end of semester exam?('y' = yes, 'n' = no)\n")
    
    while True:
        if str.lower(check_exams) == 'y':
            print(f'OK, this module has an exam.')
            break
        elif str.lower(check_exams) == 'n':
            print('OK no end of semester exam')
            break
        else:
            print('Sorry I do not understand.')
            continue
    module_path_string = f'{teaching_root_folder}\{module_code}-{module_year}'
    module_path_string.encode('unicode escape')
    set_up_check = input(f"Would you like to set up a home folder and subfolders for this module at {module_path_string}?('y' = yes, 'n' = no)\n")
    
    while True:
        if str.lower(set_up_check) == 'y':
            print(f'OK, creating folder at {module_path_string}...')
            
            if Path(module_path_string).exists():
                print(f"I'm sorry, the folder {module_path_string} already exists, please check the folder at that location.")
                exit()
            else:
                assignments = Path(module_path_string) / 'Assignments'
                documents = Path(module_path_string) / 'Module Documents'
                exams = Path(module_path_string) / 'Exam'
                Path(module_path_string).mkdir(parents=True, exist_ok=False)
                documents.mkdir(parents=True, exist_ok=False)
                assignments.mkdir(parents=True, exist_ok=False)

                for i in range(1,coursework_number+1):
                    sub_assignment = assignments / f'Assignment {i}'
                    sub_assignment.mkdir(parents=True, exist_ok=False)
                if check_exams == 'y':
                    exams.mkdir(parents=True, exist_ok=False)
            break
        elif str.lower(set_up_check) == 'n':
            print('OK, you can create your own folder structure, or restart this function if you wish to change details')
            break
        else:
            print('Sorry I do not understand.')
            continue
    print(f'OK I have created the folder {module_path_string}. This contains the sub-folders: {[x.name for x in Path(module_path_string).iterdir()]}\n')
    return(Path(module_path_string))#Maybe you can return more objects or maybe you can be more granular? Or different versions of the function depending on the usecase? 



class Document:
    '''A class for module documents like
    handbooks, assignment briefs, etc.'''
    def __init__(self, name, location, filetype, kind):
        self.name = name
        self.location = location
        self.filetype = filetype

    
    def makeDocument():
        n = input('please enter the name you would like to call the document')
        l = input('please enter the location of the document you would like to use')
        l.encode('unicode escape')
        l = Path(l)
        d = l.suffix
        i = Document(n, l, d)
        print(f'''I have found the document {l.name} in {l.parent}''')

    def copyDocument():
        l = input('please enter the location of the document you would like to use')
        l.encode('unicode escape')
        if Path(l).is_file():
            print('Found it')
        else:
            print('no file here')





