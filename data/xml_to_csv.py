import csv
import os
import xml.dom.minidom

anno_path = "VOCdevkit2007/VOC2007/Annotations/"
path = "VOCdevkit2007/VOC2007/"
split_path = "VOCdevkit2007/VOC2007/ImageSets/Main/"

train_path = "csv/train_annots.csv"
val_path = "csv/val_annots.csv"
class_path = "csv/class_list.csv"

with open(class_path,"w",newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["havestar","1"])


train_list = open(split_path+"val.txt","r")
line = True
while line:
    line = train_list.readline()
    line = line[:-1]
    print(line)
    if line=="":
        continue
    dom = xml.dom.minidom.parse(anno_path+line+".xml")
    xmin=dom.getElementsByTagName("xmin")
    xmin = int(float(xmin[0].firstChild.data))
    ymin=dom.getElementsByTagName("ymin")
    ymin = int(float(ymin[0].firstChild.data))
    xmax=dom.getElementsByTagName("xmax")
    xmax = int(float(xmax[0].firstChild.data))
    ymax=dom.getElementsByTagName("ymax")
    ymax = int(float(ymax[0].firstChild.data))
    img = line+".jpg"

    with open(val_path,"a",newline="") as f:
        writer = csv.writer(f)
        writer.writerow([line,xmin,ymin,xmax,ymax,"havestar"])
train_list.close()
print("over!!!")