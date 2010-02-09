#!/usr/bin/env pythons
# -*- coding: utf-8 -*-
#########################################################################################################################################
# 2009 CNRS Postdoctorate JFLI
#
# (c) All rights reserved
# ###############################################
#
#########################################################################################################################################
# Import required objects
#########################################################################################################################################

from pycvf.core.generic_application import *


##
## Here we expect to computer a pediction label according to the knn.
##

#def classif_score1(p1,v2)
#    label_vector=u1(labels.index(p1))
#    predict_label_vector=
#    return scipy.linalg.norm(label_vector,predict_label_vector)


def eval1(x,y):
    print  x[0][0]
    Y=zip(map(lambda t:t[0][0][0],y),range(len(y)))
    print Y
    return sum(map(lambda t:((1+len(y)-t[1]) if t[0]== x[0][0] else 0),Y))

eval_score_f=eval1


class DbIdxEvaluator(IndexUsingApplication):
  class ProgramMetadata(object):
      name="Index Evaluator Application"
      version="1.0"
      author="Bertrand Nouvel bertrand.nouvel@gmail.com"
      copyright="        COPYRIGHT Bertrand Nouvel - JFLI - CNRS 2009"

        
  key=CmdLineString(None,"key","modelpath","specified within the model what should be used as key when indexing","/")
  value=CmdLineString(None,"value","modelpath","specified within the model what should be used as value when indexing","@")
  runs=CmdLineString(None,"runs","number","number of time to run the test","3")
  ttrario=CmdLineString(None,"ttrario","ratio","ratio in-between test data and train data ","0.1")
  K=CmdLineString("K","nnn","integer","Number of nearest neighbors","5")
  evalf=CmdLineString("E","evalf","python expression","Function to evaluate result according to label","")
  labelf=CmdLineString("L","labelf","name","Name of the label set to be used","")
  
  @classmethod 
  def split_db(cls, db, ratio=0.5):
    import numpy,itertools
    try:
      l=len(db)
    except:
      l=reduce(lambda x,y:x+1,db,0) # evaluate the len of the databe
    r=numpy.random.random((l,))
    nrt=ratio/(ratio+1.)
    train_db=itertools.imap(lambda x:x[0],itertools.ifilter(lambda x:r[x[1]]>=nrt,itertools.izip(db ,range(l))))
    test_db=itertools.imap(lambda x:x[0],itertools.ifilter(lambda x:r[x[1]]<nrt,itertools.izip(db ,range(l))))
    return train_db, test_db

  @classmethod          
  def process(cls,*args, **kwargs):
      cls.mdl.print_tree()
      K=int(cls.K.value)
      runs=[]
      
      for r in range(int(cls.runs.value)):
        print "run",r
        train_db, test_db=cls.split_db(cls.vdb,float(cls.ttrario.value))
        cls.idx.reset()
        for e in train_db:
          keys=cls.mdl.process_path([e[0]],[e[1]],cls.key.value,lambda x:x)
          values=cls.mdl.process_path([e[0]],[e[1]],cls.value.value,lambda x:x)
          for c in zip(keys,values):
               cls.idx.add(c[0],c[1])
               
        cls.idx.commit()
        resv=0.
        t=0.
        print "doing test",r
        for e in test_db:
          keys=cls.mdl.process_path([e[0]],[e[1]],cls.key.value,lambda x:x)
          values=cls.mdl.process_path([e[0]],[e[1]],cls.value.value,lambda x:x)
          for c in zip(keys,values):
               a,b= c[1],cls.idx.query([c[0]],K)
               resv+=eval_score_f(a,b[0])
               t+=1
        print "mean score at run %d : %f %f/%d"%(r,resv/t, resv,t)
        runs.append(resv/t)
      print "======================================================"        
      print "================ Overall results ====================="
      print runs
      print sum(runs)/len(runs)

if __name__=="__main__":       
  DbIdxEvaluator.run(sys.argv[1:])

