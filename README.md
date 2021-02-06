# Coupled Filtering #

### Description ###

Description here

### Set up ###

#### for Python ####
1. Install python 3.8.3
>macOS [64-bit](https://www.python.org/ftp/python/3.8.3/python-3.8.3-macosx10.9.pkg)  
>Windows [32-bit](https://www.python.org/ftp/python/3.8.3/python-3.8.3-webinstall.exe) [64-bit](https://www.python.org/ftp/python/3.8.3/python-3.8.3-amd64-webinstall.exe)

#### for UI ####
1. Install PyQt5
>pip install PyQt5
2. Install Qt Designer (you can install Qt Designer alone or Qt Creator)
>* Qt Designer(unofficial) [here](https://build-system.fman.io/qt-designer-download)
>* Qt Creator(official) [here](https://www.qt.io/download-open-source)  
![Installation setting](https://puu.sh/GW277/f787f9f9be.png){width=600}

#### for Algorithm ####
1. Install NumPy
>pip install numpy==1.19.3

### Usage ###

### Remark ###
1. The Rnage of M and T are a number that is < 1. T should be a factor that will be multiplied to the image size.
2. The step of M < Range of M and < 1, while Step of T should be an integer and > 1. 
3. The input format for all parameters are *text. Assuming the range of axial and lateral strain and shear are the same, so as the interval.
4. The input file has to be .dat format

#### Refrences ###
1. T.Z. Liang, L.S. Yung and W.C. Yu, “On Feature Motion Decorrelation in Ultrasound Speckle Tracking,” in IEEE Transactions on Medical Imaging, vol. 32(2), 2013, pp. 435-448.