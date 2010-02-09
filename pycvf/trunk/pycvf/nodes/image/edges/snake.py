# -*- coding: utf-8 -*-
import numpy
import scipy
import zopencv
from pycvf.core import genericmodel
from pycvf.datatypes import image
from pycvf.datatypes import basics

def snake(src,alpha=0.45,beta=0.2,gamma=0.45,max_iter=1000,epsilon=0.001,length=int(50),neigborhoodsize=(10,10)):
  CV_VALUE=1
  if (src.ndim==2):
      src=src.reshape(src.shape+(1,))
  if (src.shape[2]!=1):
      src=src.mean(axis=2)
  src=src.astype(numpy.uint8)
  w2,h2=src.shape[1]/2,src.shape[0]/2
  points=(numpy.vstack([scipy.cos(numpy.arange(0,scipy.pi*2,scipy.pi*2./length))*w2+w2,scipy.sin(numpy.arange(0,scipy.pi*2,scipy.pi*2./length))*h2+h2])).T.astype(numpy.int32)
  alpha=numpy.array([alpha], dtype=numpy.float32)
  beta=numpy.array([beta], dtype=numpy.float32)
  gamma=numpy.array([gamma], dtype=numpy.float32)
  size=zopencv.cvSize(neigborhoodsize[0]|1,neigborhoodsize[1]|1)
  criteria=zopencv.CvTermCriteria()
  criteria.type=zopencv.CV_TERMCRIT_ITER+zopencv.CV_TERMCRIT_EPS;
  criteria.max_iter=max_iter;
  criteria.epsilon=epsilon;
  zopencv.cvSnakeImage( src, zopencv.memory_addr_of_numpy_array(points),length,alpha,beta, gamma,CV_VALUE,size,criteria,0 );
  return points

Model=genericmodel.pycvf_model_function(image.Datatype,basics.Label.Datatype)(snake)
__call__=Model
