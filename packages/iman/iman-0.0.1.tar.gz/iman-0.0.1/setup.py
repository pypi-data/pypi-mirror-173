from setuptools import setup, find_packages

setup(
        # the name must match the folder name 'verysimplemodule'
        name="iman", 
        version='0.0.1',
        author="Iman Sarraf",
        author_email="imansarraf@gmail.com",
        description='Python package for daily Tasks',
        long_description='from iman import Audio:\n1-Read, Resample and Write PCM and Alaw Files \n2-frame and split (VAD)\n3-ReadMp3 (with miniaudio)\n\n\nimport iman:\n1-plt\n2-now (get time)\n3-F (format floating point)\n4-D (format int number)\n5-Write_List\n6-Write_Dic\n7-Read (read txt file)\n8-Read_Lines (read txt file line by line and return list)\n9-Write (write string to file)\n10-gf (Get files in a directory)\n11-gfa (Get Files in a Directory and SubDirectories)\n12-ReadE (Read Excel files)\n\nfrom iman import info:\n1-Get info about cpu and gpu (need torch)\n\n\nfrom iman import metrics:\n1-EER(lab,score)\n2-cosine_distance\n3-roc(lab,score)\n\nfrom iman import tsne:\n1-tsne.plot(fea , label)\n\n',
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