import matplotlib.pyplot as plt
import time
from glob import glob as gf
import os


def help():
   print('from imansarraf import Audio:\n1-Read, Resample and Write PCM and Alaw Files \n2-frame and split (VAD)\n3-ReadMp3 (with miniaudio)\n\n\nimport imansarraf:\n1-plt\n2-now (get time)\n3-F (format floating point)\n4-D (format int number)\n5-Write_List\n6-Write_Dic\n7-Read (read txt file)\n8-Read_Lines (read txt file line by line and return list)\n9-Write (write string to file)\n10-gf (Get files in a directory)\n11-gfa (Get Files in a Directory and SubDirectories)\n12-ReadE (Read Excel files)\n\nfrom imansarraf import info:\n1-Get info about cpu and gpu (need torch)\n\n\nfrom imansarraf import metrics:\n1-EER(lab,score)\n2-cosine_distance\n3-roc(lab,score)\n\nfrom imansarraf import tsne\n1-tsne.plot(fea , label)\n\n')


def now():
   return time.time()
     
def F(float_number , float_number_count = 2):
   _str=("{:." + str(float_number_count) +"f}").format(float_number)
   return(_str) 

def D(int_number , int_number_count = 3):
   _str=("{:0>" + str(int_number_count) +"d}").format(int(int_number))
   return(_str) 
   
def Write(_str,Filename):
   with open(Filename , 'w' , encoding='utf-8') as fid:
              fid.write(_str)    

def Write_List(MyList,Filename):
   with open(Filename , 'w' , encoding='utf-8') as fid:
        for x in MyList:
              fid.write(str(x) + '\n')    

def Write_Dic(MyDic,Filename):
   with open(Filename , 'w' , encoding='utf-8') as fid:
        for x,y in MyDic.items():
              fid.write(str(x) + '\t' + str(y) + '\n')                 
              
def Read(Filename):
    with open(Filename , 'r' , encoding='utf-8') as fid:
         return(fid.read())

def Read_Lines(Filename):
    with open(Filename , 'r' , encoding='utf-8') as fid:
         return([x.strip() for x in fid if (x.strip()!="")])    

def gfa(directory , ext="*.*"):
   a=[]
   for root, dirs, files in os.walk(directory):
      for dirname in dirs:
         _dir =os.path.join(root, dirname)  
         [a.append(x) for x in gf(os.path.join(_dir , ext))]   
   return a         

def ReadE(Filename):
    import pandas as pd
    pp = pd.read_excel(Filename , engine='openpyxl')
    return pp
    