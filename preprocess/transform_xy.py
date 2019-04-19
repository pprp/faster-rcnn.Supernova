import numpy as np
import os
import cv2
import csv

path = "./test/"
CROP_SIZE = 600

csv_write = csv.writer(open('scale.csv','w',newline=''))

for f in os.listdir(path):
	name,_ = f.split("_")
	img = cv2.imread(path+f)
	sp = img.shape
	x = sp[1] / CROP_SIZE
	y = sp[0] / CROP_SIZE
	csv_write.writerow([name,x,y])
print("generate scale.csv over")

ref = csv.reader(open('list.csv','r'))
scale = csv.reader(open('scale.csv','r'))

submitfile = "./scale.csv"
listfile = "./list.csv"

fsubmit = open(submitfile,'r')
flist = open(listfile,'r')

reader_submit = csv.reader(fsubmit)
reader_list = csv.reader(flist)

reader_submit = list(reader_submit)[1:]
reader_list = list(reader_list)[1:]

out = csv.writer(open('./position.csv','w',newline=''))



def getID(name):
    for i in range(len(reader_list)):
        if reader_list[i][0] == name:
            return i
    return 0



# for name,x,y,starname in reader_list:
    # if starname == "newtarget" or starname == "isstar" or starname =="asteroid" or starname == "isnova" or starname == "known":
    #     fName = "havestar"
    #     total = total + 1
    # else:
    #     fName = "nostar"


for name,x,y in reader_submit:
    tmp = reader_list[getID(name)]
    if tmp:
        tx = int(tmp[1])
        ty = int(tmp[2])
    x = float(x)
    y = float(y)
    outx = x*tx
    outy = y*ty
    out.writerow([name,outx,outy])
print('over')
			
