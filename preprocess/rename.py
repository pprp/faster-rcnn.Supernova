import os
import shutil
path = './ALL/'
outpath = "./rename/"
outb = "./b/"
outc = "./c/"

for f in os.listdir(path):
    print(f)
    name,ext = os.path.splitext(f)
    a,ext2 = name.split('_')
    if ext2.endswith('b'):
        print(outb+f)
        shutil.copy(path+f,outb+f)
    elif ext2.endswith('c'):
        print(outc+f)
        shutil.copy(path+f,outc+f)
    print(a)
    #shutil.copy(path+f,outpath+a+ext)