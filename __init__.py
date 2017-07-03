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
 This script initializes the plugin, making it known to QGIS.
"""


def name():
    return "PPConverter"


def description():
    return "Convert PhoToPlan-images to GeoTIFFs"


def version():
    return "Version 0.1"


def icon():
    return "icon.png"


def qgisMinimumVersion():
    return "1.8"

def author():
    return "Nils Müller-Scheeßel"

def email():
    return "nils.mueller-scheessel@dainst.de"

def classFactory(iface):
    # load PPConverter class from file PPConverter
    from ppconverter import PPConverter
    return PPConverter(iface)

def category():
  return "Raster"