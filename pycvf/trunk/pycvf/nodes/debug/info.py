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
from pycvf.core.errors import *



    
    
class Model(genericmodel.Model):
        type_in=None
        type_out=None
        def input_datatype(self,x):
            return self.type_in or x
        def output_datatype(self,x):
            return self.type_out or x
        def debuginfo(self,x):
          pycvf_debug(10, "type(x)" + str(type(x)))
          if (type(x) in [list] ):
            pycvf_debug(10, "type(x[0])" + str(type(x[0])))        
          pycvf_debug(10, "dir(x)" + str(dir(x)))  
          pycvf_debug(10, "x="+ str(x)[:60]+"..."+str(x)[-60:])
          if (type(x) in [list] ):
            pycvf_debug(10, "x[0]="+ str(x[0])[:60]+"..."+str(x[0])[-60:])
          if (hasattr(x,"next") ):
            x0=x.next()
            try:
              pycvf_debug(10, "x[0]="+ str(x0)[:60]+"...")
            except StopIteration:
              pycvf_debug(10, "x->StopIteration")
              pass
          pycvf_debug(10, "db="+ str(self.get_curdb()))
          pycvf_debug(10, u"address="+ unicode(self.get_curaddr()))      
          return x
        
        def init_model(self,id="",*args,**kwargs):
                 self.processline='src|debuginfo'+id 
                 self.context['debuginfo'+id]=self.debuginfo

__call__=Model
