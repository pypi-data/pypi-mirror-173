'''
Created by Kev 'Sp1d3r-Z3r0' O'Malley (kevin.omalley[@]ul.ie, Github = 'https://github.com/spider-z3r0'), 19/07/2021, as part of the ULpsych grader bot package.
Contains a function that 
1: checks if the user wants to move the submission sub-directories to a new directory
2: checks if the target directory already exists
3: creates the target directory if it doesn't
4: or leaves the submission sub-directories in thier original location if the user prefers  
'''

from pathlib import Path
from shutil import move




def move_submissions(a):
    while True:
        move_check = input('''
        Would you like to move the submission from thier current location to a new directory\n('y' = yes, 'n' = no, type = 'exit' if you wish to close the program)\n
        ''')
        if str.lower(move_check) == 'y':
            w_space_input = input("OK, please type the location where you would like me to move the student submissions")
            w_space_input.encode('unicode escape')
            w_space_directory = Path(w_space_input)
            if not w_space_directory.exists():
                print("The location you have specified doesn't exist, would you likye me to make it for you?\n")
                create_w_space = input("('y' = yes, 'n' = no, 'exit' = you wish to close the program)\n")
                if str.lower(create_w_space) == 'y':
                    w_space_directory.mkdir(parents=True, exist_ok=False)
                    move(a, w_space_input)
                    return(move_check, w_space_directory)
                    break
            else:
                print("OK, I'm moving the student submissions to '{w_space_input}'now\n")
                move(a, w_space_input)
                print("\nFolders moved")
                return(move_check, w_space_directory)
                break
        else:
            print(f"OK we can leave them where them in '{a}' for now")
            return(move_check, a)
            break
        
