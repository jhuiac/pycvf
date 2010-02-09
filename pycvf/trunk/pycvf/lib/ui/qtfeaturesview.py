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
from pycvf.core.errors import *
from pycvf.lib.ui.qt import qapp
from PyQt4 import QtCore
from PyQt4 import QtGui


import numpy
import random
    
from PyQt4.QtCore import *
from PyQt4.QtGui import *

try:
  from PyKDE4.kdeui import *
except:
  pycvf_warning("PyKDE4 is required for some applications")
  
import time
import sys


## values are return as dictionnary
## properrt editor takes as input a "type decl/form"
## that is dictionnary of fields (like ) 
## connections with django types may be thought too
## it may be automatically constructed from the type of variable in python


class QWidgetFileComboPush(QtGui.QWidget):
        def __init__(self,d, *args):
            QtGui.QWidget.__init__(self , *args)
            self.layout=QtGui.QHBoxLayout(self)
	    self.layout.setContentsMargins(0,0,0,0)
            self.tb=QLineEdit(self)
            self.layout.addWidget(self.tb)
            self.pb=QPushButton(self)
            self.pb.setText("...")
            self.pb.setMaximumWidth(32)
            self.connect(self.pb,SIGNAL("clicked()"),self.usedialog)
            self.layout.addWidget(self.pb)
        def usedialog(self):
            self.tb.setText(QFileDialog.getOpenFileName())
        def setText(self,s):
            self.tb.setText(s)
        def text(self):
            self.tb.text()


class IntSpinEditor():
  def __init__(self,value,minv=0,maxv=256,step=1):
    self.default=value
    self.minv=minv
    self.maxv=maxv
    self.step=step
    self.w=None
    self.value=value
  def create_widget(self,br):
     self.w=QSpinBox(br)
     self.w.setRange(0,100)
     self.set_value()
     return self.w
  def set_value(self,i=None):
      if (i):
        self.w.setValue(i)
      else:
        self.w.setValue(self.value)
  def get_value(self):
     return self.w.value()

class IntDialEditor():
  def __init__(self,value,minv=0,maxv=256,step=1):
    self.default=value
    self.minv=minv
    self.maxv=maxv
    self.step=step
    self.w=None
    self.value=value
  def create_widget(self,br):
     self.w=QDial(br)
     self.w.setRange(0,100)
     self.set_value()
     return self.w
  def set_value(self,i=None):
      if (i):
        self.w.setValue(i)
      else:
        self.w.setValue(self.value)
  def get_value(self):
     return self.w.getValue()


class StringFontEditor():
  def __init__(self,value,minv=0,maxv=256,step=1):
    self.default=value
    self.minv=minv
    self.maxv=maxv
    self.step=step
    self.w=None
    self.value=value
  def create_widget(self,br):
     self.w=QFontComboBox(br)
     #self.w.setRange(0,100)
     #self.set_value(self.value)
     return self.w
  def set_value(self,i=None):
      if not i:
        i=self.value
      #if (i):
      #  self.w.setCurrentFont(i)
      #else:
      #  self.w.setCurrentFont(self.value)
      pass
  def get_value(self):
     return self.w.currentFont()
     #return self.w.getValue()


class StringFileEditor():
  def __init__(self,value,minv=0,maxv=256,step=1):
    self.default=value
    self.minv=minv
    self.maxv=maxv
    self.step=step
    self.w=None
    self.value=value
  def create_widget(self,br):
     self.w=QWidgetFileComboPush(br)
     #self.w.setRange(0,100)
     #self.set_value(self.value)
     return self.w
  def set_value(self,i=None):
      if not i:
        i=self.value
      self.w.setText(i)
      #  self.w.setCurrentFont(i)
      #else:
      #  self.w.setCurrentFont(self.value)
      pass
  def get_value(self):
     return self.w.text()
     



class ColorEditor():
  def __init__(self,value,minv=0,maxv=256,step=1):
    self.default=value
    self.minv=minv
    self.maxv=maxv
    self.step=step
    self.w=None
    self.value=value
  def set_value(self,i=None):
      if not i:
        i=self.value
      self.w.setColor((type(i)==tuple) and QColor(*i) or i)
      pass
  def create_widget(self,br):
     self.w=KColorCombo(br)
     return self.w
  def get_value(self):
     return self.w.color()

class BooleanEditor():
  def __init__(self,value,minv=0,maxv=256,step=1):
    self.default=value
    self.minv=minv
    self.maxv=maxv
    self.step=step
    self.w=None
    self.value=value
  def create_widget(self,br):
     self.w=QCheckBox(br)
     self.w.connect(self.w,SIGNAL("trigger()"),self.w,SLOT("toggle()"))
     return self.w
  def set_value(self,i=None):
      if not i:
        i=self.value
      return self.w.setCheckState(i and  Qt.Checked or Qt.Unchecked)
  def get_value(self):
     return self.w.checkState()


class MatrixEditor():
  def __init__(self,value):
    self.default=value
    self.w=None
    self.dtype=None
    self.value=value
  def create_widget(self,br):
     self.w=QTableWidget(br)
     return self.w
  def set_value(self,i=None):
      if not i:
        i=self.value
      n,m=i.shape
      self.dtype=i.dtype
      self.w.setColumnCount(m)
      self.w.setRowCount(n)
      for ni in range(n):
	for mi in range(m):
          self.w.setItem(mi ,ni, QTableWidgetItem(str(i[ni,mi]),0))
  def get_value(self):
      m=self.w.columnCount()
      n=self.w.rowCount()
      r=numpy.ndarray(shape=(n,m),dtype=self.dtype)
      for ni in range(n):
	for mi in range(m):
          r[ni,mi] =float(self.w.item(mi ,ni).text())

     



# 
# nom, variable, editeur

class PropEditMapper:
  ta={ 
    int: lambda x:IntSpinEditor,
    float: lambda x:IntSpinEditor,
    bool : lambda x:BooleanEditor,
    tuple : lambda x: (len(x)==3) and ColorEditor or None,
    str : lambda x: StringFileEditor   ,
    numpy.matrix : lambda x: MatrixEditor
  }
  
  @staticmethod 
  def from_dict(d):
    return map ( lambda x: (x[0],x[1],PropEditMapper.ta[type(x[1])]), d.items() )


class QtFeaturesViewer(QtGui.QTableWidget):
        def __init__(self, d,  *args):
            QtGui.QTableWidget.__init__(self , *args)
            self.keys=map(lambda x:x[0][0],d)
            self.setColumnCount(1)
            self.setColumnWidth(1,self.geometry().width()-30)
            self.setRowCount(len(d))
            self.setVerticalHeaderLabels(self.keys)
            self.ed=d
            self.wi=[None]*len(d)
            for i in range(len(d)):
               xiw=self.ed[i][1]
               print "xiw",xiw
               self.wi[i]=xiw.get_widget(self) 
               self.setCellWidget( i,0, self.wi[i])
               self.setRowHeight(i,300)
            #self.push(iv)
        def push(self,v,*args,**kwargs):
            for i in range(len(self.ed)):
                self.ed[i][1].set_widget_value(self.wi[i],v[i],*args,**kwargs)
        def resizeEvent(self,ev):
             self.setColumnWidth(0,self.geometry().width()-70) #self.horizontalHeader().width())
             return QtGui.QTableWidget.resizeEvent(self , ev)

class QtFeaturesViewerDialog(QtGui.QDialog):
        def __init__(self,d, *args):
            QtGui.QDialog.__init__(self , *args)
            self.cw=self
            self.layout=QtGui.QVBoxLayout(self.cw)
	    self.layout.setContentsMargins(0,0,0,0)
            self.pwl=QtFeaturesViewer(d,self.cw)
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
        def push(self,x,*args,**kwargs):
            self.pwl.push(x,*args,**kwargs)
        def __del__(self):
            self.hide()


if __name__ == "__main__":
  v=3
  w=6
  z=True
  d={"value1":v,  "value2":w , "value3": z, "value4":(10,20,30), "test":"arial", 'm':numpy.matrix([[2,3],[4,3]])}
  print d.keys(), 2
  qmw=QtGui.QMainWindow()
  myColor=QtGui.QColor (0,255,0);
  x=QtFeaturesViewerDialog(d,qmw)
  