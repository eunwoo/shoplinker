# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QMainWindow,
    QMenu, QMenuBar, QPushButton, QScrollArea,
    QSizePolicy, QSpacerItem, QStatusBar, QTabWidget,
    QTableWidget, QTableWidgetItem, QTreeWidget, QTreeWidgetItem,
    QVBoxLayout, QWidget)

from lineedit import LineEdit
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1016, 779)
        self.actionCategory = QAction(MainWindow)
        self.actionCategory.setObjectName(u"actionCategory")
        self.action = QAction(MainWindow)
        self.action.setObjectName(u"action")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_2 = QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.lineEdit = QLineEdit(self.groupBox)
        self.lineEdit.setObjectName(u"lineEdit")

        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)

        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.lineEdit_2 = LineEdit(self.groupBox)
        self.lineEdit_2.setObjectName(u"lineEdit_2")

        self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)


        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)


        self.horizontalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.verticalLayout_9 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_3 = QLabel(self.groupBox_2)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_10.addWidget(self.label_3)

        self.lineEdit_4 = QLineEdit(self.groupBox_2)
        self.lineEdit_4.setObjectName(u"lineEdit_4")

        self.horizontalLayout_10.addWidget(self.lineEdit_4)


        self.verticalLayout_8.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_5)

        self.pushButton_13 = QPushButton(self.groupBox_2)
        self.pushButton_13.setObjectName(u"pushButton_13")

        self.horizontalLayout_11.addWidget(self.pushButton_13)

        self.pushButton_14 = QPushButton(self.groupBox_2)
        self.pushButton_14.setObjectName(u"pushButton_14")

        self.horizontalLayout_11.addWidget(self.pushButton_14)


        self.verticalLayout_8.addLayout(self.horizontalLayout_11)


        self.verticalLayout_9.addLayout(self.verticalLayout_8)


        self.horizontalLayout.addWidget(self.groupBox_2)

        self.groupBox_3 = QGroupBox(self.centralwidget)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_11 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_4 = QLabel(self.groupBox_3)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_12.addWidget(self.label_4)

        self.lineEdit_5 = QLineEdit(self.groupBox_3)
        self.lineEdit_5.setObjectName(u"lineEdit_5")

        self.horizontalLayout_12.addWidget(self.lineEdit_5)


        self.verticalLayout_10.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_13.addItem(self.horizontalSpacer_6)

        self.pushButton_15 = QPushButton(self.groupBox_3)
        self.pushButton_15.setObjectName(u"pushButton_15")

        self.horizontalLayout_13.addWidget(self.pushButton_15)

        self.pushButton_16 = QPushButton(self.groupBox_3)
        self.pushButton_16.setObjectName(u"pushButton_16")

        self.horizontalLayout_13.addWidget(self.pushButton_16)


        self.verticalLayout_10.addLayout(self.horizontalLayout_13)


        self.verticalLayout_11.addLayout(self.verticalLayout_10)


        self.horizontalLayout.addWidget(self.groupBox_3)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 2)
        self.horizontalLayout.setStretch(2, 2)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.setObjectName(u"comboBox")

        self.horizontalLayout_2.addWidget(self.comboBox)

        self.comboBox_2 = QComboBox(self.centralwidget)
        self.comboBox_2.setObjectName(u"comboBox_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(3)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.comboBox_2.sizePolicy().hasHeightForWidth())
        self.comboBox_2.setSizePolicy(sizePolicy1)
        self.comboBox_2.setMinimumSize(QSize(150, 0))

        self.horizontalLayout_2.addWidget(self.comboBox_2)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_2.addWidget(self.pushButton)

        self.pushButton_9 = QPushButton(self.centralwidget)
        self.pushButton_9.setObjectName(u"pushButton_9")

        self.horizontalLayout_2.addWidget(self.pushButton_9)

        self.pushButton_10 = QPushButton(self.centralwidget)
        self.pushButton_10.setObjectName(u"pushButton_10")

        self.horizontalLayout_2.addWidget(self.pushButton_10)

        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout_2.addWidget(self.pushButton_2)

        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout_2.addWidget(self.pushButton_3)

        self.pushButton_11 = QPushButton(self.centralwidget)
        self.pushButton_11.setObjectName(u"pushButton_11")

        self.horizontalLayout_2.addWidget(self.pushButton_11)

        self.pushButton_6 = QPushButton(self.centralwidget)
        self.pushButton_6.setObjectName(u"pushButton_6")

        self.horizontalLayout_2.addWidget(self.pushButton_6)

        self.label_11 = QLabel(self.centralwidget)
        self.label_11.setObjectName(u"label_11")

        self.horizontalLayout_2.addWidget(self.label_11)

        self.lineEdit_7 = QLineEdit(self.centralwidget)
        self.lineEdit_7.setObjectName(u"lineEdit_7")

        self.horizontalLayout_2.addWidget(self.lineEdit_7)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.label_12 = QLabel(self.centralwidget)
        self.label_12.setObjectName(u"label_12")
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)

        self.horizontalLayout_14.addWidget(self.label_12)

        self.label_13 = QLabel(self.centralwidget)
        self.label_13.setObjectName(u"label_13")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(1)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy2)

        self.horizontalLayout_14.addWidget(self.label_13)


        self.verticalLayout.addLayout(self.horizontalLayout_14)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setTabShape(QTabWidget.TabShape.Rounded)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.verticalLayout_12 = QVBoxLayout(self.tab)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_13 = QVBoxLayout()
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.lineEdit_6 = QLineEdit(self.tab)
        self.lineEdit_6.setObjectName(u"lineEdit_6")

        self.horizontalLayout_3.addWidget(self.lineEdit_6)

        self.pushButton_24 = QPushButton(self.tab)
        self.pushButton_24.setObjectName(u"pushButton_24")

        self.horizontalLayout_3.addWidget(self.pushButton_24)

        self.pushButton_17 = QPushButton(self.tab)
        self.pushButton_17.setObjectName(u"pushButton_17")

        self.horizontalLayout_3.addWidget(self.pushButton_17)

        self.pushButton_18 = QPushButton(self.tab)
        self.pushButton_18.setObjectName(u"pushButton_18")

        self.horizontalLayout_3.addWidget(self.pushButton_18)

        self.pushButton_27 = QPushButton(self.tab)
        self.pushButton_27.setObjectName(u"pushButton_27")

        self.horizontalLayout_3.addWidget(self.pushButton_27)

        self.pushButton_19 = QPushButton(self.tab)
        self.pushButton_19.setObjectName(u"pushButton_19")

        self.horizontalLayout_3.addWidget(self.pushButton_19)

        self.pushButton_23 = QPushButton(self.tab)
        self.pushButton_23.setObjectName(u"pushButton_23")

        self.horizontalLayout_3.addWidget(self.pushButton_23)

        self.pushButton_26 = QPushButton(self.tab)
        self.pushButton_26.setObjectName(u"pushButton_26")

        self.horizontalLayout_3.addWidget(self.pushButton_26)

        self.pushButton_25 = QPushButton(self.tab)
        self.pushButton_25.setObjectName(u"pushButton_25")

        self.horizontalLayout_3.addWidget(self.pushButton_25)

        self.pushButton_5 = QPushButton(self.tab)
        self.pushButton_5.setObjectName(u"pushButton_5")

        self.horizontalLayout_3.addWidget(self.pushButton_5)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)


        self.verticalLayout_13.addLayout(self.horizontalLayout_3)

        self.tableWidget = QTableWidget(self.tab)
        self.tableWidget.setObjectName(u"tableWidget")

        self.verticalLayout_13.addWidget(self.tableWidget)


        self.verticalLayout_12.addLayout(self.verticalLayout_13)

        self.tabWidget.addTab(self.tab, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.verticalLayout_6 = QVBoxLayout(self.tab_4)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.lineEdit_3 = QLineEdit(self.tab_4)
        self.lineEdit_3.setObjectName(u"lineEdit_3")

        self.horizontalLayout_9.addWidget(self.lineEdit_3)

        self.pushButton_7 = QPushButton(self.tab_4)
        self.pushButton_7.setObjectName(u"pushButton_7")

        self.horizontalLayout_9.addWidget(self.pushButton_7)

        self.pushButton_8 = QPushButton(self.tab_4)
        self.pushButton_8.setObjectName(u"pushButton_8")

        self.horizontalLayout_9.addWidget(self.pushButton_8)

        self.pushButton_20 = QPushButton(self.tab_4)
        self.pushButton_20.setObjectName(u"pushButton_20")
        self.pushButton_20.setStyleSheet(u"background-color:rgb(49, 157, 229)")

        self.horizontalLayout_9.addWidget(self.pushButton_20)

        self.checkBox = QCheckBox(self.tab_4)
        self.checkBox.setObjectName(u"checkBox")

        self.horizontalLayout_9.addWidget(self.checkBox)

        self.pushButton_21 = QPushButton(self.tab_4)
        self.pushButton_21.setObjectName(u"pushButton_21")

        self.horizontalLayout_9.addWidget(self.pushButton_21)

        self.pushButton_22 = QPushButton(self.tab_4)
        self.pushButton_22.setObjectName(u"pushButton_22")

        self.horizontalLayout_9.addWidget(self.pushButton_22)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_4)


        self.verticalLayout_5.addLayout(self.horizontalLayout_9)

        self.tableWidget_2 = QTableWidget(self.tab_4)
        self.tableWidget_2.setObjectName(u"tableWidget_2")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.tableWidget_2.sizePolicy().hasHeightForWidth())
        self.tableWidget_2.setSizePolicy(sizePolicy3)
        self.tableWidget_2.setMinimumSize(QSize(0, 60))
        self.tableWidget_2.setMaximumSize(QSize(16777215, 60))

        self.verticalLayout_5.addWidget(self.tableWidget_2)

        self.tableWidget_3 = QTableWidget(self.tab_4)
        self.tableWidget_3.setObjectName(u"tableWidget_3")
        sizePolicy3.setHeightForWidth(self.tableWidget_3.sizePolicy().hasHeightForWidth())
        self.tableWidget_3.setSizePolicy(sizePolicy3)
        self.tableWidget_3.setMinimumSize(QSize(0, 60))
        self.tableWidget_3.setMaximumSize(QSize(16777215, 60))

        self.verticalLayout_5.addWidget(self.tableWidget_3)

        self.scrollArea = QScrollArea(self.tab_4)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 951, 1332))
        self.verticalLayout_7 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.label_6 = QLabel(self.scrollAreaWidgetContents)
        self.label_6.setObjectName(u"label_6")

        self.verticalLayout_7.addWidget(self.label_6)

        self.listWidget_11 = QListWidget(self.scrollAreaWidgetContents)
        self.listWidget_11.setObjectName(u"listWidget_11")
        sizePolicy3.setHeightForWidth(self.listWidget_11.sizePolicy().hasHeightForWidth())
        self.listWidget_11.setSizePolicy(sizePolicy3)

        self.verticalLayout_7.addWidget(self.listWidget_11)

        self.label_7 = QLabel(self.scrollAreaWidgetContents)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout_7.addWidget(self.label_7)

        self.listWidget_12 = QListWidget(self.scrollAreaWidgetContents)
        self.listWidget_12.setObjectName(u"listWidget_12")
        sizePolicy3.setHeightForWidth(self.listWidget_12.sizePolicy().hasHeightForWidth())
        self.listWidget_12.setSizePolicy(sizePolicy3)

        self.verticalLayout_7.addWidget(self.listWidget_12)

        self.label_8 = QLabel(self.scrollAreaWidgetContents)
        self.label_8.setObjectName(u"label_8")

        self.verticalLayout_7.addWidget(self.label_8)

        self.listWidget_13 = QListWidget(self.scrollAreaWidgetContents)
        self.listWidget_13.setObjectName(u"listWidget_13")
        sizePolicy3.setHeightForWidth(self.listWidget_13.sizePolicy().hasHeightForWidth())
        self.listWidget_13.setSizePolicy(sizePolicy3)

        self.verticalLayout_7.addWidget(self.listWidget_13)

        self.label_5 = QLabel(self.scrollAreaWidgetContents)
        self.label_5.setObjectName(u"label_5")

        self.verticalLayout_7.addWidget(self.label_5)

        self.listWidget_10 = QListWidget(self.scrollAreaWidgetContents)
        self.listWidget_10.setObjectName(u"listWidget_10")
        sizePolicy3.setHeightForWidth(self.listWidget_10.sizePolicy().hasHeightForWidth())
        self.listWidget_10.setSizePolicy(sizePolicy3)

        self.verticalLayout_7.addWidget(self.listWidget_10)

        self.label_9 = QLabel(self.scrollAreaWidgetContents)
        self.label_9.setObjectName(u"label_9")

        self.verticalLayout_7.addWidget(self.label_9)

        self.listWidget_14 = QListWidget(self.scrollAreaWidgetContents)
        self.listWidget_14.setObjectName(u"listWidget_14")
        sizePolicy3.setHeightForWidth(self.listWidget_14.sizePolicy().hasHeightForWidth())
        self.listWidget_14.setSizePolicy(sizePolicy3)

        self.verticalLayout_7.addWidget(self.listWidget_14)

        self.label_10 = QLabel(self.scrollAreaWidgetContents)
        self.label_10.setObjectName(u"label_10")

        self.verticalLayout_7.addWidget(self.label_10)

        self.listWidget_15 = QListWidget(self.scrollAreaWidgetContents)
        self.listWidget_15.setObjectName(u"listWidget_15")
        sizePolicy3.setHeightForWidth(self.listWidget_15.sizePolicy().hasHeightForWidth())
        self.listWidget_15.setSizePolicy(sizePolicy3)

        self.verticalLayout_7.addWidget(self.listWidget_15)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_5.addWidget(self.scrollArea)


        self.verticalLayout_6.addLayout(self.verticalLayout_5)

        self.tabWidget.addTab(self.tab_4, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.horizontalLayout_6 = QHBoxLayout(self.tab_3)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.listWidget = QListWidget(self.tab_3)
        self.listWidget.setObjectName(u"listWidget")

        self.horizontalLayout_5.addWidget(self.listWidget)

        self.listWidget_2 = QListWidget(self.tab_3)
        self.listWidget_2.setObjectName(u"listWidget_2")

        self.horizontalLayout_5.addWidget(self.listWidget_2)

        self.listWidget_3 = QListWidget(self.tab_3)
        self.listWidget_3.setObjectName(u"listWidget_3")

        self.horizontalLayout_5.addWidget(self.listWidget_3)

        self.listWidget_4 = QListWidget(self.tab_3)
        self.listWidget_4.setObjectName(u"listWidget_4")

        self.horizontalLayout_5.addWidget(self.listWidget_4)

        self.listWidget_5 = QListWidget(self.tab_3)
        self.listWidget_5.setObjectName(u"listWidget_5")

        self.horizontalLayout_5.addWidget(self.listWidget_5)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.listWidget_6 = QListWidget(self.tab_3)
        self.listWidget_6.setObjectName(u"listWidget_6")

        self.horizontalLayout_8.addWidget(self.listWidget_6)

        self.listWidget_7 = QListWidget(self.tab_3)
        self.listWidget_7.setObjectName(u"listWidget_7")

        self.horizontalLayout_8.addWidget(self.listWidget_7)

        self.listWidget_8 = QListWidget(self.tab_3)
        self.listWidget_8.setObjectName(u"listWidget_8")

        self.horizontalLayout_8.addWidget(self.listWidget_8)

        self.listWidget_9 = QListWidget(self.tab_3)
        self.listWidget_9.setObjectName(u"listWidget_9")

        self.horizontalLayout_8.addWidget(self.listWidget_9)


        self.verticalLayout_3.addLayout(self.horizontalLayout_8)


        self.horizontalLayout_6.addLayout(self.verticalLayout_3)

        self.tabWidget.addTab(self.tab_3, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.horizontalLayout_4 = QHBoxLayout(self.tab_2)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.pushButton_4 = QPushButton(self.tab_2)
        self.pushButton_4.setObjectName(u"pushButton_4")

        self.horizontalLayout_7.addWidget(self.pushButton_4)

        self.pushButton_12 = QPushButton(self.tab_2)
        self.pushButton_12.setObjectName(u"pushButton_12")

        self.horizontalLayout_7.addWidget(self.pushButton_12)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_3)


        self.verticalLayout_4.addLayout(self.horizontalLayout_7)

        self.treeWidget = QTreeWidget(self.tab_2)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.treeWidget.setHeaderItem(__qtreewidgetitem)
        self.treeWidget.setObjectName(u"treeWidget")

        self.verticalLayout_4.addWidget(self.treeWidget)


        self.horizontalLayout_4.addLayout(self.verticalLayout_4)

        self.tabWidget.addTab(self.tab_2, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.verticalLayout.setStretch(3, 1)

        self.verticalLayout_2.addLayout(self.verticalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1016, 33))
        self.menubar.setAutoFillBackground(True)
        self.menuSetting = QMenu(self.menubar)
        self.menuSetting.setObjectName(u"menuSetting")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuSetting.menuAction())
        self.menuSetting.addAction(self.action)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionCategory.setText(QCoreApplication.translate("MainWindow", u"Category", None))
        self.action.setText(QCoreApplication.translate("MainWindow", u"\uce74\ud14c\uace0\ub9ac", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"\ub85c\uadf8\uc778", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"ID", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"PW", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"\ub370\uc774\ud130\ud3f4\ub354", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\ud3f4\ub354\uba85", None))
        self.pushButton_13.setText(QCoreApplication.translate("MainWindow", u"\ud3f4\ub354\uc120\ud0dd", None))
        self.pushButton_14.setText(QCoreApplication.translate("MainWindow", u"\ud3f4\ub354\uc5f4\uae30", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"\uace0\uac1d\uc0ac\uce74\ud14c\uace0\ub9ac \uc124\uc815", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\ud30c\uc77c\uba85", None))
        self.pushButton_15.setText(QCoreApplication.translate("MainWindow", u"\ud30c\uc77c\uc120\ud0dd", None))
        self.pushButton_16.setText(QCoreApplication.translate("MainWindow", u"\ud30c\uc77c\uc5f4\uae30", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\uce74\ud14c\uace0\ub9ac \uac00\uc838\uc624\uae30", None))
        self.pushButton_9.setText(QCoreApplication.translate("MainWindow", u"\ub300\ubd84\ub958\ub9cc \uac00\uc838\uc624\uae30", None))
        self.pushButton_10.setText(QCoreApplication.translate("MainWindow", u"\ud30c\uc77c\uc5f4\uae30", None))
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"\uc800\uc7a5", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"\ubd88\ub7ec\uc624\uae30", None))
        self.pushButton_11.setText(QCoreApplication.translate("MainWindow", u"\ubaa8\ub450\uc9c0\uc6b0\uae30", None))
        self.pushButton_6.setText(QCoreApplication.translate("MainWindow", u"Pause", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"\ub300\uae30\uc2dc\uac04:", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"\ud06c\ub86c \ub4dc\ub77c\uc774\ubc84 \ubc84\uc804", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.pushButton_24.setText(QCoreApplication.translate("MainWindow", u"\ud0a4\uc6cc\ub4dc\uac80\uc0c9", None))
        self.pushButton_17.setText(QCoreApplication.translate("MainWindow", u"\ud0a4\uc6cc\ub4dc\uac80\uc0c9 \ub9ac\uc14b", None))
        self.pushButton_18.setText(QCoreApplication.translate("MainWindow", u"\uc120\ud0dd\ud589\uc0ad\uc81c", None))
        self.pushButton_27.setText(QCoreApplication.translate("MainWindow", u"\uc120\ud0dd\uc140\uc0ad\uc81c", None))
        self.pushButton_19.setText(QCoreApplication.translate("MainWindow", u"\uc804\uccb4\uc0ad\uc81c", None))
        self.pushButton_23.setText(QCoreApplication.translate("MainWindow", u"\uc120\ud0dd\uc5c5\ub85c\ub4dc", None))
        self.pushButton_26.setText(QCoreApplication.translate("MainWindow", u"\uc804\uccb4\uc5c5\ub85c\ub4dc", None))
        self.pushButton_25.setText(QCoreApplication.translate("MainWindow", u"\uc120\ud0dd\uc5f4 \uc624\ub984\ucc28\uc21c", None))
        self.pushButton_5.setText(QCoreApplication.translate("MainWindow", u"Test", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"\ub0b4 \uce74\ud14c\uace0\ub9ac", None))
        self.pushButton_7.setText(QCoreApplication.translate("MainWindow", u"\uac80\uc0c9", None))
        self.pushButton_8.setText(QCoreApplication.translate("MainWindow", u"\ub0b4 \uce74\ud14c\uace0\ub9ac\uc5d0 \uc800\uc7a5", None))
        self.pushButton_20.setText(QCoreApplication.translate("MainWindow", u"\uc0f5\ub9c1\ucee4 \uc5c5\ub85c\ub4dc", None))
        self.checkBox.setText(QCoreApplication.translate("MainWindow", u"\uace0\uac1d\uc0ac\uce74\ud14c\uace0\ub9ac \ubaa8\ub450\ud45c\uc2dc", None))
        self.pushButton_21.setText(QCoreApplication.translate("MainWindow", u"\uac80\uc0c9\uacb0\uacfc\uc0ad\uc81c", None))
        self.pushButton_22.setText(QCoreApplication.translate("MainWindow", u"\uc120\ud0dd\uc1fc\ud551\ubab0 \ub9e4\uce6d \uc0ad\uc81c", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"\uc2a4\ub9c8\ud2b8\uc2a4\ud1a0\uc5b4", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"\ucfe0\ud321", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"\uc9c0\ub9c8\ucf13", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"11\ubc88\uac00", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"\uc625\uc158", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"\uce74\ud39824", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"\uac80\uc0c9", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"\ub9ac\uc2a4\ud2b8", None))
        self.pushButton_4.setText(QCoreApplication.translate("MainWindow", u"\ubaa8\ub450 \ud3bc\uce58\uae30", None))
        self.pushButton_12.setText(QCoreApplication.translate("MainWindow", u"\ubaa8\ub450 \uc811\uae30", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Tree", None))
        self.menuSetting.setTitle(QCoreApplication.translate("MainWindow", u"\uc124\uc815", None))
    # retranslateUi

