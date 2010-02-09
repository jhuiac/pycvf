# -*- coding: utf-8 -*-
import numpy
import scipy
import zopencv
from pycvf.core import genericmodel
from pycvf.datatypes import image
from pycvf.datatypes import basics

from pycvf.core.distribution import *

pycvf_dist(PYCVFD_MODULE_STATUS, PYCVFD_STATUS_EXPERIMENTAL)

def largest_contour(src,maxLevel = 2):
  if (src.ndim==2):
      src=src.reshape(src.shape+(1,))
  if (src.shape[2]!=1):
      src=src.mean(axis=2)
  if (src.dtype!=numpy.uint8):
      src=src.astype(numpy.uint8)
  storage=zopencv.cvCreateMemStorage(0)
  contour=zopencv.zopencv_pclasses.PointerOnCvSeq(0)
  ctrobj=zopencv.CvContour()
  szx=ctrobj.get_sizeof(ctrobj)
  offset=zopencv.CvPoint()
  offset.x=offset.y=0
  zopencv.cvFindContours( src, storage.get_pointer(), contour.get_pointer_on_pointer(), szx, zopencv.CV_RETR_LIST, zopencv.CV_CHAIN_APPROX_SIMPLE ,offset);
  if( not contour.get_pointer() ):
      return []
  # find largest contour
  iterator=zopencv.CvTreeNodeIterator()
  zopencv.cvInitTreeNodeIterator( iterator.get_pointer(), contour.get_pointer(), maxLevel );
  largest = zopencv.zopencv_pclasses.PointerOnCvSeq(0)
  largest_total = 0
  i=0
  contour=zopencv.zopencv_pclasses.PointerOnCvSeq((zopencv.cvNextTreeNode( iterator ))) 
  while( contour.get_pointer() != 0 ) :
      if( not (contour.flags & zopencv.CV_SEQ_FLAG_HOLE ) and contour.total > largest_total ):
         largest = contour;
         largest_total = contour.total;
      i+=1
      contour=zopencv.zopencv_pclasses.PointerOnCvSeq((zopencv.cvNextTreeNode( iterator )))       
  contour = largest
  # convert it to python
  return map(lambda x:(x.x,x.y),map(lambda x:zopencv.zopencv_pclasses.PointerOnCvPoint(contour.getSeqElem(x)) ,range(contour.total)))
  

Model=genericmodel.pycvf_model_function(image.Datatype,basics.Label.Datatype)(largest_contour)
__call__=Model
