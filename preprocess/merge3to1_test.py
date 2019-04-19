import shutil
import os
import cv2
import matplotlib.pyplot as plt
import errno
import pathlib

rootdir = "./af2019-cv-testA-20190318/"
patha = "./a/"
pathb = "./b/"
pathc = "./c/"
pathout = "./merged_test/"

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exec:
        if exec.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def move(path):
    """root dir"""
    print("Start to move images")
    for f in os.listdir(path):
        if os.path.isdir(path+f):
            for file in os.listdir(path+f):
                name, ext = os.path.splitext(file)
                if name.endswith("_a"):
                    #print(path+f+"/"+file)
                    shutil.copy(path+f+"/"+file, patha+file)
                elif name.endswith("_b"):
                    #print(path+f+"/"+file)
                    shutil.copy(path+f+"/"+file, pathb+file)
                elif name.endswith("_c"):
                    #print(path+f+"/"+file)
                    shutil.copy(path+f+"/"+file, pathc+file)
    print("Move completed!!!")

def mergeImg(patha):
    print("Start to merge three images into one image")
    for f in os.listdir(patha):
        #print(f)
        name,ext = f.split('_')
        #print(patha+name+"_a.jpg")
        imga = cv2.imread(patha+name+"_a.jpg", -1)
        imgb = cv2.imread(pathb+name+"_b.jpg", -1)
        imgc = cv2.imread(pathc+name+"_c.jpg", -1)
        img = cv2.merge([imgc,imgb,imga])
        outname = name+".jpg"
        cv2.imwrite(pathout+outname, img)
        del imga,imgb,imgc,img
    print("Merge completed!!")


def delete_folder(dest):

    shutil.rmtree(dest, ignore_errors=True)

if __name__ == "__main__":
    mkdir_p(patha)
    mkdir_p(pathb)
    mkdir_p(pathc)
    mkdir_p(pathout)
    move(rootdir)
    mergeImg(patha)
    print("Deleting a,b,c")
    delete_folder(patha)
    delete_folder(pathb)
    delete_folder(pathc)
    print("Delete completed!!!")

