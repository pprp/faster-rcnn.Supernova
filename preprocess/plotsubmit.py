import cv2
import csv
import random
import os

new = "./kind/"
cate = "./kind/"

def plot_one_box(x, img, color=None, label=None, line_thickness=None,rank=0):  # Plots one bounding box on image img
    tl = 2#line_thickness or round(0.002 * max(img.shape[0:2])) + 1  # line thickness
    color = color or [random.randint(0, 255) for _ in range(3)]
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
    cv2.rectangle(img, c1, c2, color, tl)
    if label:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(img, c1, c2, color, -1)  # filled
        cv2.putText(img, label+":"+str(rank), (c1[0], c1[1] - 2), 0, tl / 4, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)

filename = "./submit.csv"
f = open(filename)
reader = csv.reader(f)
reader = list(reader)[1:]
print(list(reader))

print('-----processing-------')

for name,x1,y1,x2,y2,x3,y3,rec in reader:

    if rec == "1":
        label = "havestar"
    else:
        label = "nostar"
    print("input :",new+label+"/"+name+".jpg")
    img = cv2.imread(new+label+"/"+name+".jpg")
    if img is None:
        print("shape:")
        continue
    x1,x2,x3 = int(float(x1)),int(float(x2)),int(float(x3))
    y1,y2,y3 = int(float(y1)),int(float(y2)),int(float(y3))
    a = [x1-10,y1-10,x1+10,y1+10]
    b = [x2-10,y2-10,x2+10,y2+10]
    c = [x3-10,y3-10,x3+10,y3+10]
    print(a,b,c)
    plot_one_box(a,img,color = (250,0,0),label=label,rank=1)
    plot_one_box(b,img,color = (255,0,0),label=label,rank=2)
    plot_one_box(c,img,color = (255,0,0),label=label,rank=3)
    print("output:",cate+label+"1/"+name+".jpg")
    print(cv2.imwrite(cate+label+"1/"+name+".jpg",img))

