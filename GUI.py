# 2020 FYP ECE
# This software is designed to use on Window environment

import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QToolButton, QMainWindow, QApplication, QFileDialog
import Core
import elastogram 
import numpy as np

correlation_B4= 1
correlation_after= 1
correlation = np.empty([193,129])
axial_strains = np.empty([193,129])
lateral_strains = np.empty([193,129])
axial_shears = np.empty([193,129])
lateral_shears = np.empty([193,129])
PreFile= "./simulation/2-D_Simulation_Data/rf_2media_0percent_FieldII.dat"
PostFile= "./simulation/2-D_Simulation_Data/rf_2media_0percent_FieldII.dat"

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.core = Core.Core("./simulation/2-D_Simulation_Data/rf_2media_0percent_FieldII.dat", "./simulation/2-D_Simulation_Data/rf_2media_0percent_FieldII.dat", "1 0 0 0", "1 0 0 0", "1 1", "1 1")
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(815, 621)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.PostFileBrowse = QtWidgets.QPushButton(self.centralwidget)
        self.PostFileBrowse.setGeometry(QtCore.QRect(620, 118, 91, 26))
        self.PostFileBrowse.setObjectName("PostFileBrowse")
        font = QtGui.QFont()
        font.setPointSize(10)
        self.PostFileBrowse.setFont(font)
        self.PostFileBrowse.clicked.connect(self.PostBrowse) #click function
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(670, 490, 113, 32))
        self.pushButton_3.setObjectName("pushButton_3")
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_3.setFont(font)
        self.pushButton_3.clicked.connect(self.Clickme) #click function
        self.pushButton_3.clicked.connect(self.start) #click function: start algorithm
        self.pushButton_3.clicked.connect(self.GUI_correlation_B4) #click function
        self.pushButton_3.clicked.connect(self.GUI_correlation_after) #click function
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(140, 80, 211, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.PreFileBrowse = QtWidgets.QPushButton(self.centralwidget)
        self.PreFileBrowse.setGeometry(QtCore.QRect(230, 118, 91, 26))
        self.PreFileBrowse.setObjectName("PreFileBrowse")
        font = QtGui.QFont()
        font.setPointSize(10)
        self.PreFileBrowse.setFont(font)
        self.PreFileBrowse.clicked.connect(self.PreBrowse) #click function
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(310, 20, 201, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.PreFileDisplay = QtWidgets.QTextBrowser(self.centralwidget)
        self.PreFileDisplay.setGeometry(QtCore.QRect(100, 120, 111, 23))
        self.PreFileDisplay.setObjectName("PreFileDisplay")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(40, 460, 591, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.PostFileDisplay = QtWidgets.QTextBrowser(self.centralwidget)
        self.PostFileDisplay.setGeometry(QtCore.QRect(490, 120, 111, 23))
        self.PostFileDisplay.setObjectName("PostFileDisplay")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(560, 250, 121, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        font.setPointSize(11)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(110, 370, 111, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(500, 80, 201, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.T_Step = QtWidgets.QLineEdit(self.centralwidget)
        self.T_Step.setGeometry(QtCore.QRect(580, 370, 113, 21))
        self.T_Step.setObjectName("T_Step")
        self.M_Range = QtWidgets.QLineEdit(self.centralwidget)
        self.M_Range.setGeometry(QtCore.QRect(220, 320, 113, 21))
        self.M_Range.setObjectName("M_Range")
        self.T_Range = QtWidgets.QLineEdit(self.centralwidget)
        self.T_Range.setGeometry(QtCore.QRect(580, 320, 113, 21))
        self.T_Range.setObjectName("T_Range")
        self.M_Step = QtWidgets.QLineEdit(self.centralwidget)
        self.M_Step.setGeometry(QtCore.QRect(220, 370, 113, 21))
        self.M_Step.setObjectName("M_Step")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(470, 370, 111, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(350, 200, 171, 16))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        font.setPointSize(11)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(180, 250, 101, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        font.setPointSize(11)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(110, 320, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        self.label_14.setGeometry(QtCore.QRect(470, 320, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 815, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.PostFileBrowse.setText(_translate("MainWindow", "Browse File"))
        self.pushButton_3.setText(_translate("MainWindow", "Process Data"))
        self.label_2.setText(_translate("MainWindow", "Pre-Compression Image"))
        self.PreFileBrowse.setText(_translate("MainWindow", "Browse File"))
        self.label.setText(_translate("MainWindow", "Coupled Filtering Algorithm"))
        self.label_10.setText(_translate("MainWindow", "Note: T & M are the tissue motion parameters which describe the image after compression."))
        self.label_6.setText(_translate("MainWindow", "Matrix T"))
        self.label_9.setText(_translate("MainWindow", "Interval of M:"))
        self.label_3.setText(_translate("MainWindow", "Post-Compression Image"))
        self.label_8.setText(_translate("MainWindow", "Interval of T:"))
        self.label_4.setText(_translate("MainWindow", "Input Variables"))
        self.label_7.setText(_translate("MainWindow", "Matrix M"))
        self.label_12.setText(_translate("MainWindow", "Range of M:"))
        self.label_14.setText(_translate("MainWindow", "Range of T:"))

    def start(self):
        global PreFile
        global PostFile
        self.core = Core.Core(PreFile, PostFile, self.M_Range.text(), self.M_Step.text(), self.T_Range.text(), self.T_Step.text())
        self.core.start_algo(1, True, 2, 6)
        global axial_shears
        global axial_strains
        global lateral_shears
        global lateral_strains
        global correlation
        correlation = self.core.get_correlation()
        axial_strains = self.core.get_axial_strain()
        lateral_strains = self.core.get_lateral_strain() 
        axial_shears = self.core.get_axial_shear() 
        lateral_shears = self.core.get_lateral_shear() 
        
    def Clickme(self):
        M_Interval= self.M_Step.text()
        print(M_Interval)

        T_Interval= self.T_Step.text()
        print(T_Interval)

        Range_T= self.T_Range.text()
        print(Range_T)          

        Range_M= self.M_Range.text()
        print(Range_M) 

        SecDialog = QtWidgets.QDialog()
        ui = Ui_SecDialog()
        ui.setupUi(SecDialog)
        SecDialog.show()
        SecDialog.setModal(True)
        SecDialog.exec()

    def GUI_correlation_B4(self): #NEED CHECK
        correlation_B4_ = 0
        for y in range(0, self.core.algo.windows.shape[0]):
            for x in range(0, self.core.algo.windows.shape[1]):
                GUI_sliced_pre, GUI_sliced_post = self.core.algo.slice_image(self.core.algo.pre_img, self.core.algo.post_img, self.core.algo.windows[y, x])
                correlation_B4_ += self.core.algo.correlation(GUI_sliced_pre, GUI_sliced_post)
        global correlation_B4
        correlation_B4=  correlation_B4_ / (self.core.algo.num_win[0]*self.core.algo.num_win[1])

    def GUI_correlation_after(self): #NEED CHECK
        correlation_after_ = 0
        for y in range(0, self.core.algo.windows.shape[0]):
            for x in range(0, self.core.algo.windows.shape[1]):
                correlation_after_ += self.core.algo.windows[y, x].opt_c
        global correlation_after
        correlation_after= correlation_after_ / (self.core.algo.num_win[0]*self.core.algo.num_win[1])

    def PreBrowse(self):
        try:
            global PreFile
            PreFile= QFileDialog.getOpenFileName(None, 'Single File', '','*.dat') #change file type
            Path_PreFile= PreFile[0]
            PreFileName= Path_PreFile.split("/")[-1]
            print(PreFileName)
            self.PreFileDisplay.setText(PreFileName) #Display Browse File
            font = QtGui.QFont()
            font.setPointSize(12)
            # with open(Path_PreFile, 'r') as f:
            #     print(f.readlines())
        except:
            pass

    def PostBrowse(self):
        try:
            global PostFile
            PostFile= QFileDialog.getOpenFileName(None, 'Single File', '','*.dat') #change file type
            Path_PostFile= PostFile[0]
            PostFileName= Path_PostFile.split("/")[-1]
            self.PostFileDisplay.setText(PostFileName) #Display Browse File
            font = QtGui.QFont()
            font.setPointSize(12)
            # with open(Path_PostFile, 'r') as f:
            #     print(f.readlines())
        except:
            pass

class Ui_SecDialog(object):
    def setupUi(self, SecDialog):
        SecDialog.setObjectName("SecDialog")
        SecDialog.resize(660, 449)
        self.B4_AWarping = QtWidgets.QTextBrowser(SecDialog)
        self.B4_AWarping.setGeometry(QtCore.QRect(390, 170, 101, 28))
        self.B4_AWarping.setObjectName("B4_AWarping")
        self.B4_AWarping.setText(str(correlation_B4)) #Variable Name Display data
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_5 = QtWidgets.QLabel(SecDialog)
        self.label_5.setGeometry(QtCore.QRect(150, 225, 215, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.After_CFiltering = QtWidgets.QTextBrowser(SecDialog)
        self.After_CFiltering.setGeometry(QtCore.QRect(390, 220, 101, 28))
        self.After_CFiltering.setObjectName("After_CFiltering")
        self.After_CFiltering.setText(str(correlation_after)) #Variable Name Display data
        font = QtGui.QFont()
        font.setPointSize(11)
        self.After_CFiltering.setFont(font)
        self.pushButton_2 = QtWidgets.QPushButton(SecDialog)
        self.pushButton_2.setGeometry(QtCore.QRect(250, 360, 171, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_2.setFont(font)
        self.pushButton_2.clicked.connect(self.output) #click function
        self.label_2 = QtWidgets.QLabel(SecDialog)
        self.label_2.setGeometry(QtCore.QRect(370, 105, 153, 23))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(SecDialog)
        self.label_3.setGeometry(QtCore.QRect(150, 175, 217, 18))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label = QtWidgets.QLabel(SecDialog)
        self.label.setGeometry(QtCore.QRect(310, 50, 74, 23))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.retranslateUi(SecDialog)
        QtCore.QMetaObject.connectSlotsByName(SecDialog)

    def retranslateUi(self, SecDialog):
        _translate = QtCore.QCoreApplication.translate
        SecDialog.setWindowTitle(_translate("SecDialog", "Result Window"))
        self.label_5.setText(_translate("SecDialog", "After Coupled Filtering Method:"))
        self.pushButton_2.setText(_translate("SecDialog", "Output elastogram"))
        self.label_2.setText(_translate("SecDialog", "Correlation Coefficient"))
        self.label_3.setText(_translate("SecDialog", "Before Affine Warping Procedure:"))
        self.label.setText(_translate("SecDialog", "Result"))

    def output(self):
        global axial_shears
        global axial_strains
        global lateral_shears
        global lateral_strains
        global correlation
        elastogram.output_graph(correlation, axial_strains, lateral_strains, axial_shears, lateral_shears)
        
def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()

