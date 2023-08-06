'''
Created by Kev 'Sp1d3r-Z3r0' O'Malley (kevin.omalley[@]ul.ie, Github = 'https://github.com/spider-z3r0'), 19/07/2021, as part of the ULpsych grader bot package.

Contains a function that check if the user has downloaded the submissions from sulis and returns the directory address as a Path object and a unicode-escaped string.
'''
from pathlib import Path 

def sulis_check():
    while True: #taking the first input to identify the Sulis download.
        su_download_check = input("\nHave you downloaded the student submissions from sulis? \n('y' = yes, 'n' = no, type = 'exit' if you wish to close the program)\n")

        if str.lower(su_download_check) == 'y':#if the user states that they have downloaded the submissions from sulis
            su_download_address = input('Excellent, please enter the *full* folder location of the sulis download\n')# taking the string version of the submissions directory
            su_download_address.encode('unicode_escape')# turning that string into a raw string so that it can be used in Path
            su_download_path = Path(su_download_address)# making directory into a Path Object

            if su_download_path.exists():# If the directory actually exists (i.e. if actually downloaded and entered into the terminal correctly)
                print(f"You have selected '{str(su_download_address)}' as the folder containing the student records.") # confirming the address
                return(su_download_address, su_download_path)# returning both the Path and Raw-string objects.
            else:
                print("Sorry, I can't find that file, please check the folder address and try again")# telling the user they can't find the file and making a suggestion
                pass
        elif str.lower(su_download_check) == 'n': # if the download hasn't happened yet
            print("OK, please go the assignment tab on the Sulis module and download *all* submissions. When you have done this come back and we'll start again.")
            exit()#closing the program altogether
        elif str.lower(su_download_check) == 'exit':#if the user decides to close the program and not progress
            print("OK, I'll be here when you're ready to start again.")
            exit()#closing the program altogether
        else:
            print("I don't understand your input. Please type 'y' or 'n' only.")
            pass
    
