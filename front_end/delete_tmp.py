import os
    
for file_name in os.listdir('result\\'):
    if not file_name.endswith('merge_list.txt'):
        os.remove('result\\' + file_name)
    
for file_name in os.listdir('download\\'):
    os.remove('download\\' + file_name)