# -*- coding: utf-8 -*-

#import numpy, sys
from pycvf.core.errors import pycvf_warning
from pycvf.core import genericmodel
from pycvf.core.builders import pycvf_builder
from pycvf.datatypes import basics
from pycvf.datatypes import basics

class Model(genericmodel.Model):
        name="explodedtransfrom"
        def __init__(self,*args,**kwargs):
            super(Model,self).__init__(*args,**kwargs)
            self.structure=None
            self.model=None
        def input_datatype(self,x):
            #self.datatype_in=x
            return x
        def output_datatype(self,x):
            if (self.recomposed):
               dtp=x
            else: 
               dtp=self.structure.output_datatype(self.datatype_in)
            #model.output_datatype(self.vdb)
            return x#basics.Label.Datatype()
        def init_model(self,model,structure=None,modelelementpath="/",addressed=False,recomposed=True):
             ##
             ##
             ##
             if (structure==None):
                 structure=self.datatype_in.get_default_structure()
             if addressed:
                 pycvf_error("address is no more possible use : get_curraddr")
             self.recomposed=recomposed
             self.structure=(pycvf_builder(structure) if type(structure) in [str, unicode] else structure) 
             dtp=self.structure.output_datatype(self.datatype_in)
             self.model=(pycvf_builder(model) if type(model) in [str,unicode] else model)
             self.model.init("/",dtp,self)
             self.modelelementpath=modelelementpath
             self.model.metainf_curdb=None
             metak= self.model.get_features_meta().keys()
             modelelementpathno=metak.index(modelelementpath)
             #
             if (recomposed):
#               if (addressed):
#                 def etransform(x):
#                   decomposed=self.structure.items(x)
#                   shape=self.structure.shape(x)
#                   return self.structure.recompose(shape,[ ( self.model.process(s,addr=s[0])[modelelementpathno] , s[0]) for s in decomposed ])
#               else:
                 def etransform(x):
                   decomposed=self.structure.items(x)
                   shape=self.structure.shape(x)
                   return self.structure.recompose(shape,[ self.model.process(s[1],addr=s[0])[modelelementpathno]  for s in decomposed ])
             else:
#               if addressed:
#                 def etransform(x):
#                   decomposed=self.structure.items(x)
#                   return [ ( self.model.process((s,s[0]),addr=s[0])[modelelementpathno]) for s in decomposed ]
#               else:
                 def etransform(x):
                   decomposed=self.structure.items(x)
                   return [ ( self.model.process(s[1],addr=s[0])[modelelementpathno]) for s in decomposed ]
             self.processing=[ ('exploded_transform' , {'exploded_transform':etransform })]

__call__=Model
