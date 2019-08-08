#%%
import os
m4a_path = r"C:\Users\ZhuangBin.FLASHIELD\OneDrive\Temp"
print(m4a_path)
m4a_file = os.listdir(m4a_path)
print(m4a_file)
for i in m4a_file:
    i.split('.')[-1]
    prefix = i[0:i.rfind('.')]
    ext = i[i.rfind('.')+1:]
    if ext in ('mp3','m4a','wmv'):
        print(prefix,ext)