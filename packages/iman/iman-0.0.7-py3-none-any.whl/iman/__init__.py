import matplotlib.pyplot as plt
import time
from glob import glob as gf
import os
import numpy as np

def help():
   print('from iman import Audio:\n1-Read(filename,sr)\n2-Resample(data , fs, sr)\n3-Read_Alaw(filename)\n4-ReadMp3(filename,sr,mono=True)\n5-Write(filename, data ,fs)\n6-frame(y)\n7-split(y)\n\nfrom iman import *:\n1-plt\n2-now() (get time)\n3-F (format floating point)\n4-D (format int number)\n5-Write_List(MyList,Filename)\n6-Write_Dic(MyDic,Filename)\n7-Read(Filename) (read txt file)\n8-Read_Lines(Filename) (read txt file line by line and return list)\n9-Write(_str,Filename)\n10-gf(pattern) (Get files in a directory)\n11-gfa(directory , ext="*.*") (Get Files in a Directory and SubDirectories)\n12-ReadE(Filename) (Read Excel files)\n13-PM(dir)(creat directory)\n14-PB(fname)(get basename)\n15-PN(fname) (get file name)\n16-PE(fname)(get ext)\n17-PD(fname)(get directory)\n18-PS(fname)(get size)\n19-PJ(segments) (Join Path)\n20-clear() (clear cmd)\n21-os\n22-np\n23-RI(start_int , end_int , count=1) (random int)\n24-RF(start_float , end_float , count=1) (random float)\n25-RS(Arr) (shuffle)\n\nfrom iman import info:\n1-get() info about cpu and gpu (need torch)\n\n\nfrom iman import metrics:\n1-EER(lab,score)\n2-cosine_distance(v1,v2)\n3-roc(lab,score)\n\nfrom iman import tsne:\n1-plot(fea , label)\n\nfrom iman import xvector:\n1-xvec,lda_xvec,gender = get(filename , model_path , model_name , model_speaker_num)\n\n')

   
def clear():
    if os.name == 'nt':
        _ = os.system('cls')  
    else:
        _ = os.system('clear')
        
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
    
def PB(filename):
   return os.path.basename(filename)    
         
def PD(filename):
   return os.path.dirname(filename)  
   
def PM(folname):
   return os.makedirs(folname , exist_ok=True)
       
def PN(filename):
   return os.path.basename(os.path.splitext(filename)[0])  

def PE(filename):
   return os.path.splitext(filename)[1]    
   
def PJ(*_segments):
   x=""
   for p in _segments:
      x = os.path.join(x,p)
   return x   
   
def PS(filename):
   return os.path.getsize(filename)  
   
def RI(start_int , end_int , count=1):
   return np.random.randint(low=int(start_int), high=int(end_int), size=(count,))
   
def RF(start_float , end_float , count=1):
  return np.random.uniform(start_float, end_float , count)
  
def RS(Arr):
  np.random.shuffle(Arr)
  return Arr