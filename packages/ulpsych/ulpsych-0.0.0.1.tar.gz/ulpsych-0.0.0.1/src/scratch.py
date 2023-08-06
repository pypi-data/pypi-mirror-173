import pandas as pd
import numpy as np

#making the df
df = pd.DataFrame()
df['ids'] = np.random.randint(1, 140, size=140)
df['group_leader'] = ''


# list of leader names
leaders = ['John', 'Paul', 'George', 'Ringo', 'Apu']

frames = dict.fromkeys('group_leaders', pd.DataFrame())

for i in frames.keys(): #allows me to fill the cells with the string key?
    df.loc[df.sample(n=28).index, 'group_leader'] = str(i)
    frames[i].update(df[df['group_leader']== str(i)].copy())#also tried append()
    print(frames[i].head())
    df = df[df['group_leader'] != str(i)]
    print(f'df now has {df.shape[0]} ids left') #just in case there's a remainder of ids