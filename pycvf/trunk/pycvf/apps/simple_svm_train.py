# -*- coding: utf-8 -*-

#import orange
import numpy,shogun
from pycvf.core.generic_application import *

from shogun.Features import *
from shogun.Classifier import *
from shogun.Kernel import *




#save_classifier libsvm.model
#load_classifier libsvm.model LIBSVM


def compute_output_plot_isolines_sine(classifier, kernel, train):
        x=4*rand(1, 500)-2
        x.sort()
        test=RealFeatures(x)
        kernel.init(train, test)
        y=classifier.classify().get_labels()

        return x, y


class SimpleSvmTrainApp(ModelUsingApplication):
  class ProgramMetadata(object):
      name="Simple SVM trainer application"
      version="1.0"
      license="GPLv3"
      author="Bertrand Nouvel bertrand.nouvel@gmail.com"
      copyright="        COPYRIGHT Bertrand Nouvel - JFLI - CNRS 2009"

  @classmethod
  def process(cls,nrels=1,*args,**kwargs):
   ## we assume all our data fit into memory
   
   features=[]
   labels=[]

   # compute features according to the model
   for e in cls.vdb:
       cls.mdl.process(e[0][0],processf=(lambda x:features.append(x[0].reshape(reduce(lambda y,z:y*z,x[0].shape,1)))))
       labels.append(e[0][1])

   # stack the lists
   features=numpy.vstack(features)
   labels=numpy.vstack(labels)
   dlabels=list(set(labels.flat))


   num_svms=len(dlabels)
   width=0.5

   svmList = [None]*num_svms
   trainfeatList = [None]*num_svms
   traindatList = [None]*num_svms
   trainlabList = [None]*num_svms
   trainlabsList = [None]*num_svms
   kernelList = [None]*num_svms

   for i in range(num_svms):
        tfeatures=features.T.astype(numpy.float64).copy('C')
        print tfeatures.shape, features.dtype
        trainfeatList[i] = RealFeatures(tfeatures)     
        tlabels=((labels.squeeze()==dlabels[i]).astype(numpy.float64)*2-1).copy('C')
        print tlabels.shape, tlabels.dtype
        trainlabList[i] = Labels(tlabels) 
        kernelList[i] = GaussianKernel(trainfeatList[i], trainfeatList[i], width)
        svmList[i] = LibSVM(10, kernelList[i], trainlabList[i])#SVMOcas(3, trainfeatList[i], trainlabList[i]) #


   for i in range(num_svms):
        print "Training svm nr. %d" % (i)
        currentSVM = svmList[i]
        currentSVM.train()
        print currentSVM.get_num_support_vectors()
        print "Done."
        #print dir(currentSVM.io)
        #currentSVM.save(file("libsvm-%d.model"%(i),"w").fileno)



   ##
   ## create testing set
   ##

   features=[]
   labels=[]

   # compute features according to the model
   for e in cls.vdb:
       cls.mdl.process(e[0][0],processf=(lambda x:features.append(x[0].reshape(reduce(lambda y,z:y*z,x[0].shape,1)))))
       labels.append(e[0][1])

   # stack the lists
   features=numpy.vstack(features)
   labels=numpy.vstack(labels)

   for i in range(num_svms):
        print "Testing svm nr. %d" % (i)
        currentSVM = svmList[i]
        tfeatures=features.T.astype(numpy.float64).copy('C')
        #print dir(currentSVM)
        kernelList[i].init(trainfeatList[i],RealFeatures(tfeatures)     )
        print dlabels[i], ((currentSVM.classify().get_labels()>0) ==(labels.squeeze()==dlabels[i])).mean()*100., "% POSITIVE"
         #tfeatures)


if __name__=="__main__"   
  SimpleSvmTrainApp.run(sys.argv[1:])







   #data=orange.ExampleTable("iris.tab")
   # l=orange.SVMLearner()
   # l.svm_type=orange.SVMLearner.Nu_SVC 
   # l.nu=0.3
   # l.probability=True
   #
   # for e in cls.vdb:
   #    print cls.mdl.process(e[0],processf=lambda x:cls.idx.query([x],nq))
   # classifier=l(data)
