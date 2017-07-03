# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_ppconverter.ui'
#
# Created: Sun Dec  8 22:44:06 2013
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_PPConverter(object):
    def setupUi(self, PPConverter):
        PPConverter.setObjectName(_fromUtf8("PPConverter"))
        PPConverter.setWindowModality(QtCore.Qt.NonModal)
        PPConverter.resize(583, 403)
        PPConverter.setAcceptDrops(True)
        PPConverter.setWindowTitle(_fromUtf8("PPConverter"))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        PPConverter.setWindowIcon(icon)
        PPConverter.setSizeGripEnabled(False)
        PPConverter.setModal(False)
        self.buttonBox = QtGui.QDialogButtonBox(PPConverter)
        self.buttonBox.setGeometry(QtCore.QRect(80, 350, 461, 32))
        self.buttonBox.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.tabWidget = QtGui.QTabWidget(PPConverter)
        self.tabWidget.setGeometry(QtCore.QRect(40, 30, 501, 301))
        self.tabWidget.setAcceptDrops(True)
        self.tabWidget.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.groupBox = QtGui.QGroupBox(self.tab)
        self.groupBox.setGeometry(QtCore.QRect(30, 20, 431, 91))
        self.groupBox.setAcceptDrops(True)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.inButton = QtGui.QToolButton(self.groupBox)
        self.inButton.setGeometry(QtCore.QRect(380, 40, 30, 23))
        self.inButton.setObjectName(_fromUtf8("inButton"))
        self.inTiff = QtGui.QLineEdit(self.groupBox)
        self.inTiff.setEnabled(True)
        self.inTiff.setGeometry(QtCore.QRect(20, 40, 341, 22))
        self.inTiff.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.inTiff.setDragEnabled(True)
        self.inTiff.setObjectName(_fromUtf8("inTiff"))
        self.groupBox_2 = QtGui.QGroupBox(self.tab)
        self.groupBox_2.setGeometry(QtCore.QRect(30, 150, 431, 91))
        self.groupBox_2.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.outButton = QtGui.QToolButton(self.groupBox_2)
        self.outButton.setGeometry(QtCore.QRect(380, 40, 30, 23))
        self.outButton.setLocale(QtCore.QLocale(QtCore.QLocale.German, QtCore.QLocale.Germany))
        self.outButton.setObjectName(_fromUtf8("outButton"))
        self.outTiff = QtGui.QLineEdit(self.groupBox_2)
        self.outTiff.setEnabled(True)
        self.outTiff.setGeometry(QtCore.QRect(20, 40, 341, 22))
        self.outTiff.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.outTiff.setObjectName(_fromUtf8("outTiff"))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.label = QtGui.QLabel(self.tab_2)
        self.label.setGeometry(QtCore.QRect(30, 20, 441, 241))
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label.setWordWrap(True)
        self.label.setObjectName(_fromUtf8("label"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))

        self.retranslateUi(PPConverter)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), PPConverter.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), PPConverter.reject)
        QtCore.QMetaObject.connectSlotsByName(PPConverter)

    def retranslateUi(self, PPConverter):
        self.groupBox.setTitle(_translate("PPConverter", "Input:", None))
        self.inButton.setText(_translate("PPConverter", "...", None))
        self.inTiff.setPlaceholderText(_translate("PPConverter", "Input filepath", None))
        self.groupBox_2.setTitle(_translate("PPConverter", "Output:", None))
        self.outButton.setText(_translate("PPConverter", "...", None))
        self.outTiff.setPlaceholderText(_translate("PPConverter", "Output filepath", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("PPConverter", "Choose image", None))
        self.label.setText(_translate("PPConverter", "This plugin is supposed to convert images created within the AutoCAD©-Plugin PhoToPlan©. The user has to specify the locations of the original image and where to save the newly created GeoTiff. The plugin checks for the presence of the accompanying ppb-file and automatically determines if the image stems from a planum or a profile. In the latter case, the X- and Y-values are ignored and the origin of the GeoTIFF is set to \"0/Z-value\". Finally, the plugin opens the new file in QGIS. The user then has to choose the correct projection, as this cannot be determined from the ppb-file.\n"
"\n"
"Designed by Nils Müller-Scheeßel in collaboration with Knut Rassmann for \n"
"the Roman-Germanic Commission of the German Archaeological Institute\n"
"www.dainst.de\n"
"nils.mueller-scheessel@dainst.de", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("PPConverter", "About", None))

