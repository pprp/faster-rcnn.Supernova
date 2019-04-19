# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 13:26:20 2018

@author: Administrator
"""

import os,xml,codecs
from xml.dom.minidom import Document
import glob
import cv2
import time
import csv
from PIL import Image

image_dir="./3channels"
csv_dir="./list.csv"
image_outdir="./resizeimg"
xml_outdir="./resizexml"

gt= csv.reader(open(csv_dir))
for row in gt:
	if (str(row[3])=="newtarget")or(str(row[3])=="isstar")or(str(row[3])=="asteroid")or(str(row[3])=="isnova")or(str(row[3])=="known"):
		imgpath=image_dir+"/"+str(row[0])+".jpg"
		image=cv2.imread(imgpath,1)
		# sp = image.shape
		# win_h=sp[0]
		# win_w=sp[1]
		#win_h, win_w=image.shape[:2]
		#print(win_h, win_w)
		x=int(row[1])
		y=int(row[2])
		
		fx = 2
		fy = 2
		enlarge = cv2.resize(image, (0, 0), fx = fx, fy = fy, interpolation = cv2.INTER_CUBIC)
		win_h,win_w= enlarge.shape[:2]
		print(win_h, win_w)
		img=str(row[0]) + "%"
		outpath = os.path.join(image_outdir, img+".jpg")	
		cv2.imwrite(outpath, enlarge)  
		if(x>win_w or x<0 or y>win_h or y<0):
			print("error "+str(row[0]))
		# ltx=x-50
		# lty=y-50
		# rdx=x+50
		# rdy=y+50
		# if ltx<=1:
		# 	ltx=1
		# if lty<=1:
		# 	lty=1
		# if rdx>=win_w-1:
		# 	rdx=win_w-1
		# if rdy>=win_h-1:
		# 	rdy=win_h-1
		# if(rdy-lty!=100 and rdx-ltx!=100):
		# 	print(str(row[0]))
		# print(str(rdx-ltx)+" "+str(rdy-lty))
		# image_cut = image[lty:rdy,ltx:rdx]
		
		doc = Document()
		ann = doc.createElement("annotation")
		doc.appendChild(ann)
		folder = doc.createElement("folder")
		ann.appendChild(folder)
		cf = doc.createTextNode("VOC2007")
		folder.appendChild(cf)
		filename = doc.createElement("filename")
		cn = doc.createTextNode(img+".jpg")
		filename.appendChild(cn)
		ann.appendChild(filename)
		size = doc.createElement("size")
		w= doc.createElement("width")
		cw = doc.createTextNode(str(win_w))
		w.appendChild(cw)
		h= doc.createElement("height")
		ch = doc.createTextNode(str(win_h))
		h.appendChild(ch)
		d= doc.createElement("depth")
		cd = doc.createTextNode(str(3))
		d.appendChild(cd)
		size.appendChild(w)
		size.appendChild(h)
		size.appendChild(d)
		ann.appendChild(size)
		obj= doc.createElement("object")
		ann.appendChild(obj)
		name= doc.createElement("name")
		obj.appendChild(name)
		cname = doc.createTextNode("havestar")
		name.appendChild(cname)
		pose= doc.createElement("pose")
		obj.appendChild(pose)
		cuns = doc.createTextNode("Unspecified")
		pose.appendChild(cuns)
		truncated= doc.createElement("truncated")
		obj.appendChild(truncated)
		ctru = doc.createTextNode(str(0))
		truncated.appendChild(ctru)
		difficult= doc.createElement("difficult")
		obj.appendChild(difficult)
		cdif = doc.createTextNode(str(0))
		difficult.appendChild(cdif)
		bndbox = doc.createElement("bndbox")
		xmin= doc.createElement("xmin")
		rescxmin=x*2-5
		if (rescxmin)<1:
			rescxmin=1
		cxmin = doc.createTextNode(str(rescxmin))
		xmin.appendChild(cxmin)
		ymin= doc.createElement("ymin")
		rescymin=y*2-5
		if (rescymin)<1:
			rescymin=1
		cymin = doc.createTextNode(str(rescymin))
		ymin.appendChild(cymin)
		xmax= doc.createElement("xmax")
		rescxmax=x*2+5
		if (rescxmax)>win_w-1:
			rescxmax=win_w-1
		cxmax = doc.createTextNode(str(rescxmax))
		xmax.appendChild(cxmax)
		ymax= doc.createElement("ymax")
		rescymax=y*2+5
		if (rescymax)>win_h-1:
			rescymax=win_h-1
		cymax = doc.createTextNode(str(rescymax))
		ymax.appendChild(cymax)
		bndbox.appendChild(xmin)
		bndbox.appendChild(ymin)
		bndbox.appendChild(xmax)
		bndbox.appendChild(ymax)
		obj.appendChild(bndbox)
		f = codecs.open(xml_outdir + '/' + img + '.xml','w','utf-8')
		doc.writexml(f,addindent = ' ',newl='\n',encoding = 'utf-8')
		f.close()
		csvFile2 = open('./resize.csv','a')#,newline=''
		writer = csv.writer(csvFile2,dialect='excel')
		msg=[img,rescxmin+5,rescymin+5]
		#msg=[img,rescxmax-5,rescymax-5]
		writer.writerow(msg)
		csvFile2.close()
		print(img+"finish!")
#07180ca5d826bbd37517ceb5515fc83b#
