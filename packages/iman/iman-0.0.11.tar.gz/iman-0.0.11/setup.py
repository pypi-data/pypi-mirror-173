from setuptools import setup, find_packages

setup(
        # the name must match the folder name 'verysimplemodule'
        name="iman", 
        version='0.0.11',
        author="Iman Sarraf",
        author_email="imansarraf@gmail.com",
        description='Python package for daily Tasks',
        long_description='from iman import Audio:\n1-Read(filename,sr)\n2-Resample(data , fs, sr)\n3-Read_Alaw(filename)\n4-ReadMp3(filename,sr,mono=True)\n5-Write(filename, data ,fs)\n6-frame(y)\n7-split(y)\n\nfrom iman import *:\n1-plt\n2-now() (get time)\n3-F (format floating point)\n4-D (format int number)\n5-Write_List(MyList,Filename)\n6-Write_Dic(MyDic,Filename)\n7-Read(Filename) (read txt file)\n8-Read_Lines(Filename) (read txt file line by line and return list)\n9-Write(_str,Filename)\n10-gf(pattern) (Get files in a directory)\n11-gfa(directory , ext="*.*") (Get Files in a Directory and SubDirectories)\n12-ReadE(Filename) (Read Excel files)\n13-PM(dir)(creat directory)\n14-PB(fname)(get basename)\n15-PN(fname) (get file name)\n16-PE(fname)(get ext)\n17-PD(fname)(get directory)\n18-PS(fname)(get size)\n19-PJ(segments) (Join Path)\n20-clear() (clear cmd)\n21-os\n22-np\n23-RI(start_int , end_int , count=1) (random int)\n24-RF(start_float , end_float , count=1) (random float)\n25-RS(Arr) (shuffle)\n\nfrom iman import info:\n1-get() info about cpu and gpu (need torch)\n\n\nfrom iman import metrics:\n1-EER(lab,score)\n2-cosine_distance(v1,v2)\n3-roc(lab,score)\n4-wer(ref, hyp)\n5-cer(ref, hyp)\n6-wer_list(ref_list , hyp_list)\n7-cer_list(ref_list , hyp_list)\n\nfrom iman import tsne:\n1-plot(fea , label)\n\nfrom iman import xvector:\n1-xvec,lda_xvec,gender = get(filename , model(model_path , model_name , model_speaker_num))\n\nfrom iman import web:\n1-change_wallpaper()\n2-dl(url)\n\n',
        packages=find_packages(),
        
        # add any additional packages that 
        # needs to be installed along with your package.
        install_requires=['scipy','numpy','six','matplotlib'], 
        
        keywords=['python', 'iman'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
        ]
)