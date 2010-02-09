import traceback
import numpy
import scipy
import random
import cPickle as pickle
import marshal

try:
  from orange import *
  import orange
except:
  print "please install orange" 

print "A"
try:
  import orngSVM
except Exception,e:
  print e
print "B"  

class OrangeSVMModel():
    def __init__(self,Model=None):
      self.Model=Model
      self.mydomain=None
    def init_model(self,ndim):
      classvar=orange.EnumVariable("y",values=map(str,range(1))) 
      self.mydomain=orange.Domain( [ orange.FloatVariable("x"+str(d),startValue=-10,endValue=10) for d in range(ndim) ]
                      + [  classvar  ] )
      self.model=orngSVM.SVMLearner()
    def train(self,A_pos_set, A_neg_set, *args, **kwargs):
      if (not self.mydomain):
        self.init_model(A_pos_set.shape[1])
      training_set=numpy.vstack([
                 numpy.hstack([ A_pos_set , numpy.ones( (A_pos_set.shape[0],1) ) ]),
                 numpy.hstack([ A_neg_set , numpy.ones( (A_neg_set.shape[0],1) )*-1 ])
               ])
      self.model.kernelFunc=orngSVM.RBFKernelWrapper(orange.ExamplesDistanceConstructor_Euclidean(training_set), gamma=0.5)
      self.model.kernel_type=orange.SVMLearner.Custom
      self.model.probability=True
      self.model.name="SVM - RBF(Euclidean)"
      training_data=orange.ExampleTable(self.mydomain , training_set )
      self.c1=self.model(data)
    def test(self,data,log=True, *args, **kwargs): ## return likelihood of samples
      datatest=orange.ExampleTable(self.mydomain , data )
      if log:
        return numpy.log(self.c1(datatest))
      else:
        return numpy.log(self.c1(datatest))        
    def dump(self,file_):
      self.a.dump(file_, self)
    @staticmethod
    def load(file_, *args, ** kwargs):
      return pickle.load(file_)
    def memory_cost(self, *args, **kwargs):
        assert(False)
    def cpu_cost(self, *args, **kwargs):
        assert(False)
  
__call__=OrangeSVMModel
StatModel=OrangeSVMModel