import os

filename = "./comp4_det_test_havestar.txt"
outfile = "./submit.csv"

f = open(filename,'r')
rl = f.readlines()
fout = open(outfile,'w')

def str2float(s):
    def fn(x,y):
        return x*10+y
    n=s.index('.')
    s1 = list(map(str2float,[x for x in s[:n]]))
    s2 = list(map(str2float,[x for x in s[n+1:]]))
    return reduce(fn,s1)+reduce(fn,s2)/(10**len(s2))

nameset = set()

cnt = 0
outext=""
tag = True

for line in rl:
    line = line[:-1]
    name,conf,xmin,ymin,xmax,ymax = line.split(' ')
    xcenter,ycenter = (float(xmin)+float(xmax))//2 ,(float(ymin)+float(ymax))//2
    print(xcenter,ycenter)
    print("cnt:",cnt)
    if name not in nameset:
        outext=""
        nameset.add(name)
        outext = outext + name + ","+str(xcenter)+","+str(ycenter)
        cnt = 1 
        tag = True
    elif name in nameset:
        if cnt < 3 and tag:
            cnt = cnt + 1
            outext = outext+","+str(xcenter)+","+str(ycenter)
        elif cnt == 3: 
            cnt = 0
            tag = False
            print(outext)
            fout.write(outext+",1\n")
        elif cnt > 3:
            continue


f.close()
fout.close()
