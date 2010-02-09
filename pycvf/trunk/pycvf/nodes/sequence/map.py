# -*- coding: utf-8 -*-
#########################################################################################################################################
#
# MyModel By Bertrand NOUVEL
# 2009 CNRS Postdoctorate JFLI
#
# (c) All rights reserved
# ###############################################
#
################################################################################################################################################################################
# Includes
################################################################################################################################################################################


###
###


from pycvf.core import genericmodel
from pycvf.datatypes import image
from pycvf.datatypes import basics

#class Model(genericmodel.Model):
        #@classmethod
        #def input_datatype(self,x):
            #return x
        #def output_datatype(self,x):
            #return x
        #def init_model(self,mdl,id="",*args,**kwargs):
                 #mdl.init('/',self.datatype_in)
                 #def xmap(l):
                    #return map(lambda e:emdl.process(e),l)
                 #self.processline='src|map'+id
                 #self.context['map'+id]=xmap

class ModelMap:
  def __init__(self,mdl,modelelementpath=-1,*args, **kwargs):
       self.mdl=mdl
       self.modelelementpath=modelelementpath
       self.modelelementpathno=0
  def set_model_node(self,model):
      self.model_node=model
      self.mdl.init('/',self.model_node.datatype_in, self.model_node)
      #self.model.metainf_curdb=None
  def on_model_destroy(self,model):
       self.mdl=None
       self.model_node=None
       metak= self.mdl.get_features_meta().keys()
       try: 
         self.modelelementpathno=metak.index(modelelementpath)
       except:
         self.modelelementpathno=modelelementpath
  def process(self,l):
   return map(lambda e:self.mdl.process(e)[self.modelelementpathno],l)

Model=genericmodel.pycvf_model_class(None,None)(ModelMap)
__call__=Model
