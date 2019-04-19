import cv2
import csv
import random
import os

new = "./3channels/"
cate = "./kind/"

def plot_one_box(x, img, color=None, label=None, line_thickness=None):  # Plots one bounding box on image img
    tl = 2#line_thickness or round(0.002 * max(img.shape[0:2])) + 1  # line thickness
    color = color #or [random.randint(0, 255) for _ in range(3)]
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
    cv2.rectangle(img, c1, c2, color, tl)
    if label:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(img, c1, c2, color, -1)  # filled
        cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 4, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)

filename = "./list.csv"
f = open(filename)
reader = csv.reader(f)
reader = list(reader)[1:]
print(list(reader))

print('-----processing-------')

for name,x,y,label in reader:
    img = cv2.imread(new+name+".jpg")

    x = int(x)
    y = int(y)
    a = [x-10,y-10,x+10,y+10]
    print(label)
    #if label == "newtarget" or label == "isstar" or label == "asteroid" or label == "isnova" or label == "known":
    #    print("havestar")
    #    label = "havestar"
    #else:
    #    print("nostar")
    #    label = "nostar"
    plot_one_box(a,img,color = (34,139,34),label=label)
    print(cate+label+"/"+name+".jpg")
    print(os.path.isdir(cate+label))
    print(cv2.imwrite(cate+label+"/"+name+".jpg",img))

