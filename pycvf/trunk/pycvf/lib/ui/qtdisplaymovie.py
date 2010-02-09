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
from pylab import cm

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

#al=numpy.dstack([  scipy.lena().astype(numpy.uint16).reshape(512,512,1).repeat(3,axis=2),  numpy.ones((512,512),dtype=numpy.uint8)*255])
#l.f(al)
class QtDisplayMovie(QtGui.QWidget):
        fps=29.7
        imgconvarray=LazyDisplayQt__imgconvarray
        def __init__(self,parent,subimages=5, aspectratio=-1, *args):
            QtGui.QWidget.__init__(self,parent, *args)
            self.subimages=subimages
            self._i=numpy.zeros((90,120,4),dtype=numpy.uint8)
            self.t=None
            if (self._i.ndim==2):
              self._i=self._i.reshape(self._i.shape+(1,)).repeat(3,axis=2)
            self.i=QtGui.QImage(self._i.data,self._i.shape[1],self._i.shape[0],self.imgconvarray[self._i.shape[2]])
            if (self.subimages): 
               self._si=[None]* self.subimages
               self.si=[None]* self.subimages
               for sii in range(self.subimages):
                 self._si[sii]=numpy.zeros((90,120,4),dtype=numpy.uint8)
                 self.si[sii]=QtGui.QImage(self._si[sii].data,self._si[sii].shape[1],self._si[sii].shape[0],self.imgconvarray[self._si[sii].shape[2]])
            self.colortable=[ (numpy.array(cm.jet(x)[0:3])*256.).astype(numpy.uint8) for x in range(0,256) ]
            self.setMinimumHeight(self._i.shape[0])
            self.setMinimumWidth(self._i.shape[1])
            self.aspectratio=aspectratio
        def set_colormap(self,cma):
            self.colortable=cma
        def push(self,reader):
            self.reader=reader.copy()
            self.reader.set_observer(self.f)
            self.t=QtCore.QTimer()
            self.t.setInterval(int(1000./self.fps))
            self.t.setSingleShot(False)
            self.t.start()
            self.connect(self.t,QtCore.SIGNAL("timeout()"),self.ontimer)
            #print "timer set"
            try:
              if (self.subimages): 
               cf=0#self.reader.get_current_frame_no()
               ls=len(self.reader)
               for sii in range(self.subimages):                
                 thearray=self.reader[sii*ls/self.subimages]
                 self._si[sii]=thearray.astype(numpy.uint8).copy('C')
                 self.si[sii]=QtGui.QImage(self._si[sii].data,self._si[sii].shape[1],self._si[sii].shape[0],self.imgconvarray[self._si[sii].shape[2]])
                 if (self._si[sii].shape[2]==1):
                    self.si[sii].setColorTable(self.colortable)
               self.reader.seek_to(cf)
            except:
              pycvf_warning("seek is probably not supported : no subimages") 
            #self.update()
        def ontimer(self):
            try:
                #sys.stderr.write("[*")
                self.reader.step()
                #sys.stderr.write("]")
            except KeyboardInterrupt:
                raise
            except Exception,e:
                #sys.stderr.write("~")
                print "Exception in qtdisplaymovie",e
                self.reader.rewind()
                self.reader.step()
        def f(self,thearray):
            #print "f"
            self._i=thearray.astype(numpy.uint8).copy('C')
            if (self._i.ndim==2):
              self._i=self._i.reshape(self._i.shape+(1,)).repeat(3,axis=2)
            self.i=QtGui.QImage(self._i.data,self._i.shape[1],self._i.shape[0],self.imgconvarray[self._i.shape[2]])
            if (self._i.shape[2]==1):
                self.i.setColorTable(self.colortable)
            self.update()
            #print "/f"
        def paintEvent(self, ev):
            #print "p", self._i.shape
            rdiv=0.66666
            self.p = QtGui.QPainter()
            self.p.begin(self)
            if (self.aspectratio<0):
               aspectratio=(self.i.width()/self.i.height())*-self.aspectratio
            else:
               aspectratio=self.aspectration   
            w,h=self.width(),self.height()
            if (self.subimages): 
               w*=rdiv
               h*=rdiv
            if (h*self.aspectratio>w):
               h=(w/self.aspectratio)
            else:
               w=(h*self.aspectratio)
            self.p.drawImage(QtCore.QRect(0,0,w,h),
                             self.i,
                             QtCore.QRect(0,0,self.i.width(),self.i.height()))
            if (self.subimages): 
               dw=self.width()/self.subimages
               for sii in range(self.subimages):
                 self.p.drawImage(QtCore.QRect(sii*dw,h+rdiv,dw,h*(1-rdiv)),
                             self.si[sii],
                             QtCore.QRect(0,0,self.si[sii].width(),self.si[sii].height()))
            self.p.end()
            #print "/p"


class QtDisplayMovieDialog(QtGui.QDialog):
        def __init__(self,*args):
            QtGui.QDialog.__init__(self , *args)
            self.cw=self
            self.layout=QtGui.QVBoxLayout(self.cw)
	    self.layout.setContentsMargins(0,0,0,0)
            self.pwl=QtDisplayMovie(self.cw)
            self.layout.addWidget(self.pwl)
            self.pbok=QtGui.QPushButton(self.cw)
            self.pbok.setText("Ok")
            self.connect(self.pbok,QtCore.SIGNAL("clicked()"),self,QtCore.SLOT("accept()"))
            self.layout.addWidget(self.pbok)
            self.pbcancel=QtGui.QPushButton(self.cw)
            self.pbcancel.setText("Cancel")
            self.connect(self.pbcancel,QtCore.SIGNAL("clicked()"),self,QtCore.SLOT("reject()"))
            self.layout.addWidget(self.pbcancel)
            self.update()
        def __del__(self):
            self.hide()
        def push(self,movie):
	    return self.pwl.push(movie)

if __name__=="__main__":
     from pycvf.lib.ui.qt import qapp
     from pycvf.lib.video.simplevideoreader7 import *
     vf="../project_specific/videozaic/skylines/QkhKSPrMgPA.flv"
     vf="../../../pyffmpeg2-alpha-candidate/2009_06_13_04_56-16.mpg"
     vr=SimpleVideoReader7(vf)
     qmw=QtGui.QMainWindow()
     x=QtDisplayMovieDialog(qmw)
     x.push(vr)
     #x.exec_()
     x.show()
     while True:
       qapp.processEvents()

