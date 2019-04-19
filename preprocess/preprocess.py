# -*- coding: utf-8 -*-
"""
@author: frothmoon
"""

import os,xml,codecs
from xml.dom.minidom import Document
import glob
import cv2
import time
import csv
import shutil
from PIL import Image

VOC_root = "./data/VOCdevkit2007/VOC2007"


training_path="./3channels"

def genetate_org_xml(img,im,training_path,row,xml_path,img_path):
    adSize = 24
    height, width = im.shape[:2]
    if row[0] == str(img):
        if row[3] == "newtarget" or row[3] == "isstar" or row[3] == "asteroid" or row[3] == "isnova" or row[
            3] == "known":
            fName = "havestar"
        else:
            fName = "nostar"

        if fName == "havestar":
            x = int(row[1])
            y = int(row[2])
            tmp_path=os.path.join(training_path,img+'.jpg')
            tmp2_path=os.path.join(img_path,img+'.jpg')
            shutil.copy(tmp_path, tmp2_path)
            #cv2.imwrite(img_path, im)
            cdoc = Document()
            ann = cdoc.createElement("annotation")
            cdoc.appendChild(ann)
            folder = cdoc.createElement("folder")
            ann.appendChild(folder)
            cf = cdoc.createTextNode("VOC2007")
            folder.appendChild(cf)
            filename = cdoc.createElement("filename")
            cn = cdoc.createTextNode(img + ".jpg")
            filename.appendChild(cn)
            ann.appendChild(filename)
            size = cdoc.createElement("size")
            w = cdoc.createElement("width")
            cw = cdoc.createTextNode(str(x))
            w.appendChild(cw)
            h = cdoc.createElement("height")
            ch = cdoc.createTextNode(str(y))
            h.appendChild(ch)
            d = cdoc.createElement("depth")
            cd = cdoc.createTextNode(str(3))
            d.appendChild(cd)
            size.appendChild(w)
            size.appendChild(h)
            size.appendChild(d)
            ann.appendChild(size)
            obj = cdoc.createElement("object")
            ann.appendChild(obj)
            name = cdoc.createElement("name")
            obj.appendChild(name)
            cname = cdoc.createTextNode("havestar")
            name.appendChild(cname)
            pose = cdoc.createElement("pose")
            obj.appendChild(pose)
            cuns = cdoc.createTextNode("Unspecified")
            pose.appendChild(cuns)
            truncated = cdoc.createElement("truncated")
            obj.appendChild(truncated)
            ctru = cdoc.createTextNode(str(0))
            truncated.appendChild(ctru)
            difficult = cdoc.createElement("difficult")
            obj.appendChild(difficult)
            cdif = cdoc.createTextNode(str(0))
            difficult.appendChild(cdif)
            bndbox = cdoc.createElement("bndbox")
            xmin = cdoc.createElement("xmin")
            rescxmin = x - adSize
            if (rescxmin) < 1:
                rescxmin = 1
            cxmin = cdoc.createTextNode(str(rescxmin))
            xmin.appendChild(cxmin)
            ymin = cdoc.createElement("ymin")
            rescymin = y - adSize
            if (rescymin) < 1:
                rescymin = 1
            cymin = cdoc.createTextNode(str(rescymin))
            ymin.appendChild(cymin)
            xmax = cdoc.createElement("xmax")
            rescxmax = x  + adSize
            if (rescxmax) > width - 1:
                rescxmax = x - 1
            cxmax = cdoc.createTextNode(str(rescxmax))
            xmax.appendChild(cxmax)
            ymax = cdoc.createElement("ymax")
            rescymax = y  + adSize
            if (rescymax) > height - 1:
                rescymax = y - 1
            cymax = cdoc.createTextNode(str(rescymax))
            ymax.appendChild(cymax)
            bndbox.appendChild(xmin)
            bndbox.appendChild(ymin)
            bndbox.appendChild(xmax)
            bndbox.appendChild(ymax)
            obj.appendChild(bndbox)
            f = codecs.open(xml_path + '/' + img +  '.xml', 'w', 'utf-8')
            cdoc.writexml(f, addindent=' ', newl='\n', encoding='utf-8')
            f.close()
def generate_xml(img,row,im,xml_path,img_path):
    adSize = 24
    cutsize = 50
    cut_flag = True
    height, width = im.shape[:2]
    if row[0] == str(img):
        if row[3] == "newtarget" or row[3] == "isstar" or row[3] == "asteroid" or row[3] == "isnova" or row[
            3] == "known":
            fName = "havestar"
        else:
            fName = "nostar"

        if fName == "havestar":
            x = int(row[1])
            y = int(row[2])
            if (x > width or x < 0 or y > height or y < 0):
                print("error " + str(row[0]))
                return
            ltx = x - cutsize
            lty = y - cutsize
            rdx = x + cutsize
            rdy = y + cutsize
            if ltx <= 1:
                ltx = 1
            if lty <= 1:
                lty = 1
            if rdx >= width - 1:
                rdx = width - 1
            if rdy >= height - 1:
                rdy = height - 1
            # print(str(rdx-ltx)+" "+str(rdy-lty))
            image_cut = im[lty:rdy, ltx:rdx]
            imgcc = str(row[0]) + "#%"
            if cut_flag:
                fx = 2
                fy = 2
                rescc = cv2.resize(image_cut, (0, 0), fx=fx, fy=fy, interpolation=cv2.INTER_CUBIC)

            else:
                rescc = image_cut
            outpath = os.path.join(img_path, imgcc + "_" + str(cutsize) + ".jpg")
            cv2.imwrite(outpath, rescc)
            resizeh, resizew = rescc.shape[:2]
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
            f = codecs.open(xml_path + '/' + imgcc +"_"+str(cutsize)+ '.xml','w','utf-8')
            cdoc.writexml(f,addindent = ' ',newl='\n',encoding = 'utf-8')
            f.close()
def make_voc(training_path,img_path,xml_path,txt_path):

    img_Lists = glob.glob(training_path + '/*.jpg')

    img_basenames = []
    for item in img_Lists:
        img_basenames.append(os.path.basename(item))

    img_names = []
    for item in img_basenames:
        temp1, temp2 = os.path.splitext(item)
        img_names.append(temp1)

    org_csv=glob.glob(training_path+'/*.csv')

    for img in img_names:
        imgpath = training_path + '/' + img + '.jpg'
        im = cv2.imread(imgpath, 1)

        height, width = im.shape[:2]

        gt = csv.reader(open(org_csv[0]))
        for row in gt:
            if row[3] == "newtarget" or row[3] == "isstar" or row[3] == "asteroid" or row[3] == "isnova" or row[
                3] == "known":
                genetate_org_xml(img,im,training_path,row,xml_path,img_path)
                generate_xml(img,row,im,xml_path,img_path)



if __name__ == '__main__':
    if not VOC_root:
        os.makedirs(VOC_root)

    image_path=VOC_root+"/JPEGImages"
    isExists = os.path.exists(image_path)
    if not isExists:
        os.makedirs(image_path)

    xml_path=VOC_root+"/Annotations"
    isExists = os.path.exists(xml_path)
    if not isExists:
        os.makedirs(xml_path)

    txt_path=VOC_root+"/Imagesets"+"/Main"
    isExists = os.path.exists(txt_path)
    if not isExists:
        os.makedirs(txt_path)

    make_voc(training_path,image_path,xml_path,txt_path)

    print("successful")



