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
from pycvf.lib.ui.qt import qapp
from PyQt4 import QtCore
from PyQt4 import QtGui
import numpy
import random
    
class QtSelector(QtGui.QListWidget): 
        def __init__(self, l, *args):
            QtGui.QListWidget.__init__(self , *args)
            self.set_elements(l)
        def get_selection(self):
            return [ self.item(i).isSelected() for i in range(len(self.l)) ]
        def get_selected_elements(self):
            return reduce(lambda b,y:b+ (y[0 ] and [y[1]] or [])  , zip(self.get_selection(), self.l))
        def set_selection(self,l):
            assert(len(l)==len(self.l))
            for i in range(l):
               self.setSelected(i,l[i])
        def set_elements(self,l):
            self.l=l
            self.clear()
            for i in range(len(l)):
                self.insertItem(i,l[i])


class QtSelectorWin(QtGui.QDialog):
        def __init__(self, sz, *args):
            QtGui.QDialog.__init__(self , *args)
        #self.cw=QWidget()
            self.cw=self
            self.layout=QtGui.QVBoxLayout(self.cw)
            self.layout.setContentsMargins(0,0,0,0)
            self.pwl=QtSelector(sz,self.cw)
            self.layout.addWidget(self.pwl)
            self.pbok=QtGui.QPushButton(self.cw)
            self.pbok.setText("Ok")
            #self.pbok.actionEvent=self.accept 
            self.connect(self.pbok,QtCore.SIGNAL("clicked()"),self,QtCore.SLOT("accept()"))
            self.layout.addWidget(self.pbok)
            self.pbcancel=QtGui.QPushButton(self.cw)
            self.pbcancel.setText("Cancel")
            self.connect(self.pbcancel,QtCore.SIGNAL("clicked()"),self,QtCore.SLOT("reject()"))
            self.layout.addWidget(self.pbcancel)
            #self.setCentralWidget(self.cw)
            self.update()
            #self.show()
        def accept(self):
            QtGui.QDialog.accept(self)
        def __del__(self):
            self.hide()
        def get_selection(self):
            return self.pwl.get_selection()
        def get_selected_elements(self):
            return self.pwl.get_selected_elements()
        def set_selection(self,l):
            self.pwl.set_selection(l)
        def set_elements(self,l):
            self.pwl.set_elements(l)



import time

if __name__ == "__main__":
  pass
  