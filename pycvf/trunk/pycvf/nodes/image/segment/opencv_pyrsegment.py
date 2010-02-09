# -*- coding: utf-8 -*-

from pycvf.core import genericmodel
from pycvf.datatypes import image
import zopencv

def opencv_pyrsegmentation( image0, threshold1 =255,threshold2 =30, level=4,output=0):
    block_size = 0
    storage = zopencv.cvCreateMemStorage ( block_size )
    height,width=image0.shape[:2]
    width =width & -(1<<level)
    height =height & -(1<<level)
    image0 = image0[:height,:width,:].copy('C')
    image1 = image0.copy('C')
    comp=zopencv.zopencv_pclasses.PointerOnCvSeq(0)
    zopencv.cvPyrSegmentation(image0, image1, storage,  comp.get_pointer_on_pointer(), level,   min(255,max(5, threshold1+1)), min(255,max(5, threshold2+1)))
    #del comp
    #comp=None
    zopencv.cvReleaseMemStorage(storage.get_pointer_on_pointer())
    if (output==0):
      return image1.copy('C')
    elif (output==1):
      return comp
    else:
      return image1,comp

Model=genericmodel.pycvf_model_function(image.Datatype,image.Datatype)(opencv_pyrsegmentation)
__call__=Model