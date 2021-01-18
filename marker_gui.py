#!/usr/bin/env python

import argparse
import cv2 
from opencv_paint_chinese import putChineseText
import env
from util import log

import sys
import os.path

from gui.id_marker import Ui_MainWindow
from gui.about import Ui_Dialog as Ui_Dialog_about
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5 import QtWidgets, QtCore, QtGui
from MouseEventQLabel import MyQLabel


def ParseArguments(): 
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-debug",  help="Print Debug Log", action="store_true")

    args = ap.parse_args()
    env.DEBUG = args.debug

    return args


def frontButtonClicked():
    #options = QFileDialog.Options()
    fileName,_ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","Images (*.png *.bmp *.jpg)")
    if fileName:
       log(fileName)
       w.label.setText(fileName)
       #w.label.setAlignment(QtCore.Qt.AlignHCenter and QtCore.Qt.AlignVCenter)

       pic = QPixmap()
       pic.load(fileName)
       w.label_3.setPixmap(pic)
       w.label_3.setScaledContents(True)
        

def backButtonClicked():
    #options = QFileDialog.Options()
    fileName,_ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","Images (*.png *.bmp *.jpg)")
    if fileName:
       log(fileName)
       w.label_2.setText(fileName)
       #w.label_2.setAlignment(QtCore.Qt.AlignHCenter and QtCore.Qt.AlignVCenter)

       pic = QPixmap()
       pic.load(fileName)
       w.label_4.setPixmap(pic)
       w.label_4.setScaledContents(True)

def pathButtonClicked():
    options = QFileDialog.Options()
    log (options)
    #fileName,_ = QFileDialog.getOpenFileName(None,"QFileDialog.getOpenFileName()", "","All Files (*)", options=options)
    fileName = QFileDialog.getExistingDirectory(None,"Output Directory", "All Directories (*)", QFileDialog.ShowDirsOnly)
    
    if fileName:
       log(fileName)
       w.lineEdit_2.setText(fileName)

def outputButtonClicked():
    log ('Front Image:' + w.label.text())
    log ('Back Image:' + w.label_2.text())
    log ('Overlay text: ' + overlay.text())
    log (f'Overlay coordinates: ({overlay.x()},{overlay.y()})')

    if w.label.text() == '正面':
        QMessageBox.information(
        None, '警告',
        '請選擇一張正面照片',
        QMessageBox.Close)
    elif w.label_2.text() == '反面':
        QMessageBox.information(
        None, '警告',
        '請選擇一張反面照片',
        QMessageBox.Close)
    elif w.lineEdit.text() == '':
        QMessageBox.information(
        None, '警告',
        '請輸入要壓的字',
        QMessageBox.Close)
    elif w.lineEdit_2.text() == '':
        QMessageBox.information(
        None, '警告',
        '請選擇要輸出的路徑',
        QMessageBox.Close)
    else:
        front_image = cv2.imread(w.label.text())
        front_image_resize = cv2.resize (front_image, (320, 240), cv2.INTER_AREA)
        front_x = overlay.x() - 45
        front_y = overlay.y() - 140
        front_image_resize = putChineseText (front_image_resize, w.lineEdit.text(), (front_x, front_y), (0, 0, 0), env.FONT, 14)

        back_image = cv2.imread(w.label_2.text())
        back_image_resize = cv2.resize (back_image, (320, 240), cv2.INTER_AREA)
        back_x = overlay_2.x() - 45 - 370
        back_y = overlay_2.y() - 140
        back_image_resize = putChineseText (back_image_resize, w.lineEdit.text(), (back_x, back_y), (0, 0, 0), env.FONT, 14)

        _, origin_fname = os.path.split(w.label.text())
        _, origin_bname = os.path.split(w.label_2.text())
        fname = origin_fname[:origin_fname.rfind('.')] + '(' + w.lineEdit.text() + ')' + origin_fname[origin_fname.rfind('.'):]
        bname = origin_bname[:origin_bname.rfind('.')] + '(' + w.lineEdit.text() + ')' + origin_bname[origin_bname.rfind('.'):]

        cv2.imwrite(w.lineEdit_2.text() + os.path.sep + fname, front_image_resize)
        cv2.imwrite(w.lineEdit_2.text() + os.path.sep + bname, back_image_resize)
        QMessageBox.information(
        None, 'Success !',
        '輸出成功 !',
        QMessageBox.Close)
    

def handleTextChanged(text):
    if text != '':
        overlay.setText(text+'   ')
        overlay.setGeometry( overlay.x(), overlay.y(), overlay.fontMetrics().boundingRect(overlay.text()).width(), overlay.height())
        overlay.show()

        overlay_2.setText(text+'   ')
        overlay_2.setGeometry( overlay_2.x(), overlay_2.y(), overlay_2.fontMetrics().boundingRect(overlay_2.text()).width(), overlay_2.height())
        overlay_2.show()
    else:
        overlay.hide()
        overlay_2.hide()


ParseArguments()

app = QApplication(sys.argv)
ui_w = QtWidgets.QMainWindow()
w = Ui_MainWindow()
w.setupUi(ui_w)

ui_about = QtWidgets.QDialog()
about = Ui_Dialog_about()
about.setupUi(ui_about)


ui_w.show()
w.pushButton.clicked.connect(frontButtonClicked)
w.pushButton_2.clicked.connect(backButtonClicked)

w.pushButton_3.clicked.connect(pathButtonClicked)
w.pushButton_4.clicked.connect(outputButtonClicked)
w.pushButton_5.clicked.connect(app.exit)

w.action_4.triggered.connect(app.exit)
w.action_5.triggered.connect(ui_about.show)

about.pushButton.clicked.connect(ui_about.hide)


font = QtGui.QFont()
font.setFamily(env.FONT)
font.setPointSize(14)

overlay =MyQLabel (ui_w)
overlay.setGeometry (120, 250, 120,20)
overlay.setBoundary(w.label_3.geometry())
overlay.setFrameShape(QtWidgets.QFrame.Box)


overlay_2 =MyQLabel (ui_w)
overlay_2.setGeometry (490, 250, 120,20)
overlay_2.setBoundary(w.label_4.geometry())
overlay_2.setFrameShape(QtWidgets.QFrame.Box)

overlay.setFont (font)
overlay_2.setFont (font)

w.lineEdit.textChanged.connect(handleTextChanged)

app.exec_()

