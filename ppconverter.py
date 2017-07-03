# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PPConverter
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
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
#from ppconverterdialog import PPConverterDialog
import os, sys

from ui_ppconverter import Ui_PPConverter
# create the dialog for zoom to point

class PPConverter:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = QFileInfo(QgsApplication.qgisUserDbFilePath()).path() + "/python/plugins/ppconverter"
         
        # initialize locale
        localePath = ""
        locale = QSettings().value("locale/userLocale", "")
        
        if QFileInfo(self.plugin_dir).exists():
            localePath = self.plugin_dir + "/i18n/ppconverter_" + locale + ".qm"

        if QFileInfo(localePath).exists():
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = PPConverterDialog()

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/ppconverter/icon.png"),
            u"PPConverter", self.iface.mainWindow())
        # connect the action to the run method
        QObject.connect(self.action, SIGNAL("triggered()"), self.run)

        # check if Raster menu available
        if hasattr(self.iface, "addPluginToRasterMenu"):
           # Raster menu and toolbar available
           self.iface.addRasterToolBarIcon(self.action)
           self.iface.addPluginToRasterMenu(u"&PPConverter", self.action)
        else:
           # there is no Raster menu, place plugin under Plugins menu as usual
           self.iface.addToolBarIcon(self.action)
           self.iface.addPluginToMenu(u"&PPConverter", self.action)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&PPConverter", self.action)
        self.iface.removeToolBarIcon(self.action)

    # run method that performs all the real work
    def run(self):
        # show the dialog
        #self.dlg.exec_()
        self.dlg.show()

class PPConverterDialog(QDialog, Ui_PPConverter):
    def __init__(self):
		QDialog.__init__(self)

		# Set up the user interface from Designer.
		self.ui = Ui_PPConverter()
		self.setupUi(self)
		
		QObject.connect(self.outButton, SIGNAL("clicked()"), self.outFile)
		QObject.connect(self.inButton, SIGNAL("clicked()"), self.inFile)


    #set source file
    def inFile(self, src_filepath = None, ppb_file = None):
        src_filepath = ""
        self.inTiff.clear()
        # localize plugin
        locale = QSettings().value("locale/userLocale", "")
        if locale == "de_DE":
              LocateImage="Bildauswahl"
              NoPPBExtension = unicode("Zu diesem Bild scheint keine Datei mit ppb-Erweiterung zu gehören oder diese wurde bewegt. Bitte nochmals versuchen.", encoding='utf-8')
        else:
              LocateImage="Locate image"
              NoPPBExtension = "Sorry, this image does not seem to have a file with ppb-extension or the respective file has been moved. Please try again."

        ppb_filepath = ""
        fileDialog = QFileDialog()
        src_filepath = fileDialog.getOpenFileName(None, LocateImage)
        if not src_filepath == "":
			(src_path, src_name) = os.path.split(unicode(src_filepath))
			(src_shortname, src_extension) = os.path.splitext(src_name)
			ppb_filename = "_".join([src_shortname,src_extension[1:]])
			ppb_fileextension = ".".join([ppb_filename,"ppb"])
			ppb_filepath = os.path.join(src_path,ppb_fileextension)
	
			#Try to open ppb-file
			try:
			   ppb_file=open(ppb_filepath)
			   ppb_file.close()
			except IOError:
			   QMessageBox.information(None, "DEBUG:",NoPPBExtension)
			   return	
        
        inPath = QFileInfo(src_filepath).absoluteFilePath()
        if not src_filepath == "":
			self.inTiff.clear()
			self.inTiff.insert(inPath)

            
    #set file destination
    def outFile(self, dst_filepath = None):
        self.outTiff.clear()
        dst_filepath = ""
        
        # localize plugin
        locale = QSettings().value("locale/userLocale", "")
        if locale == "de_DE":
            SaveGeoTIFF = "Sichern des GeoTIFF"
        else:
            SaveGeoTIFF = "Save GeoTIFF"
            
        fileDialog = QFileDialog()
        fileDialog.setConfirmOverwrite(False)
        dst_filepath = fileDialog.getSaveFileName(self, SaveGeoTIFF, '', "TIFF (*.tif)")
        outPath = QFileInfo(dst_filepath).absoluteFilePath()
        if not dst_filepath == "":
			self.outTiff.clear()
			self.outTiff.insert(outPath)

    
    def accept(self):
		from os.path import expanduser
		home = expanduser("~")
		# localize plugin
		locale = QSettings().value("locale/userLocale", "")
		if locale == "de_DE":
			specifyFiles = "Ein- und Ausgabedateien fehlen noch!"
			specifyInput = "Eingabedatei fehlt noch!"
			specifyOutput = "Ausgabedatei fehlt noch!"
			NoPPBExtension = unicode("Zu dem Eingabebild scheint keine Datei mit ppb-Erweiterung zu gehören oder diese wurde bewegt. Bitte nochmals versuchen.", encoding='utf-8')
			ErrorMessage = "Irgendetwas ist schief gelaufen. Vermutlich gibt es den angegebenen Speicherort (noch) nicht. Bitte nochmals versuchen."
		else:
			specifyFiles = "You must specify in- and output files!"
			specifyInput = "You must specify an input-file!"
			specifyOutput = "You must specify an output-file!"
			NoPPBExtension = "Sorry, the input image does not seem to have a file with ppb-extension or the respective file has been moved. Please try again."
			ErrorMessage = "Sorry, something went wrong. Likely, the specified location does not (yet) exists. Please try again."

		# Handling if user leaves fields blank
		if self.inTiff.text() == "" and self.outTiff.text() == "":
			QMessageBox.information(self, "PPConverter",specifyFiles)
		elif self.inTiff.text() == "":
			QMessageBox.information(None, "PPConverter",specifyInput)
		elif self.outTiff.text() == "":
			QMessageBox.information(None, "PPConverter",specifyOutput)
			   
		else:
			import re
			dst_filepath = self.outTiff.text()
			src_filepath = self.inTiff.text()
			if dst_filepath[4:] != ".tif":
				dst_file = unicode(dst_filepath + ".tif")
				dst_filepath = os.path.join(home, dst_file)
			(src_path, src_name) = os.path.split(unicode(src_filepath))
			(src_shortname, src_extension) = os.path.splitext(src_name)
			ppb_filename = "_".join([src_shortname,src_extension[1:]])
			ppb_fileextension = ".".join([ppb_filename,"ppb"])
			ppb_filepath = os.path.join(src_path,ppb_fileextension)
			try:
				ppb_file=open(ppb_filepath)
			except IOError:
			   QMessageBox.information(None, "DEBUG:",NoPPBExtension)
			   return

			#setting the regular expression parser
			image_info=re.compile(r"BildZeilen,(\d+)},{BildSpalten,(\d+)},{BKS,{{{Ursprung,{([+/-]?\d+\.\d+[eE][+\-]?\d+|[+/-]?\d+\.\d+|[+/-]?\d+),([+/-]?\d+\.\d+[eE][+\-]?\d+|[+/-]?\d+\.\d+|[+/-]?\d+),([+/-]?\d+\.\d+[eE][+\-]?\d+|[+/-]?\d+\.\d+|[+/-]?\d+)}}},{{xAchse,{([+/-]?\d+\.\d+[eE][+\-]?\d+|[+/-]?\d+\.\d+|[+/-]?\d+),([+/-]?\d+\.\d+[eE][+\-]?\d+|[+/-]?\d+\.\d+|[+/-]?\d+),([+/-]?\d+\.\d+[eE][+\-]?\d+|[+/-]?\d+\.\d+|[+/-]?\d+)}}},{{yAchse,{([+/-]?\d+\.\d+[eE][+\-]?\d+|[+/-]?\d+\.\d+|[+/-]?\d+),([+/-]?\d+\.\d+[eE][+\-]?\d+|[+/-]?\d+\.\d+|[+/-]?\d+),([+/-]?\d+\.\d+[eE][+\-]?\d+|[+/-]?\d+\.\d+|[+/-]?\d+)}}}}},{BildPos,{{{Ursprung,{([+/-]?\d+\.\d+[eE][+\-]?\d+|[+/-]?\d+\.\d+|[+/-]?\d+),([+/-]?\d+\.\d+[eE][+\-]?\d+|[+/-]?\d+\.\d+|[+/-]?\d+),([+/-]?\d+\.\d+[eE][+\-]?\d+|[+/-]?\d+\.\d+|[+/-]?\d+)}}},{{xAchse,{([+/-]?\d+\.\d+[eE][+\-]?\d+|[+/-]?\d+\.\d+|[+/-]?\d+),([+/-]?\d+\.\d+[eE][+\-]?\d+|[+/-]?\d+\.\d+|[+/-]?\d+),([+/-]?\d+\.\d+[eE][+\-]?\d+|[+/-]?\d+\.\d+|[+/-]?\d+)}}},{{yAchse,{([+/-]?\d+\.\d+[eE][+\-]?\d+|[+/-]?\d+\.\d+|[+/-]?\d+),([+/-]?\d+\.\d+[eE][+\-]?\d+|[+/-]?\d+\.\d+|[+/-]?\d+),([+/-]?\d+\.\d+[eE][+\-]?\d+|[+/-]?\d+\.\d+|[+/-]?\d+)")
			image_info_result=image_info.search(ppb_file.read()).groups()
			
			#define geoinformation
			(BildZeilen,BildSpalten,BKSx,BKSy,BKSz,xAchse_x,xAchse_y,xAchse_z,yAchse_x,yAchse_y,yAchse_z,BildPos_x,BildPos_y,BildPos_z,xAchseParam_x,xAchseParam_y,xAchseParam_z,yAchseParam_x,yAchseParam_y,yAchseParam_z)=image_info_result

			#option for profiles or plana
			if float(BKSx)!=0 or float(BKSy)!=0 or float(BKSz)!=0:
			   n_s_resolution=float(yAchseParam_z)/float(BildSpalten)*(-1)
			   w_e_resolution=n_s_resolution*(-1)
			   top_left_x=0
			   top_left_y=float(BildPos_z)+float(yAchseParam_z)
			else:
			   n_s_resolution=float(yAchseParam_y)/float(BildSpalten)*(-1)
			   w_e_resolution=float(xAchseParam_x)/float(BildZeilen)
			   top_left_x=float(BildPos_x)
			   top_left_y=float(BildPos_y)+float(yAchseParam_y)

			# code snippets by Andre Hauptfleisch: http://adventuresindevelopment.blogspot.de/2008/12/python-gdal-adding-geotiff-meta-data.html   
			from osgeo import gdal
			#Open the source file
			src_ds=gdal.Open(unicode(src_filepath))

			#Open output format driver
			format = "GTiff"
			driver = gdal.GetDriverByName( format )

			#Output to new format
			dst_ds = driver.CreateCopy(unicode(dst_filepath), src_ds, 0 )

			try:
				#Apply Geotransformation: top left x, w-e pixel resolution, rotation, top left y, rotation, n-s pixel resolution
				dst_ds.SetGeoTransform([top_left_x,w_e_resolution,0,top_left_y,0,n_s_resolution])

				#Properly close the datasets to flush to disk
				src_ds = None
				dst_ds = None
				self.inTiff.clear()
				self.outTiff.clear()
				super(PPConverterDialog, self).accept()

				dst_Info = QFileInfo(unicode(dst_filepath))
				baseName=dst_Info.baseName()
				rlayer=QgsRasterLayer(unicode(dst_filepath),baseName)
				src_filepath = ""
				dst_filepath = ""
				QgsMapLayerRegistry.instance().addMapLayer(rlayer)
			except:
			   QMessageBox.information(None, "DEBUG:",ErrorMessage)
			   return