# -*- coding: utf-8 -*-

def Datatype(ElemType):
  class _GeneratedDatatype:
    ld=None
    ElementType=ElemType
    content_type="Generator("+ElemType.content_type+")"
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
    def set_widget_value(cls,widget,x,*args,**kwargs):
        #print widget
        widget.clear()
        xc=x#.copy()
        for i in range(3):#len(x)):
            q=ElemType.get_widget(widget)
            ElemType.set_widget_value(q,xc.next())
            widget.addItem(str(i))
            widget.setItemWidget(widget.item(i),q)
    @classmethod
    def get_typerelated_structures(cls):
        return { }
    @classmethod
    def get_default_structure(cls):
       from pycvf.structures import generator as gs
       return gs.DefaultStructure()
  return _GeneratedDatatype
