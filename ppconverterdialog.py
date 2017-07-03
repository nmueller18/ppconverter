# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PPConverterDialog
                                 A QGIS plugin
 Plugin to convert files created with PP
                             -------------------
        begin                : 2013-04-03
        copyright            : (C) 2013 by Nils Müller-Scheeßel
        email                : nils.mueller-scheessel@dainst.de
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

#from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from ui_ppconverter import Ui_PPConverter
# create the dialog for zoom to point


class PPConverterDialog(QDialog, Ui_PPConverter):
    def __init__(self):
        QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_PPConverter()
        self.setupUi(self)
        QObject.connect(self.outButton, SIGNAL("clicked()"), self.outFile)
        QObject.connect(self.inButton, SIGNAL("clicked()"), self.inFile)

    def outFile(self):
        self.outTiff.clear()
        fileDialog = QFileDialog()
        fileDialog.setConfirmOverwrite(False)
        dst_filepath = fileDialog.getSaveFileName(self, SaveGeoTIFF, '', "TIFF (*.tif)")
        outPath = QFileInfo(dst_filepath).absoluteFilePath()
        if outPath.right(4) != ".tif":
            outPath = outPath + ".tif"
        if not dst_filepath.isEmpty():
            self.outFile.clear()
            self.outFile.insert(outPath)
            
    def inFile(self):
        self.inTiff.clear()
        fileDialog = QFileDialog()
        src_filepath = fileDialog.getOpenFileName(None, LocateImage)