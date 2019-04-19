import os
import shutil
import argparse

parser = argparse.ArgumentParser(description="rename a pair of xml and jpg")
parser.add_argument('--append',type=str,default="rename")
parser.add_argument('--jpg_path',type=str,default="./JPGEImages")
parser.add_argument('--xml_path',type=str,default="./Annotations")
parser.add_argument('--out',action='store_false')
parser.add_argument('--delete',type=str,default="rename")
args = parser.parse_args()

path_jpg = args.jpg_path
path_xml = args.xml_path


if args.append == "rename" and args.delete != "rename":
    lth = len(args.delete)
    print("start to delete rename string")
    for f in os.listdir(path_jpg):
        name,ext = f.split('.')
        newName = name[:-lth]
        os.rename(os.path.join(path_jpg,f),os.path.join(path_jpg,newName+"."+ext))
        os.rename(os.path.join(path_xml,name+".xml"),os.path.join(path_xml,newName+".xml"))
    print("delete rename completed")

else:
    print("start to append rename string")
    for f in os.listdir(path_jpg):
        name,ext = f.split('.')
        os.rename(os.path.join(path_jpg,f),os.path.join(path_jpg,name+args.append+"."+ext))
        os.rename(os.path.join(path_xml,name+".xml"),os.path.join(path_xml,name+args.append+".xml"))
    print("append rename completed")
