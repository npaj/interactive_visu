import os
import pandas as pd
import numpy as np

df = pd.DataFrame()

x = np.random.randn(5)
y = np.random.randn(5)
target_list = np.random.randint(10, size=(5))
filename_list = [f'{k}.txt' for k in range(1,6)]

folder = 'data'
if not os.path.exists(folder):
    os.makedirs(folder)
    print(f"{folder} folder created.")
    
for k in filename_list:
    np.savetxt(os.path.join(folder, k), np.random.randn(8000))

df['x'] = x
df['y'] = y
df['target'] = target_list
df['filename'] = filename_list

df.to_csv('out.csv')

print('done')