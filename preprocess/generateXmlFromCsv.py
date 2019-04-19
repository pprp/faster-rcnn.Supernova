
import os,xml,codecs
from xml.dom.minidom import Document
import csv
import glob
from PIL import Image

src_img_dir = "/media/learner/Passport/COPY/VOCdevkit2007/VOC2007/JPEGImages"
src_csv_dir = "/media/learner/Passport/COPY"
src_xml_dir = "/media/learner/Passport/COPY/VOCdevkit2007/VOC2007/Annotations"
error_file = "/media/learner/Passport/COPY/error.txt"

img_Lists = glob.glob(src_img_dir + '/*.jpg')

#print(img_Lists)

img_basenames = [] # e.g. 100.jpg
for item in img_Lists:
    img_basenames.append(os.path.basename(item))

img_names = [] # e.g. 100
for item in img_basenames:
    temp1, temp2 = os.path.splitext(item)
    img_names.append(temp1)

for img in img_names:
    im = Image.open((src_img_dir + '/' + img+ '.jpg'))
    width, height = im.size

    gt= csv.reader(open(src_csv_dir + '/' +'list.csv'))
    for row in gt:
        if row[0]==str(img):
            if not os.path.exists(src_xml_dir+ '/' + img +'.xml'):
#                xml_file =
                doc = Document()
                ann = doc.createElement("annotation")
                doc.appendChild(ann)
                folder = doc.createElement("folder")
                ann.appendChild(folder)
                cf = doc.createTextNode("VOC2007")
                folder.appendChild(cf)
                filename = doc.createElement("filename")
                cn = doc.createTextNode(str(img+'.JPG'))
                filename.appendChild(cn)
                ann.appendChild(filename)
                size = doc.createElement("size")
                w= doc.createElement("width")
                cw = doc.createTextNode(str(width))
                w.appendChild(cw)
                h= doc.createElement("height")
                ch = doc.createTextNode(str(height))
                h.appendChild(ch)
                d= doc.createElement("depth")
                cd = doc.createTextNode(str(3))
                d.appendChild(cd)
                size.appendChild(w)
                size.appendChild(h)
                size.appendChild(d)
                ann.appendChild(size)

                f = codecs.open(src_xml_dir + '/' + img + '.xml','w','utf-8')
                doc.writexml(f,addindent = ' ',newl='\n',encoding = 'utf-8')
                f.close()


            dom = xml.dom.minidom.parse(src_xml_dir + '/' + img + '.xml')
            fd = dom.getElementsByTagName("annotation")
            obj= dom.createElement("object")
            fd[0].appendChild(obj)
            name= dom.createElement("name")
            obj.appendChild(name)
            print(row[3])
            fName = ""
            if row[3] == "newtarget" or row[3] == "isstar" or row[3] =="asteroid" or row[3] == "isnova" or row[3] == "known":
                fName = "havestar"
            else:
                fName = "nostar"
            fName = "havestar"
            if int(row[1]) > width or int(row[2]) > height:
                print("ERROR!!!!",img)
                continue

            cname = dom.createTextNode(str(fName))
            name.appendChild(cname)
            pose= dom.createElement("pose")
            obj.appendChild(pose)
            cuns = dom.createTextNode("Unspecified")
            pose.appendChild(cuns)
            truncated= dom.createElement("truncated")
            obj.appendChild(truncated)
            ctru = dom.createTextNode(str(0))
            truncated.appendChild(ctru)
            difficult= dom.createElement("difficult")
            obj.appendChild(difficult)
            cdif = dom.createTextNode(str(0))
            difficult.appendChild(cdif)
            bndbox = dom.createElement("bndbox")
            xmin= dom.createElement("xmin")
            cxmin = dom.createTextNode(str(max(1,int(row[1])-24)))
            xmin.appendChild(cxmin)
            ymin= dom.createElement("ymin")
            cymin = dom.createTextNode(str(max(1,int(row[2])-24)))
            ymin.appendChild(cymin)
            xmax= dom.createElement("xmax")
            cxmax = dom.createTextNode(str(min(int(row[1])+24,width-1)))
            xmax.appendChild(cxmax)
            ymax= dom.createElement("ymax")
            cymax = dom.createTextNode(str(min(int(row[2])+24,height-1)))
            ymax.appendChild(cymax)
            print(img,":",width,height,":",int(row[1]),int(row[2]),":",str(max(1,int(row[1])-24)),str(max(1,int(row[2])-24)),str(min(int(row[1])+24,width)),str(min(int(row[2])+24,height)))
            bndbox.appendChild(xmin)
            bndbox.appendChild(ymin)
            bndbox.appendChild(xmax)
            bndbox.appendChild(ymax)
            obj.appendChild(bndbox)
            f = codecs.open(src_xml_dir + '/' + img + '.xml','w','utf-8')
            dom.writexml(f,addindent = ' ',newl='\n',encoding = 'utf-8')
#            dom.writexml(f,newl='\n',encoding = 'utf-8')
            f.close()
