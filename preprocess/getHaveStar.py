import os
import csv
import shutil

f = open("./list.csv","r")
reader = csv.reader(f)

reader = list(reader)[1:]
cnt = 0
for name,x,y,judge in reader:
    if judge in ["newtarget","isstar","asteroid","isnova","known"]:
        print(name)
        cnt += 1
        print(cnt)
        shutil.copy("./3channels/"+name+".jpg","./VOCdevkit2007/havestar/"+name+".jpg")
