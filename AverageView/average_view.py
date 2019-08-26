# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AverageView\average_view.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AverageView(object):
    def setupUi(self, AverageView):
        AverageView.setObjectName("AverageView")
        AverageView.resize(984, 709)
        self.centralwidget = QtWidgets.QWidget(AverageView)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.avgNumSpinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.avgNumSpinBox.setMinimumSize(QtCore.QSize(811, 0))
        self.avgNumSpinBox.setMinimum(1)
        self.avgNumSpinBox.setMaximum(9999999)
        self.avgNumSpinBox.setProperty("value", 5)
        self.avgNumSpinBox.setObjectName("avgNumSpinBox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.avgNumSpinBox)
        self.verticalLayout_2.addLayout(self.formLayout)
        self.browseButton = QtWidgets.QPushButton(self.centralwidget)
        self.browseButton.setObjectName("browseButton")
        self.verticalLayout_2.addWidget(self.browseButton, 0, QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_2.addWidget(self.progressBar)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout = QtWidgets.QGridLayout(self.tab)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_5.addWidget(self.label_3)
        self.eastStdTableView = QtWidgets.QTableView(self.tab)
        self.eastStdTableView.setObjectName("eastStdTableView")
        self.verticalLayout_5.addWidget(self.eastStdTableView)
        self.gridLayout.addLayout(self.verticalLayout_5, 0, 0, 1, 1)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_4.addWidget(self.label_2)
        self.eastAvgTableView = QtWidgets.QTableView(self.tab)
        self.eastAvgTableView.setObjectName("eastAvgTableView")
        self.verticalLayout_4.addWidget(self.eastAvgTableView)
        self.gridLayout.addLayout(self.verticalLayout_4, 1, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.eastTableView = QtWidgets.QTableView(self.tab)
        self.eastTableView.setObjectName("eastTableView")
        self.verticalLayout.addWidget(self.eastTableView)
        self.gridLayout.addLayout(self.verticalLayout, 2, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.northTableView = QtWidgets.QTableView(self.tab_2)
        self.northTableView.setObjectName("northTableView")
        self.verticalLayout_3.addWidget(self.northTableView)
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout_2.addWidget(self.tabWidget)
        AverageView.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(AverageView)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 984, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        AverageView.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(AverageView)
        self.statusbar.setObjectName("statusbar")
        AverageView.setStatusBar(self.statusbar)
        self.actionSelect_Files = QtWidgets.QAction(AverageView)
        self.actionSelect_Files.setObjectName("actionSelect_Files")
        self.menuFile.addAction(self.actionSelect_Files)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(AverageView)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(AverageView)

    def retranslateUi(self, AverageView):
        _translate = QtCore.QCoreApplication.translate
        AverageView.setWindowTitle(_translate("AverageView", "MainWindow"))
        self.label_4.setText(_translate("AverageView", "Number Ensembles to Average"))
        self.browseButton.setText(_translate("AverageView", "Browse"))
        self.label_3.setText(_translate("AverageView", "Bin Standard Deviation"))
        self.label_2.setText(_translate("AverageView", "Bin Average"))
        self.label.setText(_translate("AverageView", "Averaged Data"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("AverageView", "East Velocity"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("AverageView", "North Velocity"))
        self.menuFile.setTitle(_translate("AverageView", "File"))
        self.actionSelect_Files.setText(_translate("AverageView", "Select Files"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AverageView = QtWidgets.QMainWindow()
    ui = Ui_AverageView()
    ui.setupUi(AverageView)
    AverageView.show()
    sys.exit(app.exec_())

