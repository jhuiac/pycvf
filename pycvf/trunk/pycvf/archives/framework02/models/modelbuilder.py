#!/usr/bin/env python
# -*- coding: utf-8 -*-
## ##########################################################################################################
## 
## This file is released under GNU Public License v3
## See LICENSE File at the top the pycvf tree.
##
## Author : Bertrand NOUVEL / CNRS (2009)
##
##
##
## Revision FILE: $Id$
##
## ###########################################################################################################
## copyright $Copyright$
## @version $Revision$
## @lastrevision $Date$
## @modifiedby $LastChangedBy$
## @lastmodified $LastChangedDate$
#############################################################################################################


# -*- coding: utf-8 -*-
## 
## We agglomerate high level models to make more powerful / specific models
## 

from pycvf.core.genericmodel import *
from pycvf.lib.stats.models import *


#for x

class M:
  structurepath=None
  def __init__(self,modelname, *args, **kwargs):
     self.modelname=modelname
     self.args=args
     self.kwargs=kwargs
     self.submodels={}
     self.structures={}
     self.statmodels={}
  def __get_model(self,name,basepath,path="//"):
    try:
       iname=self.modelname
       module=__import__(iname,fromlist=iname.split(".")[:-1])
    except:
       iname="pycvf.nodes."+self.modelname
       module=__import__(iname,fromlist=iname.split(".")[:-1])
    return module.Model

  def _create(self,name,basepath,path="//"):
    _model=self.__get_model(name,basepath)
    return _model
    
  def create(self,name,vdb,basepath,path="//"):
    _model=self.__get_model(name,basepath)
    model=_model(name,vdb,basepath)
    return model

  def set_env(self,path,dargs):
    if not (dargs.has_key(path)):
       dargs[path]=((self.args,self.kwargs,{}))
    else:
       (oargs,okwargs,xxargs)=dargs[path]
       mdict=okwargs.copy()
       for i in self.kwargs:
          mdict[i[0]]=i[1]
       dargs[path]=((oargs+list(self.args),mdict,xxargs))
    for x in self.submodels.items():
       if hasattr(x[1],"_create"):
         x[1].set_env(path+x[0]+"/",dargs)
    for x in self.structures.items():
       dargs[path+x[0]]=x[1]
       x[1].set_env(path+x[0]+"/",dargs)
    for x in self.statmodels.items():
       dargs[path+x[0]]=x[1]
       x[1].set_env(path+x[0]+"/",dargs)     
##
##

  def set_structure_args(self,name,_model,basepath,dico):
    dsubmodels=_model.submodels.copy()
    #dstructures=_model.stuctures.copy()
    dstructures={}
    dstatmodels=_model.statmodels.copy()
    for x in self.submodels.items():
       #print "mirroring submodel:",x
       dsubmodels[x[0]]=(x[1].__get_model(x[0],basepath+x[0]+"/"),x[1].structurepath)

       x[1].set_structure_args(x[0], x[1].__get_model(x[0],basepath+x[0]+"/" ) ,basepath+x[0]+"/",dico)

    for x in self.structures.items():
       #print "mirroring structure:",x
       dstructures[x[0]]=x[1].x__get_structure(x[0],basepath+x[0]+"/")
    for x in self.statmodels.items():
       #print "mirroring statmodels:",x
       dstatmodels[x[0]]=x[1].x__get_statmodel(x[0],basepath+x[0]+"/")
    if not dico.has_key(basepath):
       dico[basepath]=([],{},{})
    dico[basepath][2]["submodels"]=dsubmodels
    dico[basepath][2]["structures"]=dstructures
    dico[basepath][2]["statmodels"]=dstatmodels

  def new(self,name,vdb,basepath,path="//"):
    model=self.create(name,vdb,basepath,path)
    dargs={}
    #dargs[path+self.modelname]=((self.args,self.kwargs))
    dsubmodels={}
    dstructures={}
    dstatmodels={}
    for x in self.submodels.items():
       print "mirroring submodel:",x
       if hasattr(x[1],"_create"):
         #submodel=x[1]._create(x[0].split('/')[-1],path+"/"+x[0])  
         submodel=x[1]._create(x[0],path+"/"+x[0])  
         dsubmodels[x[0]]=(submodel,x[1].structurepath)
         self.set_structure_args(x[0],submodel,path,dargs)
       else:
         submodel=x[1]
         dsubmodels[x[0]]=(submodel,x[1].structurepath)
#       print dargs
    for x in self.structures.items():
       print "mirroring structure:",x
       print x[1].x__get_structure(x[0],path+x[0])
       if type(x[1].x__get_structure(x[0],path+x[0])) in [ 'unicode', 'str'] :
          dstructures[x[0]]=x[1].x__get_structure(x[0],path+x[0])+"/"
       else:
          dstructures[x[0]]=x[1].x__get_structure(x[0],path+x[0])           
    for x in self.statmodels.items():
       print "mirroring statmodels:",x
       dstatmodels[x[0]]=x[1].x__get_statmodel(x[0],path+x[0]+"/")
    self.set_env(path,dargs)
    print type(model)
    #model*dstructures
    #model|dubmodels
    #model-dstatmodels
    #print dir(model)
    #print model.submodels
    #print GenericModel.submodels
    model.extend_structures(dstructures)
    model.extend_submodels(dsubmodels)
    model.extend_statmodels(dstatmodels)
    #print model.submodels
    #print GenericModel.submodels
    #print model,model.submodels,model.submodels.values()[0],"sm=",model.submodels.values()[0].submodels
    #print dargs
    print "dargdict",dargs
    print "dsubstruct",dstructures
    print "dsubmodels",dsubmodels
    model.recinit(dargs,"//")
    
    return model
  def __mul__(self,x):
    for i in x.items():
      self.structures[i[0]]=i[1]
    return self
  def __or__(self,x):
    print "or"
    for i in x.items():
      self.submodels[i[0]]=i[1]    
    return self
  def __sub__(self,x):
    for i in x.items():
      self.statmodels[i[0]]=i[1]    
    return self

class MS(M):
  def __init__(self,structurepath,modelname, *args, **kwargs):
       M.__init__(self,modelname,*args,**kwargs)
       self.structurepath=(1,structurepath)


class MR(M):
  def __init__(self,structurepath,modelname, *args, **kwargs):
       M.__init__(self,modelname,*args,**kwargs)
       self.structurepath=(-1,structurepath)


class S:
  def __init__(self,structurenameortuple, *args, **kwargs):
     self.structurenameortuple=structurenameortuple
     self.args=args
     self.kwargs=kwargs
  def new(self,name,basepath,path="//"):
    iname=(type(self.structurenameortuple)==tuple) and self.structurenameortuple[0] or self.structurenameortuple
    try:
       module=__import__(".".join(iname.split(".")[:-1]),fromlist=iname.split(".")[:-2])
    except:
       iname="pycvf.nodes.structures."+iname
       module=__import__(".".join(iname.split(".")[:-1]),fromlist=iname.split(".")[:-2])
    structure=eval('m.'+iname.split(".")[-1], {'m': module} )
    if (type(self.structurenameortuple)==tuple):
       return (structure, self.structurenameortuple[1])
    else:
       return structure
  def x__get_structure(self,name,basepath,path="//"):
    iname=(type(self.structurenameortuple)==tuple) and self.structurenameortuple[0] or self.structurenameortuple
    try:
       module=__import__(".".join(iname.split(".")[:-1]),fromlist=iname.split(".")[:-2])
    except:
       iname="pycvf.nodes.structures."+iname
       module=__import__(".".join(iname.split(".")[:-1]),fromlist=iname.split(".")[:-2])
    structure=eval('m.'+iname.split(".")[-1], {'m': module} )
    if (type(self.structurenameortuple)==tuple):
       return (structure, self.structurenameortuple[1])
    else:
       return structure
  def set_env(self,path,dargs):
    dargs[path]=((self.args,self.kwargs))

class L:
  def __init__(self,lowlevelname, *args, **kwargs):
     self.lowlevelname=lowlevelname
     self.args=args
     self.kwargs=kwargs
  def new(self,name,basepath,path="//"):
    try:
       iname=self.lowlevelname
       module=__import__(".".join(iname.split(".")[:-1]),fromlist=iname.split(".")[:-2])
    except:
       iname="pycvf.lib.stats."+self.lowlevelname
       module=__import__(".".join(iname.split(".")[:-1]),fromlist=iname.split(".")[:-2])
    lowlevel=eval('m.'+iname.split(".")[-1], {'m': module} )
    #dargs={}
    #dargs[path=self.lowlevelname]=((self.args,self.kwargs))    
    #lowlevel.init(dargs)
    return lowlevel
  def x__get_statmodel(self,name,basepath,path="//"):
    try:
       iname=self.lowlevelname
       module=__import__(".".join(iname.split(".")[:-1]),fromlist=iname.split(".")[:-2])
    except:
       iname="pycvf.lib.stats."+self.lowlevelname
       module=__import__(".".join(iname.split(".")[:-1]),fromlist=iname.split(".")[:-2])
    lowlevel=eval('m.'+iname.split(".")[-1], {'m': module} )
    return lowlevel
  def set_env(self,path,dargs):
    dargs[path]=((self.args,self.kwargs))

def model_build(mdlexpr,vdb,root="/",modelpath="/tmp",suppargs="",context=None):
   """
      M("image.colormodel",modelargs(1)) * d(struct1="spatial.Spatial")) | d(mdl1=M("model2",modelargs) | ( model3(modelargs) ~ [ GMM() ]   | model3() - [ Gaussian() ] ] 
      () = parenth
      []  = list
      | []  = submodel relationship
      - []  statmodels
      + [] structure
   """
   if str(mdlexpr)[0]=="#":
      if context==None:
        context={}
      xd=context.copy()
      xd['M']=M 
      xd['MS']=MS
      xd['MR']=MR
      xd['S']=S
      xd['L']=L
      #xd['LS']=LS
      xd['d']=dict
      mdlf=eval(mdlexpr[1:],xd)
      mdl=mdlf.new(root,vdb,modelpath)
   else:
     #print mdlexpr[0]
     try :
      exec("from "+ mdlexpr +" import Model")
     except ImportError:
      exec("from pycvf.nodes."+ mdlexpr +" import Model")
     mdl=Model(mdlexpr,vdb)
     argdict=eval('{'+suppargs+'}')
     mdl.recinit({'//':({},argdict,{})},"//")

   return mdl
   
   
