import pathlib as pl
import os
from shutil import copy, move


print("S'all good homie")

over_dir = pl.WindowsPath(r'C:\Users\kevin.omalley\OneDrive - University of Limerick\Documents\GitHub\grading_colation\data\Submissions')
a = [e.name for e in over_dir.iterdir()]

for i in a:
    sub_dir = over_dir / str(i)
    fb = sub_dir / 'Feedback Attachment(s)'
    b = [e for e in sub_dir.iterdir()]
    for j in b:
        if '.xlsx' in j.name:
            move(j, fb)

