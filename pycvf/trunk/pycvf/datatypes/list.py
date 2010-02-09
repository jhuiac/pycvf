# -*- coding: utf-8 -*-

from PyQt4 import QtCore

def Datatype(ElemType):
  class _ListDatatype:
    ld=None
    ElementType=ElemType
    content_type="List("+ElemType.content_type+")"
    @classmethod
    def display(cls,x):
      for e in x:
        ElemType.display(x)
    @classmethod
    def get_numpy(cls,x):
      return numpy.array( [ ElemType.get_numpy(e) for e in x  ])
    @staticmethod
    def pylab_display(cls,x):
       assert(False)
    @classmethod
    def get_widget(cls,*args):
       from PyQt4.QtGui import QListWidget
       q=QListWidget(*args)
       return q
    @classmethod 
    def distance(cls,x1,x2): 
       return min(scipy.spatial.distance.cdist(x1,x2,ElemType.distance))
    @classmethod
    def set_widget_value(cls,widget,x):
        #print widget
        widget.clear()
        for i in range(len(x)):
            q=ElemType.get_widget(widget)
            ElemType.set_widget_value(q,x[i])
            widget.addItem(str(i))
            wi=widget.item(i)
            widget.setItemWidget(wi,q)
            arw=q.minimumWidth()
            arh=q.minimumHeight()
            #print "ARW,ARH",arw, arh
            wi.setSizeHint(QtCore.QSize(arw,arh))
    @classmethod
    def get_typerelated_structures(cls):
        return { }
    @classmethod
    def get_default_structure(cls):
       from pycvf.structures import list as ls
       return ls.DefaultStructure()
  return _ListDatatype
