# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ppconverter
                                 A QGIS plugin
 Plugin to convert files created with PP
                              -------------------
        begin                : 2019-06-03
        copyright            : (C) 2013 by Nils Müller-Scheeßel
        email                : nmueller-scheessel@gmx.net
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

from PyQt5 import uic
from PyQt5 import QtWidgets
from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, QFileInfo, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QLineEdit,QApplication, QWidget, QInputDialog, QFileDialog, QMessageBox
from qgis._core import QgsRasterLayer, QgsProject

# Initialize Qt resources from file resources.py
from .resources import *
from builtins import str
from builtins import object

# Import the code for the dialog
# from .ppconverter_dialog import ppconverterDialog
import os.path
import os, sys


# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui_ppconverter.ui'))

class ppconverter:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'ppconverter_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&PPConverter')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('ppconverter', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToRasterMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/ppconverter/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'PPConverter'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginRasterMenu(
                self.tr(u'&PPConverter'),
                action)
            self.iface.removeToolBarIcon(action)


    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = ppconverterDialog()

        # show the dialog
        self.dlg.show()

class ppconverterDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(ppconverterDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        # self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.outButton.clicked.connect(self.outFile)
        self.inButton.clicked.connect(self.inFile)


    #set source file
    def inFile(self, src_filepath = None, ppb_file = None):
        src_filepath = ""
        self.inTiff.clear()
        # localize plugin
        locale = QSettings().value("locale/userLocale", "")
        if locale == "de_DE":
              LocateImage="Bildauswahl"
              NoPPBExtension = unicode("Zu diesem Bild scheint keine Datei mit ppb-Erweiterung zu gehören oder diese wurde bewegt. Bitte nochmals versuchen.")
        else:
              LocateImage="Locate image"
              NoPPBExtension = "Sorry, this image does not seem to have a file with ppb-extension or the respective file has been moved. Please try again."
        ppb_filepath = ""
        fileDialog = QtWidgets.QFileDialog()
        src_filepath, _ = fileDialog.getOpenFileName(None, LocateImage)
        if not src_filepath == "":
            (src_path, src_name) = os.path.split(str(src_filepath))
            (src_shortname, src_extension) = os.path.splitext(src_name)
            ppb_filename = "_".join([src_shortname,src_extension[1:]])
            ppb_fileextension = ".".join([ppb_filename,"ppb"])
            ppb_filepath = os.path.join(src_path,ppb_fileextension)
            
            #Try to open ppb-file
            try:
               ppb_file=open(ppb_filepath)
               ppb_file.close()
            except IOError:
               QtWidgets.QMessageBox.information(None, "DEBUG:",NoPPBExtension)
               return    
        
        inPath = QFileInfo(src_filepath).absoluteFilePath()
        if not src_filepath == "":
            self.inTiff.clear()
            self.inTiff.setText(str(inPath))

            
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
            
        fileDialog = QtWidgets.QFileDialog()
        #fileDialog.setConfirmOverwrite(False)
        dst_filepath, _ = fileDialog.getSaveFileName(self, SaveGeoTIFF, '', "TIFF (*.tif)")
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
            NoPPBExtension = unicode("Zu dem Eingabebild scheint keine Datei mit ppb-Erweiterung zu gehören oder diese wurde bewegt. Bitte nochmals versuchen.")
            ErrorMessage = "Irgendetwas ist schief gelaufen. Vermutlich gibt es den angegebenen Speicherort (noch) nicht. Bitte nochmals versuchen."
        else:
            specifyFiles = "You must specify in- and output files!"
            specifyInput = "You must specify an input-file!"
            specifyOutput = "You must specify an output-file!"
            NoPPBExtension = "Sorry, the input image does not seem to have a file with ppb-extension or the respective file has been moved. Please try again."
            ErrorMessage = "Sorry, something went wrong. Likely, the specified location does not (yet) exists. Please try again."

        # Handling if user leaves fields blank
        if self.inTiff.text() == "" and self.outTiff.text() == "":
            QtWidgets.QMessageBox.information(self, "PPConverter",specifyFiles)
        elif self.inTiff.text() == "":
            QtWidgets.QMessageBox.information(None, "PPConverter",specifyInput)
        elif self.outTiff.text() == "":
            QtWidgets.QMessageBox.information(None, "PPConverter",specifyOutput)
               
        else:
            import re
            dst_filepath = self.outTiff.text()
            src_filepath = self.inTiff.text()
            if dst_filepath[4:] != ".tif":
                dst_file = str(dst_filepath + ".tif")
                dst_filepath = os.path.join(home, dst_file)
            (src_path, src_name) = os.path.split(str(src_filepath))
            (src_shortname, src_extension) = os.path.splitext(src_name)
            ppb_filename = "_".join([src_shortname,src_extension[1:]])
            ppb_fileextension = ".".join([ppb_filename,"ppb"])
            ppb_filepath = os.path.join(src_path,ppb_fileextension)
            try:
                ppb_file=open(ppb_filepath)
            except IOError:
               QtWidgets.QMessageBox.information(None, "DEBUG:",NoPPBExtension)
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
            src_ds=gdal.Open(str(src_filepath))

            #Open output format driver
            format = "GTiff"
            driver = gdal.GetDriverByName( format )

            #Output to new format
            dst_ds = driver.CreateCopy(str(dst_filepath), src_ds, 0 )

            try:
                #Apply Geotransformation: top left x, w-e pixel resolution, rotation, top left y, rotation, n-s pixel resolution
                dst_ds.SetGeoTransform([top_left_x,w_e_resolution,0,top_left_y,0,n_s_resolution])

                #Properly close the datasets to flush to disk
                src_ds = None
                dst_ds = None
                ppb_file.close()
                self.inTiff.clear()
                self.outTiff.clear()
                super(ppconverterDialog, self).accept()
                #self.dlg.close()

                dst_Info = QFileInfo(str(dst_filepath))
                baseName=dst_Info.baseName()
                rlayer=QgsRasterLayer(str(dst_filepath),baseName)
                src_filepath = ""
                dst_filepath = ""
                QgsProject.instance().addMapLayer(rlayer)
            except:
               QMessageBox.information(None, "DEBUG:",ErrorMessage)
               return