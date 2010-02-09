#!/usr/bin/env python
# -*- coding: utf-8 -*-
## ##########################################################################################################
## 
## This file is released under GNU Public License v3
## See LICENSE File at the top the pycvf tree.
##
## Author : Bertrand NOUVEL / CNRS (2009)
##
##
##
## Revision FILE: $Id$
##
## ###########################################################################################################
## copyright $Copyright$
## @version $Revision$
## @lastrevision $Date$
## @modifiedby $LastChangedBy$
## @lastmodified $LastChangedDate$
#############################################################################################################


# -*- coding: utf-8 -*-
import os
import sys
from PyQt4 import QtCore
from PyQt4 import QtGui

if not (os.environ.has_key("DISABLE_PYQT_CENTRAL_APP")):
  qapp = QtGui.QApplication(sys.argv)
  qapp.processEvents()
else:
  qapp=None