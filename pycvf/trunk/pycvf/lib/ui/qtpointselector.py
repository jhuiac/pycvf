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

class PointWidget(QWidget):
    def __init__(self,parent,pos,color=(255,0,0,127),pointsz=10, selectedcolor=(0,255,0,127),*args):
        apply(QWidget.__init__,(self, parent,) + args)
        self.setMinimumHeight(pointsz)
        self.setMinimumWidth(pointsz)
        self.setMaximumHeight(pointsz)
        self.setMaximumWidth(pointsz)
        self.connections=[]
        self.color=color
        self.setGeometry(pos[0]-pointsz//2,  pos[1]-pointsz//2  ,pointsz,pointsz)
        self.selectedcolor=selectedcolor
        self.pointsz=pointsz
        self.isselected=False
    def set_selected(self,v):
	self.isselected=v
    def getpos(self):
	g=self.geometry()
        return (g.x()+self.width()//2, g.y()+self.height()//2)
    def paintEvent(self,ev):
        self.p = QPainter()
        self.p.begin(self)
        self.p.setBrush(QBrush(QColor(*(self.isselected and (self.selectedcolor) or (self.color)))))
        self.p.drawEllipse(0,0,self.pointsz,self.pointsz)
        self.p.end()


try:
    LazyDisplayQt__imgconvarray={
                      1:QtGui.QImage.Format_Indexed8,
                      3:QtGui.QImage.Format_RGB888,  
                      4:QtGui.QImage.Format_RGB32    
                      }                              
except:                                              
    LazyDisplayQt__imgconvarray={                    
                      1:QtGui.QImage.Format_Indexed8,
                      4:QtGui.QImage.Format_RGB32    
                      }                  


class QtPointSelector(QtGui.QWidget):
        imgconvarray=LazyDisplayQt__imgconvarray 
        def __init__(self, sz, *args):
            QtGui.QWidget.__init__(self , *args)
            self._i=numpy.zeros((sz[0],sz[1],4),dtype=numpy.uint8)
            self.i=QtGui.QImage(self._i.data,self._i.shape[1],self._i.shape[0],QtGui.QImage.Format_RGB32)
            self.lp=[]
            self.selectcolor=(0,0,255,127)
            self.pwl=[PointWidget(self,(random.randint(0,sz[1]),random.randint(0,sz[0]))) for x in range(5)]
            self.setMinimumHeight(sz[0])
            self.setMinimumWidth(sz[1])
            self.setMaximumHeight(sz[0])
            self.setMaximumWidth(sz[1])
            self.startpos=(0,0)
            self.endpos=(0,0)
            self.mode=0
            #self.show()
            #self.lp
        def __del__(self):
            self.hide()
        def paintEvent(self, ev):
	   if (self.i):
              self.p = QtGui.QPainter()
              self.p.begin(self)
              self.p.drawImage(QtCore.QRect(0,0,self.width(),self.height()),
                             self.i,
                             QtCore.QRect(0,0,self.i.width(),self.i.height()))
              self.p.end()
           QWidget.paintEvent(self,ev)
           self.p = QPainter()
           self.p.begin(self)
           self.p.setBrush(QBrush(QColor(*self.selectcolor)))
           mx,Mx=min(self.startpos[0],self.endpos[0]),max(self.startpos[0],self.endpos[0])
           my,My=min(self.startpos[1],self.endpos[1]),max(self.startpos[1],self.endpos[1])
           dx=Mx-mx
           dy=My-my
           self.p.drawRect(mx,my,dx,dy)
           self.p.end()
        def update_img(self,thearray):
            self._i=thearray.astype(numpy.uint8).copy('C')
            self.i=QtGui.QImage(self._i.data,self._i.shape[1],self._i.shape[0],self.imgconvarray[self._i.shape[2]])
            if (self._i.shape[2]==1):
                self.i.setColorTable(self.colortable)
            self.update()
        def mousePressEvent(self,ev):
          if ( ev.button()==Qt.LeftButton): 
            self.mode=0
          if ( ev.button()==Qt.MidButton): 
            self.mode=1
          if ( ev.button()==Qt.RightButton): 
            self.mode=2
          self.startpos=(ev.x(),ev.y())
        def mouseMoveEvent(self,ev):
          self.endpos=(ev.x(),ev.y())
          mx,Mx=min(self.startpos[0],self.endpos[0]),max(self.startpos[0],self.endpos[0])
          my,My=min(self.startpos[1],self.endpos[1]),max(self.startpos[1],self.endpos[1])	  
          if (self.mode==1):
	    for p in self.pwl:
              pos=p.getpos()
	      if (mx<=pos[0]<=Mx ) and(my<=pos[1]<=My ) :
	        p.set_selected(True)
	      else:
	        p.set_selected(False)
          else:
	      for p in self.pwl:
                pos=p.getpos()
	        if (mx<=pos[0]<=Mx ) and(my<=pos[1]<=My ) :
	          p.set_selected(self.mode==0)
       
          self.parent().repaint()
        def mouseReleaseEvent(self,ev):
          self.endpos=(0,0)
          self.startpos=(0,0)
          self.parent().repaint()
        def get_selection(self):
	  return [ p.isselected for p in self.pwl ]
        def get_selected_points(self):
	  return reduce(lambda b,y:b+ (y[0 ] and [y[1]] or [])  , zip(self.get_selection(), map(lambda p:p.getpos(),self.pwl)),[])
	def set_selection(self,l):
	  assert(len(l)==len(self.pwl))
	  for i in range(l):
	    self.pwl[i].set_selected(i)
	def set_points(self,l):
            self.pwl=[PointWidget(self,x) for x in l]


class QtPointSelectorWin(QtGui.QDialog):
        def __init__(self, sz, *args):
            QtGui.QDialog.__init__(self , *args)
	    #self.cw=QWidget()
            
            self.cw=self
            self.layout=QtGui.QVBoxLayout(self.cw)
	    self.layout.setContentsMargins(0,0,0,0)
            self.pwl=QtPointSelector(sz,self.cw)
            self.layout.addWidget(self.pwl)
            self.pbok=QPushButton(self.cw)
            self.pbok.setText("Ok")
            #self.pbok.actionEvent=self.accept 
            self.connect(self.pbok,SIGNAL("clicked()"),self,SLOT("accept()"))
            self.layout.addWidget(self.pbok)
            self.pbcancel=QPushButton(self.cw)
            self.pbcancel.setText("Cancel")
            self.connect(self.pbcancel,SIGNAL("clicked()"),self,SLOT("reject()"))
            self.layout.addWidget(self.pbcancel)
            #self.setCentralWidget(self.cw)
            self.update()
            #self.show()
        def accept(self):
            #print "ok"
            #print  self.pwl.get_selected_points()
            QDialog.accept(self)
        def __del__(self):
            self.hide()
        def update_img(self,img):
	    self.pwl.update_img(img)
            qapp.processEvents()
        def get_selection(self):
	  return self.pwl.get_selection()
        def get_selected_points(self):
	  return self.pwl.get_selected_points()
	def set_selection(self,l):
	  self.pwl.set_selection(l)
	def set_points(self,l):
	  self.pwl.set_points(l)



import time

if __name__ == "__main__":
  import sys,numpy,scipy
#  import pysift
  from jfli.readers.directoryreader import ImageDirectoryReader
  #from pycvf.lib.graphics.randompatches import *
  from pycvf.lib.graphics.rescale import Rescaler2d
  from jfli.dimred.nmf3 import *
  from jfli.dimred.PCA import *
  from jfli.dimred.ica import *
  from pycvf.lib.stats.models import *
  from pycvf.lib.stats.incremental import *
  from itertools import imap
  #import pycudaSift1024 as pcs
  #import pysift.sift as sift
  from pycvf.lib.graphics.kp_sift import sift
  
  qmw=QMainWindow()
  rsc=Rescaler2d((256,256,'R'))
  
  def grayscale(i):
      if (i.ndim==3):
          return i.mean(axis=2)
      elif(i.ndim==2):
          return i
      else:
          assert(False)
  
  basedir="/home/tranx/databases/101ObjectCategories/PNGImages/saxophone/"
  
  dr=imap(lambda i : (rsc.process(grayscale(i[0])),i[1]),
           ImageDirectoryReader(basedir).iterimages_with_filenames
          )
  
  print "computing all sifts"
  xallsifts=[]
 # for xl in dr:
 #   sys.stdout.write(".")
 #   sys.stdout.flush()
 #   print xl[1] ,xl[0].shape 
 #   xl=xl[0]
 #   #print xl
 #   #ll=xl.reshape(xl.shape[1]*xl.shape[0]).astype(numpy.int)#.tolist()
 #   siftr=sift(  xl.astype(uint8).copy('C')  )
 #   xallsifts.extend(siftr)
  
  #print
  #print "computing dimension reduction"
  #dr1=NMFdimred(numpy.array(xallsifts),16)
  
  #del xallsifts
  #dmr=DimReducedModel(dr1,EmModel(16,100))
  #dmr.train(alltrainingset)
  
  dr=imap(lambda i : rsc.process(i.mean(axis=2)),
           ImageDirectoryReader("/home/tranx/databases/101ObjectCategories/PNGImages/saxophone/").iterimages
          )
  
  print "learning model"
  for xl in dr:
#    xl=xl[0]
    print xl.shape
    x=QtPointSelectorWin((xl.shape[1],xl.shape[0]),qmw) 
    #r=pcs.cudaSift(xl.astype(numpy.float32),octave=3)
    #points=[ ( x.get_xpos(), x.get_ypos() ) for x in r.get_h_data() ]
    print (xl.shape[1],xl.shape[0])
    #ll=xl.reshape(xl.shape[1]*xl.shape[0]).astype(numpy.uint8).tolist()
    siftr=sift(  xl.astype(uint8).copy('C'))
    points=map(lambda x:(x[0],x[1]),siftr)
    l=xl.reshape(xl.shape[0],xl.shape[1],1).repeat(3,axis=2).astype(numpy.uint8)
    x.update_img(l)
    x.set_points(points)
    if (x.exec_()):  
      print numpy.array(siftr)[x.get_selection(),:]
    else:
        break;


  