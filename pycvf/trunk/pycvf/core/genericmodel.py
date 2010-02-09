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
## Models can be specified either directly either through loading
## filename are resolved by application
##

"""
 Generic Models For PyCVF
 ------------------------

 A model aims at providing ONE representation of the information from observations.
 
 EACH NODE OF THE MODEL IS ASSOCIATED TO A STATUS THAT TELLS WHETHER IT IS READY TO RECEIVE INFORMATION
 
 
 Models have are a key-concept of the framework.
  
 In applications GENRIC MODELS are in charged of broadcasting and linking the informations in-between different SUBMODELS.
 
 There exists THREE kind of link a model may have 
   * SUBMODEL : Knowing 1 representation / we may decide to simplify even more this representation by using SUBMODELS
   * STATISTICAL MODEL : Knowing one represntation, we may simplify this representation
   * STRUCTURES : It is sometimes usefule to decompose 1 element in many SUBELEMENTS that may be modelized by other models
   
   
 The role of THE MODEL is 
  1) to compute the representation from the model
  2) to manage the dispatch of the information among the different links that a model may habe
  3) to manage the fusion of all the information coming from the submodels

 Structures (have no direct clique concept yet)

 Algorithm may be based on different structures.

 
"""


import re, os, math, random, time,sys, traceback,logging

from pycvf.lib.info.observations import *
from pycvf.lib.info.cacheable import *
from pycvf.lib.info.track import *
from pycvf.core.errors import *

ltick=0

from pycvf.datatypes import image
from pycvf.core.structure import *
#from pycvf.lib.stats.cachedmodel import CachedModel

import scipy

class NoAddress:
  pass

class class___:
  pass


def iconcatiter(f,l):
    for e in l:
      for i in f(e):
        yield i





class STATUS_NOT_READY:
    pass

class STATUS_READY:
    pass

class STATUS_ERROR:
    pass


class Model(object):
  """
  This is our generic model class.
  """
  anonymous_ctr=0
  processline=None

  

  def input_datatype(self,datatype):
     return datatype

  def output_datatype(self,datatype):
     return datatype

  def get_directory(self):
      return self.directory

  def __init__(self,  *args, ** kwargs):
      self.parent=None ## parent node... (to be reseted to node on  delete)
      self.args=args        ## initialize arguments
      self.kwargs=kwargs   ##
      self.application=None  ## our context : pathes, databases and so on...
      self.context={}
      self.submodels={}
      self.processing=[]
      self.status=STATUS_READY
      self.invert_processing=[]
      self.directory=None
      self.datatype_in=None
      self.datatype_out=None
      self.metainfo_curdb=None
      self.metainfo_curaddr=None
      self.last_child=None
      if (self.kwargs.has_key("name") and self.kwargs["name"]!=None):
           self.name=self.kwargs["name"]
      else :
           if (not (hasattr(self.__class__,"name"))):
             self.name=None
      self.cname=None
      #self.invert_processing=None # optional
  
  def destroy(self):
      """
      This function is the counterpart of init()
      """
      if (hasattr(self,"on_destroy") and (self.on_destroy!=None)):
        self.on_destroy()
      self.parent=None
      for s in self.submodels.values():
         s.destroy()
      self.submodels=None
      #self.structures=None
      #self.statmodels=None
  
  def  set_parent(self,parent):
      self.parent=parent

  def init(self,basecname,datatype,application,*args, **kargs):
     """
     This is the second step initialization of the model.
     This function is called with some additional arguments that
     make the context quite well defined
     """
     self.cname=basecname
     self.application=application # the application
     self.directory=(kargs["directory"] if  kargs.has_key("directory") else "/tmp/" )
     try: 
       os.stat(self.directory)
     except:
       os.mkdir(self.directory)
     pycvf_debug(10,basecname)
     ## ported from 2.0
     def set_cname(a,b):
         pycvf_debug(10,"init of "+b+a[1].get_name(None)+"/")
         a[1].init(b+a[1].get_name(None)+"/",self.datatype_out, application,directory=self.directory+a[1].get_name("noname")+"/")
         for k in a[1].context.items():
           c=0
           rn=on=k[0]
           while (self.context.has_key(rn)):
              pycvf_warning("BE CAREFUL IT SEEMS THAT YOU HAVE A CONFLICT")
              rn="%s_%d"%(on,c)
              c+=1
           self.context[rn]=k[1]
     self.datatype_in=self.input_datatype(datatype)
     self.datatype_out=self.output_datatype(datatype)
     self.submodel_op(lambda x,y:issubclass(x[1].__class__,Model), set_cname, self.cname)
     self.metas=self.get_features_meta()
     self.init_model(*self.args, **self.kwargs)
     self.datatype_in=self.input_datatype(datatype)
     self.datatype_out=self.output_datatype(datatype)
     self.metas=self.get_features_meta()
     if self.processline==None:
       for pi in self.processing:
	      for i in pi[1].items():
		if (self.context.has_key(i[0])):
		  pycvf_warning("overriding name %s"%i[0])
		self.context[i[0]]=i[1]
       self.processline ='|'.join(['src']+map(lambda x:x[0],self.processing))
     self.metas=self.get_features_meta()
     #sys.stderr.write("METAS="+str(self.metas)+"\n")
     self.cnames=self.get_cnames()
     self.cnames_models=dict(self.get_cnames_models())
     self.ready=True
     
  def init_model(self,*args,**kargs):
     """
     This function contains user implementation.
     It is called separately after __init__ as a consequence of init.
     """
     pass
 
  def instantiate_types():
      """
          This function is called to instantantiate the correct structure all 
          along the models 
      """
      pass

  def get_name(self,sugg_name):
     if (not self.name):
         self.name=sugg_name
     return self.name
     
  def set_name(self,sugg_name):
      self.name=sugg_name

  def prepare_model(self):
      # normally we shall check for all submodels
      self.status=StatusReady

  #
  # Get Item
  #
  def __getitem__(self,pathitem):
     #print pathitem
     return None #self.getpath(pathitem)



  #
  # Structure construction
  #

  #def get_new_anonymous_substructure_name(self):
  #   pycvf_warning("DEPRECATED")
  #   self.anonymous_ctr+=1
  #   return "__substructure__%04d"%(self.anonymous_ctr,)

  def get_new_anonymous_submodel_name(self):
     self.anonymous_ctr+=1
     return "__submodel__%04d"%(self.anonymous_ctr,)

  #def get_new_anonymous_statmodel_name(self):
  #   pycvf_warning("DEPRECATED")
  #   self.anonymous_ctr+=1
  #   return "__statmodel__%04d"%(self.anonymous_ctr,)


  def get_last_child(self):
     if (self.last_child!=None):
        return self.last_child.get_last_child()
     return self

  def __add__(self,model2):
       c=0
       rn=on=model2.get_name(self.get_new_anonymous_submodel_name())
       while (self.submodels.has_key(rn)):
         pycvf_warning("already a submodel with name %s"%(rn))
         rn="%s_%d"%(on,c)
         c+=1
         model2.set_name(rn)
       self.submodels[rn]=model2
       self.last_child=model2
       model2.parent=self
       return self

  def __sub__(self,model2):
       self.get_last_child()+model2
       return self

  def __or__(self,model2):
       return self.get_last_child()+model2


  #def __mul__(self,struct2):
  #     pycvf_warning("DEPRECATED CONSTRUCTION")
  #     self.structures[struct2.get_name(self.get_new_anonymous_substructure_name())]=struct2
  #     return self

  #def __sub__(self,stat2):
  #     pycvf_warning("DEPRECATED CONSTRUCTION")
  #     self.statmodels[stat2.get_name(self.get_new_anonymous_statmodel_name())]=stat2
  #     return self

  def get_curdb(self):
      """
      Checks whether one may access the database to query more information about the element
      """
      if (self.metainfo_curdb==None) and (self.parent!=None):
          return self.parent.get_curdb()
      return self.metainfo_curdb
  
  def get_curaddr(self):
      """
      Checks whether address information is available for the model
      """
      if (self.metainfo_curaddr==None) and (self.parent!=None):
          return self.parent.get_curaddr()
      return self.metainfo_curaddr  

  ###
  ### BASICS META INFOS ABOUT THE MODEL
  ###



  def items(self):
    """
    Returns all the subnodes items associated to that node.
    """
    return self.submodels.items() #+ self.statmodels.items() + self.structures.items())
   
  def keys(self):
    """
    Returns all the subnodes keys associated to that node.
    """
    return self.submodels.keys() #+ self.statmodels.keys() + self.structures.keys())

  def values(self):
    """
    Returns all the subnodes associated to that node.
    """
    return self.submodels.values() #+ self.statmodels.values() + self.structures.values())

  ###
  ### process own
  ###

#  def get_default_structure(self):
#     pass
  def process(self,element,processf=None,metas=None,addr=None):
        """
          Compute all the processlines on the input element.
          
          The processline may be changed by adding meta.
          
          This functions returns the list of result for all elements of the processline, optionally 
          processed by the function processf.
          
          The argument addr may
          
          
          NOTE
          ====
          
          Do process one element (apply feature filters)
              I.E. APPLY ALL FEATURE FILTERS FOR THE SELECTION OF META
              AND RETURN THE RESULT TO THE PROCESS
        """
        if (addr!=None):
            self.metainfo_curaddr=addr
        if (not processf):
          processf=lambda x:x
        if metas==None:
          metas=self.metas
        #print self,self.processing,self.metas
        self.context['src']=element
        cacheable_object=CacheableObject(element,transform_catalog=SimpleEvaluatorTransformCatalog(self.xeval_s))
        self.context['thesrc']=cacheable_object ## allow complex observers...
        r=[]
        for o in metas.values():
             #print o["processline"]
             try:
               r.append(cacheable_object[o["processline"]]) #TODO: < Optimize
             except KeyboardInterrupt:
               raise
             except NotReady:
               #r.append(NotReady)
               raise
        #print metas
        #print "result =",len(r), len(sef)
        return processf(r)


  def process_self(self,i,push=False):
     """

     SUGG NEW FOR VERSION 3 (PROCESS ONLY THIS NODES AND NOT SUB PROCESS)

     If push=True, then the result of this computation is saved under self.processed for later use.
     
     The process function computes the model represntation of the data from the data it self.

     It assumes that not only one element is given but that an iterable set of elements is given.
     It is assumed that the result of this iterable would fit into memory.
     
     
     TODO: suggest optimized version returning template code for on-the-fly compilation...
     """
     for p in self.processing:
        i=p(i)
     if (push):
       self.processed=i
     return i

  def process_under(self,i,push=False):
     """
     This computes the results from all 
     
     """
     pi=self.process_self(i,push)
     r={'/':pi}
     for s in submodels.items(statmodel_process=None):
       r[s[0]]=s[1].process_under(pi,push)
     if (statmodel_process):
       for s in statmodels.items():
         r[s[0]]=s[1].process_under(pi,push)
     return r




  def process_path(self,elements,eaddresses,cpath,funcname,return_all=False):
      #print self.metas
      filtb=cpath
      telements=elements        
      if filtb[0]=="@":
               telements=eaddresses
      else:
               telements=self.process_multiple_alt_unimeta(telements,metas=self.metas[filtb])
      return funcname(telements)






      #sys.exit(-1)

  def process_path_deprecated(self,elements,eaddress,cpath,funcname,return_all=False):
        """
           This kind of path were too complicated thus they are DEPRECATED
           Users have now to use the KEYWORD EXPLODED....

           --------------------------------------------------------------------------------------
           COMPUTE RESULTS ALONG ONE PATH
           --------------------------------------------------------------------------------------
           //
           //model1
           //#pixels
           //#//pictures (default structure submodel)
           //model1#subimages
           --------------------------------------------------------------------------------------
        """
        print "PROCESS PATH",cpath
        l=cpath.split('#')


        ## current elements
        telements=elements
        teaddresses=eaddress
        cmodel=self


        #telements, teaddress,cmodel=process_path(self,telements,teaddresses,cpath,funcname,True)
        ###
        ### FILTERTING
        ###
        filtb=l[0]
        if filtb[0]=="@":
            if filtb=="@":
               telements=teaddresses
            elif (filtb[1]=="[" and filtb[-1]=="]"):
               def extractor(e):
                 return eval('e'+filtb[1:])
               telements=map(extractor,teaddresses)
            else:
               raise Exception, "Unknown addresses"
        elif (filtb not in ["" ,"/"]):
            #print "filtb=",filtb
            #print self.submodels
            #print telements
            telements=self.process_multiple_alt_unimeta(telements,metas= self.get_metas_by_query(filtb))
        ###
        ### DO STRUCTURE DECOMPOSITION AND RECURSION
        ###
        #if (len(l) > 1):
          #filt=l[1].split('/')
          #filta=filt[0]
          #if (filta[-1]=='*'):
            #recmode="*"
            #filta=filta[:-1]
          #elif (filta[-1]=='@'):
            #recmode="@"
            #filta=filta[:-1]
          #else:
            #recmode=False
          #filtb="/"+"/".join(l[-1].split("/")[1:])
          #if (len(l)>1):
             #print "available structures=", cmodel.structures.keys(), "len",len(l),l
             #try:
               #taddresses=reduce (lambda x,y: x+y,
                  #[ self.extract_structure(e,cmodel.structures[filta],lambda x:x,"@", eaddress) for e in telements ],
                  #[]
                #)
               #telements=reduce (lambda x,y: x+y,
                 #[ self.extract_structure(e,cmodel.structures[filta],lambda x:x,recmode, eaddress) for e in telements],
                 #[]
                #)
             #except:
               #taddresses=iconcatiter(lambda e: self.extract_structure(e,cmodel.structures[filta],lambda x:x,"@", eaddress) ,telements )
               #telements=iconcatiter(lambda e: self.extract_structure(e,cmodel.structures[filta],lambda x:x,recmode, eaddress) , telements)
             ##print telements
             ##sys.stdin.readline()
             #print cmodel.structures[filta]
             #print self.submodels.values()
             #print filter(lambda x:x[1]==cmodel.structures[filta],self.submodels.values())
             #cmodel=filter(lambda x:x[1]==cmodel.structures[filta],self.submodels.values())[0][0]
             #print cmodel
             #print "RESELEMS=", telements
             #for x in telements:
                    #print x

             #return map(funcname,[ cmodel.process_path([e[0]],[e[1]],  '#'.join(['/'.join(filt[1:])]+l[2:]), lambda x:x, return_all) for e in zip(telements,taddresses) ])
             ##assert(False)
         ###
          #print telements
        if return_all:
          return funcname(telements), teaddresses, cmodel
        else:
          return funcname(telements)


  def process_multiple_alt_unimeta(self,elements,metas=None):
        """
           INPUT : ITERABLE
           OUTPUT : ITERABLE

           Compute all one features for all the elements
        
           if meta = None then the default set of feature is used, else specified set of feature is used
   
           returns a table with one feature per row, (suitable in case where processing is later applied hierarchically)
           TODO : provide optimized computations
        """
        #print self
        if metas==None:
          metas=self.metas
        le=len(elements)
        assert(type(metas)==dict)
        r=[]
        li=iter(elements)
        for e in range(le):
          self.context['src']=li.next()
          cacheable_object=CacheableObject(elements[e],transform_catalog=SimpleEvaluatorTransformCatalog(self.xeval))
          self.context['thesrc']=cacheable_object ## allow complex observers...
          try:
               r.append(cacheable_object[metas['processline']])
          #except NotReady:
          #     r.append(NotReady)
          except NotReady:
            raise
        return r




  def submodel_op(self,submodel_selector_f, fct_f, cpath="/"):
     """
      We apply the function fct_f to all the model that match the submodel_selector_f.
      This function is not implicitely recursive if the submodels are selected
        but is recursive else
     """
     r={}
     for s in self.submodels.items():
       if (submodel_selector_f(s,cpath)):
           r[s[0]]=fct_f(s,cpath)
       else:
           r[s[0]]=s[1].submodel_op(submodel_selector_f, fct_f)
     #for s in self.statmodels.items():
     #  if (submodel_selector_f(s,cpath)):
     #      r[s[0]]=fct_f(s,cpath)
     #for s in self.structures.items():
     #  if (submodel_selector_f(s)):
     #      r[s[0]]=fct_f(s,cpath)
     return r

        
  def get_metas_by_query(self,x):       
       try:
         o=self.get_object_by_cpath("/".join(x.split('/')[:3])+"/")
       except KeyError:
         pycvf_warning("unable to find your submodel : "+ str( x))
         print "candidates are "+str(self.submodels.keys())
         raise
       return filter(lambda x:x[3]==o,self.metas)

  def get_object_by_cpath(self,cpath, cpathl=None):     
     #print self.cnames_models
     return  self.cnames_models[cpath]
  

  def submodel_merge(self,submodel_selector_f, fct_f, cpath="/"):
     """
     """
     r=[]
     for s in self.submodels.items():
       if (submodel_selector_f(s,cpath)):
           r.extend(fct_f(s,cpath))
       else:
           r.extend(s[1].submodel_op(submodel_selector_f, fct_f))
     #for s in self.statmodels.items():
     #  if (submodel_selector_f(s,cpath)):
     #      r.extend(fct_f(s,cpath))
     #for s in self.structures.items():
     #  if (submodel_selector_f(s)):
     #      r.extend(fct_f(s,cpath))
     return r


  ######################################################################################################################################################################
  ######################################################################################################################################################################
  ######################################################################################################################################################################


  
  def push(self,ein):
     #
     assert(self.datatype_in.is_valid_instance(ein))
     #
     r=self.process_self(ein, push=True)
     #
     assert(self.datatype_out.is_valid_instance(self.processed))
     #
     return r

  def get_current_obs(self):
     return self.processed

  def get_current_obsvector(self):
     return self.datatype.default_structure.decompose(self.processed)

  ######################################################################################################################################################################
  ######################################################################################################################################################################
  ######################################################################################################################################################################
  ### Meta information about one node
  ###
 
  def local_meta(self):
     """
     Returns information about one node
     """
     return {'name':self.name,'total_name':self.get_total_name(),'data_in':self.datatype_in, 'processline': self.processline,'data_out': self.datatype_out,'directory':self.get_directory()}



  def get_features_meta(self):
     #pycvf_debug(10,"getting meta")
     lm=self.local_meta()
     def update_processlines(e):
         if lm['processline']:
           d=e[1]
           d['processline']=re.subn( "src" , lm['processline'] and lm['processline'] or "src",d['processline'])[0]
           return (e[0],d)
         return e
     r=dict(self.submodel_merge( lambda x,y: issubclass(x[1].__class__,Model),
                         lambda x,y: map(update_processlines, x[1].get_features_meta().items() )
                       ))
     r[self.cname]=lm
     return r

  def get_local_status(self):
      """ Returns the local status of a node """
      return self.status#STATUS_READY

  def get_status(self):
      """ Returns STATUS_READY if and only if the whole subtree if ready"""
      ls=self.get_local_status()
      if ls!=STATUS_READY:      
          return ls
      else:
          for sub in self.submodels.values():
              s=sub.get_status()
              if (s!=STATUS_READY):
                  return s
      return STATUS_READY
  
  def get_total_name(self):
    return self.cname.replace("/","_")

  def get_cnames(self):
    "returns the complete name of a model"
    r=[]
    if (self.cname):
      r+=[ self.cname] # basecname+self.cname+"/" ] 
      #r+=map(lambda x:self.cname+"#"+x,self.structures.keys())
    r+=reduce(lambda x,y:x+ y.get_cnames(),self.submodels.values(),[])
    return r

  def get_cnames_models(self):
    "returns the complete name of all the models"
    r=[]
    if (self.cname):
      r+=[ (self.cname,self)] # basecname+self.cname+"/" ] 
    r+=reduce(lambda x,y:x+ y.get_cnames_models(),self.submodels.values(),[])
    return r


  def get_by_cname(self,cname):
    "query for a specified cname"
    return self.cnames_models[cname]
     
  def print_tree(self,  indent="",stream=sys.stdout):
     stream.write("*: "+str(self.local_meta())+"\n")
     #stream.write(indent+ "|  (submodels keys="+str(self.submodels.keys())+")\n")
     #stream.write(indent+ "|  (structures keys="+str(self.structures.keys())+")\n")
     #stream.write(indent+ "|  (statmodel keys="+str(self.statmodels.keys())+")\n")
     stream.write(indent+"|\n")
     lsm=len(self.submodels)
     submodelsi=self.submodels.items()
     for smi in range(lsm):
        sm= submodelsi[smi]
        stream.write(indent+"+-")
        sm[1].print_tree(indent=indent+(((smi+1)<lsm) and "| " or "  "),stream=stream)
        stream.write(indent+"\n")
        if (smi+1!=lsm):
          stream.write(indent+"\n")
     #lsm=len(self.statmodels)
     #statmodelsi=self.statmodels.items()
     #for smi in range(lsm):
     #   sm= statmodelsi[smi]
     #   stream.write(indent+"+-"+sm[0]+"\n")
     #   if (smi+1!=lsm):
     #     stream.write(indent+"\n")
     stream.write(indent+"\n")

  ##
  ## interpretation
  ##
  def xeval(self,s,xobject):
        return eval(s,self.context,{'xobject':xobject})

  def xeval_s(self,s,xobject):
        try :
          return eval(s,self.context,{'xobject':xobject})
        except KeyboardInterrupt:
          raise
        except NotReady:
          raise
        except Exception, e:
          pycvf_warning( "Unhandled Exception while evalutation subexpression")
          pycvf_warning( u"exception =" +unicode(e))
          pycvf_warning( u"subexpression="+unicode(s))
          #print "xobject",xobject
          #if (hasattr(sys,"last_traceback")):
          #     traceback.print_tb(sys.last_traceback)
          #else:
          #     traceback.print_tb(sys.exc_traceback)
          #sys.exit(-1)
          raise
          #assert(False)



## """""""""""""""""""""""""""""""""""""""""""
##
##


def pycvf_model_function(datatype_in=None, datatype_out=None):
  """
  This functions takes in argument the input datatype and the output_datatype of a node,
  and returns a decorator for a function doing processing that will be encapsulatedof the class 
  within a PyCVF Node.
   
   The datatype_in, datatype_out may be either a datatype, either none to leave unconstrained, either a function 
   of the current input_datatype.
   
   EXAMPLE : see file pycvf/model/image/gray.py
  """  
  def make_decorator(fct):
    class CModel(Model):
        name=fct.__name__
        #def __init__(self,*args,**kwargs):
        #   self.name=fct.__name__   
        #   super(CModel,self).__init__(*args,**kwargs)
        def input_datatype(self,x):
            dtin=(datatype_in if datatype_in !=None else x)
            if ((dtin!=None) and callable(dtin) and (hasattr(dtin,"func_name"))):
                dtin=dtin(x)
            return dtin
        def output_datatype(self,x):
            dtout= (datatype_out if datatype_out !=None else x)
            if ((dtout!=None) and callable(dtout) and (hasattr(dtout,"func_name"))):
                dtout=dtout(x)            
            return dtout        
        def init_model(self,*args,**kwargs):
                 idn=self.get_total_name()
                 self.processline='src|'+idn
                 self.context[idn]=lambda x:fct(x,*args,**kwargs)
    return CModel
  return make_decorator
    
def pycvf_model_class(datatype_in=None, datatype_out=None):
  """
  This functions takes in argument the input datatype and the output_datatype of a node,
  and returns a decorator for the class, that will provide a simple encapsulation of the class 
  within a PyCVF Node.
   
   The datatype_in, datatype_out may be either a datatype, either none to leave unconstrained, either a function 
   of the current input_datatype.
  """
  def make_decorator(cls):
    class CModel(Model):
        name=cls.__name__
        #def __init__(self,*args,**kwargs):
        #   self.name=cls.__name__   
        #   super(CModel,self).__init__(*args,**kwargs)
        def input_datatype(self,x):
            dtin=(datatype_in if datatype_in !=None else x)
            if ((dtin!=None) and callable(dtin) and (hasattr(dtin,"func_name"))):
                dtin=dtin(x)
            return dtin
        def output_datatype(self,x):
            dtout= (datatype_out if datatype_out !=None else x)
            if ((dtout!=None) and callable(dtout) and (hasattr(dtout,"func_name"))):
                dtout=dtout(x)            
            return dtout
        def init_model(self,*args,**kwargs):
                 idn=self.get_total_name()
                 self.processline='src|'+idn
                 self.cmodel_inst=cls(*args,**kwargs)
                 if hasattr(self.cmodel_inst,"set_model_node"):
                     self.cmodel_inst.set_model_node(self)
                 self.context[idn]=self.cmodel_inst.process
        def on_destroy(self):
            if hasattr(self.cmodel_inst,"on_model_destroy"):
                self.cmodel_inst.on_model_destroy(self)                        
        def __del__(self):
          super(CModel,self).__del__()  
    return CModel
  return make_decorator
