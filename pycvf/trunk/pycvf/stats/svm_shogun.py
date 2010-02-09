from pycvf.core.errors import *
import numpy,shogun
from shogun.Features import *
from shogun.Classifier import *
from shogun.Kernel import *

class SvmShogun(object):
   def __init__(self):
        pass
   def train(self,pos,neg,width=0.5,online=False):
        assert(online==False)
        features=numpy.vstack([pos,neg])
        labels=numpy.vstack([numpy.ones((pos.shape[0],1)),numpy.ones((neg.shape[0],1))*-1])
        self.tfeatures=features.T.astype(numpy.float64).copy('C')
        self.features = RealFeatures(self.tfeatures)     
        self.tlabels=(labels.squeeze()).astype(numpy.float64).copy('C')
        self.labels = Labels(self.tlabels) 
        self.kernel = GaussianKernel(self.features, self.features, width)
        self.svm = LibSVM(10, self.kernel, self.labels)
        self.svm.train()
        pycvf_debug(10,"Training is finished")
        pycvf_debug(10,"Number of support vector : "+str(self.svm.get_num_support_vectors()))
   def test(self,features):
        tfeatures=features.T.astype(numpy.float64).copy('C')
        self.kernel.init(self.features,RealFeatures(tfeatures)     )
        return self.svm.classify().get_labels()
   def dump(self,file_):
        pickle.dump(file_, self)
   @staticmethod
   def load(file_, *args, ** kwargs):
      return pickle.load(file_)
   def memory_cost(self, *args, **kwargs):
      return self.svm.get_num_support_vectors()*10
   def cpu_cost(self, *args, **kwargs):
      return self.svm.get_num_support_vectors()*10
   
__call__=SvmShogun
StatModel=SvmShogun
