import cv2
import random
import numpy as np
import os
import shutil
from scipy import signal
import matplotlib.pyplot as plt


file1 = "/media/learner/Passport/tttt/5c.jpg"
file2 = "/media/learner/Passport/tttt/5b.jpg"

def process2Image(file1,file2,savePath,saveName):
    """file1 --- c file2 --- b"""
    img1 = cv2.imread(file1,0)
    img2 = cv2.imread(file2,0)
    
    img1 = cv2.blur(img1,(3,3))
    img2 = cv2.blur(img2,(3,3))
    
    size = 2
    kernel = np.ones((size, size), dtype=np.uint8)
    ret,th = cv2.threshold(img1,0,255,cv2.THRESH_TOZERO+cv2.THRESH_OTSU)    
    ret2,th2 = cv2.threshold(img2,0,255,cv2.THRESH_TOZERO+cv2.THRESH_OTSU)
   
    img_and = cv2.bitwise_and(th2,th)
    sub1 = cv2.subtract(th2,img_and)
    #sub2 = cv2.subtract(th,img_and)
    more_thresh = cv2.erode(cv2.erode(sub1,kernel),kernel)#cv2.threshold(sub1,0,255,cv2.THRESH_TOZERO+cv2.THRESH_OTSU)
    cv2.imwrite(savePath+saveName,more_thresh)
    
    
    
if __name__ == "__main__":
    pathb = "./b/"
    pathc = "./c/"
    savePath = "./save/"
    for f in os.listdir(pathb):
        print(f)
        a,b =os.path.splitext(f)
        name,ext = a.split('_')
        print(name)
        process2Image(pathc+name+"_c.jpg",pathb+name+"_b.jpg",savePath,name+".jpg")
        
        
    
    
'''
plt.figure(figsize=(28,28))
plt.rcParams['figure.dpi'] = 400
plt.subplots_adjust(left=0.125,bottom=None,right=0.4,top=None)
plt.subplot(421),plt.imshow(img1,'gray'),plt.title('origin1')
plt.subplot(423),plt.imshow(img_close,'gray'),plt.title('sub')
plt.subplot(425),plt.imshow(th,'gray'),plt.title('th1')
plt.subplot(422),plt.imshow(img2,'gray'),plt.title('origin2')
plt.subplot(424),plt.imshow(img_and,'gray'),plt.title('and')
plt.subplot(426),plt.imshow(th2,'gray'),plt.title('th2')
plt.subplot(427),plt.imshow(sub1,'gray'),plt.title('sub1-2')
plt.subplot(428),plt.imshow(more_thresh,'gray'),plt.title('sub2-1')
plt.show()

centercut_img=img_outdir+"/centercut_img"


isExists=os.path.exists(centercut_img)
if not isExists:
    os.makedirs(centercut_img)

cc_have_img=centercut_img+"/havestar"

isExists=os.path.exists(cc_have_img)
if not isExists:
    os.makedirs(cc_have_img)

centercut_xml=xml_outdir+"/centercut_xml"

isExists=os.path.exists(centercut_xml)
if not isExists:
    os.makedirs(centercut_xml)

cc_have_xml=centercut_xml+"/havestar"

isExists=os.path.exists(cc_have_xml)
if not isExists:
    os.makedirs(cc_have_xml)


img_Lists = glob.glob(img_dir + '/*.jpg')

img_basenames = []
for item in img_Lists:
    img_basenames.append(os.path.basename(item))

img_names = []
for item in img_basenames:
    temp1, temp2 = os.path.splitext(item)
    img_names.append(temp1)

for img in img_names:
    imgpath=img_dir + '/' + img+ '.jpg'
    im=cv2.imread(imgpath,1)

    height, width = im.shape[:2]

    gt= csv.reader(open(csv_dir))
    for row in gt:
        if row[0]==str(img):
            if row[3] == "newtarget" or row[3] == "isstar" or row[3] =="asteroid" or row[3] == "isnova" or row[3] == "known" or row[3] == "noise" or row[3] == "ghost" or row[3] == "pity":
                fName = "havestar"
            else:
                fName = "nostar"

            if fName=="havestar":
                x=int(row[1])
                y=int(row[2])
                if(x>width or x<0 or y>height or y<0):
                    print("error "+str(row[0]))
                    continue
                ltx=x-cutsize
                lty=y-cutsize
                rdx=x+cutsize
                rdy=y+cutsize
                if ltx<=1:
                    ltx=1
                if lty<=1:
                    lty=1
                if rdx>=width-1:
                    rdx=width-1
                if rdy>=height-1:
                    rdy=height-1
                #print(str(rdx-ltx)+" "+str(rdy-lty))
                image_cut = im[lty:rdy,ltx:rdx]
                imgcc=str(row[0]) + "#%"
                if cut_flag:
                    fx = 2
                    fy = 2
                    rescc = cv2.resize(image_cut, (0, 0), fx = fx, fy = fy, interpolation = cv2.INTER_CUBIC)
                else:
                    rescc=image_cut
                outpath = os.path.join(cc_have_img, imgcc+"_"+str(cutsize)+".jpg")
                cv2.imwrite(outpath, rescc)
                resizeh,resizew=rescc.shape[:2]
                cdoc = Document()
                ann = cdoc.createElement("annotation")
                cdoc.appendChild(ann)
                folder = cdoc.createElement("folder")
                ann.appendChild(folder)
                cf = cdoc.createTextNode("VOC2007")
                folder.appendChild(cf)
                filename = cdoc.createElement("filename")
                cn = cdoc.createTextNode(imgcc+".jpg")
                filename.appendChild(cn)
                ann.appendChild(filename)
                size = cdoc.createElement("size")
                w= cdoc.createElement("width")
                if cut_flag:
                    multag=2
                else:
                    multag=1
                cw = cdoc.createTextNode(str((rdx-ltx)*multag))
                w.appendChild(cw)
                h= cdoc.createElement("height")
                ch = cdoc.createTextNode(str((rdy-lty)*multag))
                h.appendChild(ch)
                d= cdoc.createElement("depth")
                cd = cdoc.createTextNode(str(3))
                d.appendChild(cd)
                size.appendChild(w)
                size.appendChild(h)
                size.appendChild(d)
                ann.appendChild(size)
                obj= cdoc.createElement("object")
                ann.appendChild(obj)
                name= cdoc.createElement("name")
                obj.appendChild(name)
                cname = cdoc.createTextNode("havestar")
                name.appendChild(cname)
                pose= cdoc.createElement("pose")
                obj.appendChild(pose)
                cuns = cdoc.createTextNode("Unspecified")
                pose.appendChild(cuns)
                truncated= cdoc.createElement("truncated")
                obj.appendChild(truncated)
                ctru = cdoc.createTextNode(str(0))
                truncated.appendChild(ctru)
                difficult= cdoc.createElement("difficult")
                obj.appendChild(difficult)
                cdif = cdoc.createTextNode(str(0))
                difficult.appendChild(cdif)
                bndbox = cdoc.createElement("bndbox")
                xmin= cdoc.createElement("xmin")
                rescxmin=(x-ltx)*multag-adSize
                if (rescxmin)<1:
                    rescxmin=1
                cxmin = cdoc.createTextNode(str(rescxmin))
                xmin.appendChild(cxmin)
                ymin= cdoc.createElement("ymin")
                rescymin=(y-lty)*multag-adSize
                if (rescymin)<1:
                    rescymin=1
                cymin = cdoc.createTextNode(str(rescymin))
                ymin.appendChild(cymin)
                xmax= cdoc.createElement("xmax")
                rescxmax=(x-ltx)*multag+adSize
                if (rescxmax)>resizew-1:
                    rescxmax=resizew-1
                cxmax = cdoc.createTextNode(str(rescxmax))
                xmax.appendChild(cxmax)
                ymax= cdoc.createElement("ymax")
                rescymax=(y-lty)*multag+adSize
                if (rescymax)>resizeh-1:
                    rescymax=resizeh-1
                cymax = cdoc.createTextNode(str(rescymax))
                ymax.appendChild(cymax)
                bndbox.appendChild(xmin)
                bndbox.appendChild(ymin)
                bndbox.appendChild(xmax)
                bndbox.appendChild(ymax)
                obj.appendChild(bndbox)
                f = codecs.open(cc_have_xml + '/' + imgcc +"_"+str(cutsize)+ '.xml','w','utf-8')
                cdoc.writexml(f,addindent = ' ',newl='\n',encoding = 'utf-8')
                f.close()
                csvFile = open(csv_outdir+'/centercut.csv','a')#,newline=''
                writer = csv.writer(csvFile,dialect='excel')
                msg=[imgcc,rescxmin+adSize,rescymin+adSize]
                #msg=[img,rescxmax-5,rescymax-5]
                writer.writerow(msg)
                csvFile.close()
                print(imgcc+" finish!")

'''