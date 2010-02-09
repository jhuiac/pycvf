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
    
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import time
import sys


## values are return as dictionnary
## properrt editor takes as input a "type decl/form"
## that is dictionnary of fields (like ) 
## connections with django types may be thought too
## it may be automatically constructed from the type of variable in python

class QtNearestNeighborsViewer(QtGui.QTableWidget):
        def __init__(self, ed, nd, n,  *args):
            QtGui.QTableWidget.__init__(self , *args)
            self.setColumnCount(2*nd+1)
            #self.setColumnWidth(2*n+1,self.geometry().width()-30)
            self.setRowCount(n)
            self.setHorizontalHeaderLabels( reduce(lambda x,y:x+y, [ ["R"+str(d),"D"+str(d)] for d in range(nd)],["Query"]))
            self.ed=ed
            self.nd=nd
            self.n=n
            self.wi=numpy.zeros((n,nd),dtype=object)
            self.wiq=numpy.zeros((n,),dtype=object)
            xiw=self.ed[1]['data_out']
            for i in range(n):            
              self.wiq[i]=xiw.get_widget(self) 
              self.setCellWidget( i,0, self.wiq[i])
              for j in range(nd):
                 self.wi[i,j]=xiw.get_widget(self) 
                 self.setCellWidget( i,2*j+1, self.wi[i,j])
            #self.push(iv)
        def push(self,r):
            #print "pushing ",len(r[1])
            xiw=self.ed[1]['data_out']            
            for i in range(self.n):
              xiw.set_widget_value(self.wiq[i],r[0][i])
              for j in range(self.nd):
                 #print i,j,r[1]
                 try:
                   it=QtGui.QTableWidgetItem()
                   it.setText(str(r[1][i][j][1]))
                   self.setItem( i,2*j+2,it)
                   w=self.wi[i,j]
                   xiw.set_widget_value(w,r[1][i][j][0])
                   if (w.minimumWidth()>self.columnWidth(2*j+1)):
                        self.setColumnWidth(2*j+1,w.minimumWidth())
                   if (w.minimumHeight()>self.rowHeight(i)):
                        self.setRowHeight(i,w.minimumHeight())                        
                 except Exception,e: 
                   print "unable to set widget j : reason ", e

class QtNearestNeighborsViewerDialog(QtGui.QDialog):
        def __init__(self,ed,nd,n, *args):
            QtGui.QDialog.__init__(self , *args)
            self.cw=self
            self.layout=QtGui.QVBoxLayout(self.cw)
	    self.layout.setContentsMargins(0,0,0,0)
            self.pwl=QtNearestNeighborsViewer(ed,nd,n,self.cw)
            self.layout.addWidget(self.pwl)
            self.pbok=QPushButton(self.cw)
            self.pbok.setText("Ok")
            self.connect(self.pbok,SIGNAL("clicked()"),self,SLOT("accept()"))
            self.layout.addWidget(self.pbok)
            self.pbcancel=QPushButton(self.cw)
            self.pbcancel.setText("Cancel")
            self.connect(self.pbcancel,SIGNAL("clicked()"),self,SLOT("reject()"))
            self.layout.addWidget(self.pbcancel)
            self.update()
        def push(self,x):
            self.pwl.push(x)
        def __del__(self):
            self.hide()




  