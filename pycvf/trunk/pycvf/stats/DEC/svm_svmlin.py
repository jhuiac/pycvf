import traceback
import numpy
import os
import random

from pycvf.lib.info import svmformat

class SVMLin_SVMModel():
    def __init__(self,filename="/tmp/svmlin"):
        self.filename=filename
    def train(self,A_pos_set, A_neg_set, online=False):
        assert(online==False)
        filename="%s-training"%(self.filename,)
        labelfilename="%s-traininglabels"%(self.filename,)        
        svmformat.output_matrix_svmformat(numpy.vstack([A_pos_set,A_neg_set]) ,filename)
        f=open(labelfilename,"w")
        f.write("\n".join(["1",] * len(A_pos_set) + ["-1",] * len(A_neg_set)))
        f.close()
        os.system("svmlin %s %s "%(filename,labelfilename))
    def test(self,data,log=True): ## return likelihood of samples
        filename="%s-training.weights"%(self.filename,)
        filename2="%s-testing"%(self.filename,)
        svmformat.output_matrix_svmformat(data,filename2)
        print "running test"
        os.system("svmlin -f %s %s"%(filename, filename2) )
        A=numpy.array(map(lambda x:float(x),open("%s.testing.outputs"%(self.filename,)).readlines()))
        if log:
          return numpy.log(A)
        else:
          return A
    def dump(self,file_):
      self.a.dump(file_, self)
    @staticmethod
    def load(file_, *args, ** kwargs):
      return pickle.load(file_)
    def memory_cost(self, *args, **kwargs):
        assert(False)
    def cpu_cost(self, *args, **kwargs):
        assert(False)
  
__call__=SVMLin_SVMModel
StatModel=SVMLin_SVMModel
