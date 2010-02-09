#!/usr/bin/env python
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


import numpy,gc,itertools
from pycvf.core.errors import *
from pycvf.core.generic_application import *
from pycvf.lib.info.track import OnDiskMultiTrackLarge, OnDiskMultiTrackLargeZ
from pycvf.lib.info import pmap
import cPickle as pickle 

# -*- coding: utf-8 -*-
class ComputeFeaturesApp(ModelUsingApplication):
  class ProgramMetadata(object):
      name="Feature Computer Application"
      version="1.0"
      author="Bertrand Nouvel bertrand.nouvel@gmail.com"
      copyright="        COPYRIGHT Bertrand Nouvel - JFLI - CNRS 2009"
      license="GPLv3"

  trackfilename=CmdLineString("t","trackfile","filename","name of the files where you want the features to be computed ","features")                             
  processors=CmdLineString("p","processors","number","Number of process to be runned","1")                               
  pmode=CmdLineString(None,"pmode","integer","0:1db/many features computers 1:many db/many feature computers ","2")
  accept_in_errors=CmdLineString(None,"ignoreerrors","boolean","Set to 1 for ignoring errors","0")
  meta_selector=CmdLineString(None,"metaselector","None","defines which features to select (lambda expressions on meta! see doc!)","None")

  gcs=[]
  
  @classmethod
  def process_sp(cls,*args,**kwargs):
      """ Process with a singprocesso"""
      i=iter(cls.vdb)
      cont=True
      while cont:
        try:
          e=i.next()
          print "e",e[1]
          c=(cls.mdl.process(e[0],addr=e[1],metas=cls.nmetas),e[1])
          print "c",c          
          cls.tf.append(c)
        except StopIteration:
          cont=False
        except:
          if (int(cls.accept_in_errors.value)):
              cls.tf.append(( None,e[1]))
          else:
              raise 
  
  @classmethod
  def process_pmode1(cls,*args,**kwargs):
    """
     Proceess by distributing keys to be computed and gathering results to put them in the track
    """
    p=int(cls.processors.value)
    @pmap.parallelizable(p)    
    def compute_feature(e):
        try:
          #gc.collect()
          #cls.gcs=gc.get_objects()          
          e=(cls.vdb[e],e)
          x= (cls.mdl.process(e[0],addr=e[1],metas=cls.nmetas),e[1])
          del e
          gc.collect()
          #print "A",filter(lambda x:x not in cls.gcs,gc.get_objects())
          #cls.gcs=gc.get_objects()
          return x
          #return ( numpy.zeros((1000,1000)),0)
        except Exception,e:
            import traceback, sys
            print e
            traceback.print_tb(sys.exc_info()[2])
            if (int(cls.accept_in_errors.value)):
              return None
            else:
              raise
    def append_proc(index,value):       
        cls.tf.append(value)  
    pycvf_debug(10,"Computing Keys")
    lk=list(cls.vdb.keys())
    pycvf_warning("You are using multiple processor options. Please take some time to ensure that your model is not using some internal state. (I.E. that you assume nothing about the database elements order) ")
    pmap.xmap(compute_feature,append_proc,lk)

  @classmethod
  def process_pmode0(cls,*args,**kwargs):
    """
    Proceess by distributing the values to be computed and gathering the results to be computed
    """      
    p=int(cls.processors.value)
    @pmap.parallelizable(p)    
    def compute_feature(e):
        try:
          x= (cls.mdl.process(e[0],addr=e[1],metas=cls.nmetas),e[1])
          return x
        except Exception,e:
            import traceback, sys
            print e
            traceback.print_tb(sys.exc_info()[2])
            if (int(cls.accept_in_errors.value)):
              return None
            else:
              raise
    def append_proc(index,value):       
        cls.tf.append(value)  
    pycvf_warning("You are using multiple processor options. Please take some time to ensure that your model is not using some internal state. (I.E. that you assume nothing about the database elements order) ")
    pmap.xmap(compute_feature,append_proc,cls.vdb)
    
  @classmethod
  def process_pmode2(cls,*args,**kwargs):
    """
    Proceess by distributing the values to be computed and gathering the results to be computed
    """      
    p=int(cls.processors.value)
    @pmap.parallelizable(p)    
    def compute_feature(e):
        try:
          fn=e
          e=pickle.load(file(fn))
          x= (cls.mdl.process(e[0],addr=e[1],metas=cls.nmetas),e[1])
          os.remove(fn)
          return x
        except Exception,e:
            os.remove(fn)            
            import traceback, sys
            print e
            traceback.print_tb(sys.exc_info()[2])
            if (int(cls.accept_in_errors.value)):
              return None
            else:
              raise
    def append_proc(index,value):       
        cls.tf.append(value)  
    pycvf_warning("You are using multiple processor options. Please take some time to ensure that your model is not using some internal state. (I.E. that you assume nothing about the database elements order) ")
    def tmpsave(x):
        fn=os.tmpnam()
        f=file(fn,'wb')
        f.write(pickle.dumps(x))
        f.close()
        return fn
    class O:
        def __iter__(self):
          return itertools.imap(tmpsave,cls.vdb)
        def __len__(self):
            return len(cls.vdb)
    pmap.xmap(compute_feature,append_proc,O())
  
  @classmethod
  def process(cls,nrels=1,*args,**kwargs):                         
    trackfile=cls.trackfilename.value
    meta_selector=eval(cls.meta_selector.value)
    cls.nmetas=cls.mmeta
    if (meta_selector!=None):
       cls.nmetas=dict(filter(meta_selector,cls.nmetas.items()))
       pycvf_warning("NEW METAS = %r"%(cls.nmetas,))
    else:
       cls.nmetas=None
       
       
    cls.tf=OnDiskMultiTrackLargeZ(trackfile)
    p=int(cls.processors.value)
    
    if (p>1):
        if (cls.pmode.value=='0'):
            cls.process_pmode0(*args,**kwargs)
        elif (cls.pmode.value=='1'):
            cls.process_pmode1(*args,**kwargs)
        else:
            cls.process_pmode2(*args,**kwargs)            
    else:
           cls.process_sp(*args,**kwargs)
          
    if self.tf.meta==None:
       self.tf.meta={}
    
    cls.tf.meta['model_expr']=cls.mymodel.value
    cls.tf.meta['models_meta']=cls.mmeta
    cls.tf.meta['model_class']=cls.mdl.__class__
    cls.tf.meta['inbound_datatype']=cls.vdb.__class__
    cls.tf.savemeta()
  
if __name__=="__main__":       
  ComputeFeaturesApp.run(sys.argv[1:])

