# -*- coding: utf-8 -*-
#########################################################################################################################################
#
# Abstract Model
# 2009 CNRS Postdoctorate JFLI
#
# (c) All rights reserved Bertrand Nouvel
# ###############################################
#
#########################################################################################################################################
# Import required objects
#########################################################################################################################################

import re, os, math, random, time,sys, traceback,logging
from pycvf.lib.info.observations import *
from pycvf.lib.info.cacheable import *
from pycvf.lib.info.track import *
from pycvf.core.errors import *

ltick=0

from pycvf.datatypes import image
from pycvf.nodes.structure import *
from pycvf.lib.stats.cachedmodel import CachedModel

import scipy

class NoAddress:
  pass

class class___:
  pass


def iconcatiter(f,l):
    for e in l:
      for i in f(e):
        yield i



class GenericModel(object):
  """
    To 1 model : 1 shape / possible many stats models
 
    Un model est objet  
     0) Integrant des elements de traitement des donnees
     1) Potentiellement pompose par des modeles elementaires au niveau statistique ou d'autres modeles
     2) Integrant des facilites pour les operations les plus courantes et la sauvegarde des donnees associees sur disque.


     A) 
     La gestion de l'enregistrement / chargement des modeles provient 
       de primitives statistiques
     
     B) L'ensemble des chemins du modele doit etre si possible inversible.

     C) Les hypotheses courantes comme : 
           A presence d'un modele local a telle niveau, ou tel niveau doivent etre facilement accesibles..
           
           Les resultats doivent pouvoir etre sauvegarder dans des fichiers ou stockes pour d'autres procedure...


           Pour simplifier, les objets reader et writer doivent a termes fonctionnes uniformement comme fichier ou tableau..
           
           GenericModel doivent aussi se charger de preserver le type des elements appris / restitues...

      Il n'y a normalement pas de calcul de sortie sans statisique associe... donc le processus de creation des liens est inverse a celui precedement vu...
          Chaque model include son propre filtrage(et ne corresspond qu'a un parcours)
  """
  ##############################################################################################################################################################################
  ##############################################################################################################################################################################
  ### Since we may iterate over long files(video, or pixel in images images)
  ###
  ### The way to push the data during training and testing maybe different and meybe depedant of the model to learn
  ###
  ### The models must not be instantiated in the FEATURES STREAM
  ### The FEATURES MUST BE NAMED
  ##############################################################################################################################################################################
  ##############################################################################################################################################################################  

  featurefilter=None
  structures={}  ## ARE INITIALLY : INSTANCES, (INSTANCE, CLIQUESEL), (CLASS, CLASSPARAMS), ((CLASS, CLASSPARAMS), CLIQUESEL)
  submodels={}
  statmodels={}
  datatype=lambda self,x:x
  input_datatype=lambda self,x:x
  add_ctx={}

  def __init__(self,name,datatype,modelpath="/tmp",featurefilter=None,save_after_each_sample=False,structures=None,submodels=None, statmodels=None):
      self.mode=" "
      self.modelpath=modelpath             
      self.context={}
      self._datatype=datatype
      self.instantiated_datatype=None
      self._featurefilter=featurefilter
      self._structures=structures
      self._submodels=submodels
      self._statmodels=statmodels
      self.structures=self.structures.copy()
      self.statmodels=self.statmodels.copy()
      self.submodels=self.submodels.copy()
      self.save_after_each_sample=save_after_each_sample
      self.shape=None ## use to save shape
      self.cname=None
      self.dicargs={}
      self.add_ctx=GenericModel.add_ctx.copy()
      self.ready=False
      #assert(self.submodels=={})


  def substructure_construct(self):
      if (self._featurefilter):
         self.featurefilter=self._featurefilter ## each model must be associated with a datatype, and an input datatype
      else:
         self.init_featurefilter()
       
      if 1:
      #try:
         dt=self.datatype(self._datatype)
         self.instantiated_datatype=dt
         if (dt):
           for i in dt.get_typerelated_structures().items():
             #assert(not self.structures.has_key(i[0]))
             if self.structures.has_key(i[0]):
                sys.stderr.write("#*#*#* WARNING overwrting structure + "+ i[0] +" + \n")

             self.structures[i[0]]=i[1]  ### submodels that are used in learning datas (they have to be highlevel models like genericmodels)
         else:
            sys.stderr.write("error "+str(self)+" has no datatype\n")
      #except:
      #   pass

      if (self._structures):
         for i in self._stuctures.items():
            assert(not self.structures.has_key(i[0]))
            self.structures[i[0]]=i[1]  
      if (self.dicargs.has_key(self.cname) and self.dicargs[self.cname][2].has_key("structures")):
         for i in self.dicargs[self.cname][2]["structures"].items():
            assert(not self.structures.has_key(i[0]))
            self.structures[i[0]]=i[1]  
      self.init_structures()


      if (self._submodels):
         for i in self._submodels.items():
            self.submodels[i[0]]=i[1]  ### submodels that are used in learning datas (they have to be highlevel models like genericmodels)
      if (self.dicargs.has_key(self.cname) and self.dicargs[self.cname][2].has_key("submodels")):
         for i in self.dicargs[self.cname][2]["submodels"].items():
            self.submodels[i[0]]=i[1]  ### submodels that are used in learning datas (they have to be highlevel models like genericmodels)          
      self.init_submodels()

      #print "POST",self.submodels
      if (self._statmodels):
         for i in self._statmodels.items():
            self.statmodels[i[0]]=i[1]  
      if (self.dicargs.has_key(self.cname) and self.dicargs[self.cname][2].has_key("statmodels")):
         for i in self.dicargs[self.cname][2]["statmodels"].items():
            self.statmodels[i[0]]=i[1]  
      self.init_statmodels()


      for m in self.submodels.keys():
        try:
          os.mkdir(self.modelpath+"/"+m)
        except:
          pass

      #self.submodels=dict([( m[0], (type(m[1][0])==type(GenericModel)) and m[1][0](m[0],self.datatype(self._datatype),modelpath=self.modelpath+"/"+m) or m[1][0](m[0],modelpath=self.modelpath+"/"+m) ) for m in self.submodels.items() ] )
      #self.submodels=dict([( m[0], (issubclass(m[1],GenericModel)) and m[1](m[0],self.datatype(self._datatype),modelpath=self.modelpath+"/"+m[0]) 
      #                                                               or m[1](m[0],self.datatype(self._datatype),modelpath=self.modelpath+"/"+m[0]) )
      #                      for m in self.submodels.items() ] )
      #for m in self.submodels.items() :
           #print type(m[1])
           #print m
#      self.submodels=dict([( m[0], (((m[1][0](m[0],self.datatype(self._datatype),modelpath=self.modelpath+"/"+m[0]) ,self.structures[m[1][1]] )
#                                           if hasattr(m[1][0],"__call___") else ((m[1][0],"DIRECT"),self.structures[m[1][1]] )
#                                                                    )    if m[1][1]!=None else None) ) for m in self.submodels.items() ] )



      tstruct=[]
      print "INSTANTIATING STRUCTURES"
      for m in self.structures.items():
           print "cname",self.cname
           print "structure",m[0]
           if not self.dicargs.has_key(self.cname+m[0]+"/"):
              self.dicargs[self.cname+m[0]+"/"]=([],{})
           if (type(m[1])!=tuple):
              if (type(m[1]) in [ type(GenericModel),type(class___) ] ):
                 tstruct.append((m[0],  m[1](*(self.dicargs[self.cname+m[0]+"/"][0]),**(self.dicargs[self.cname+m[0]+"/"][1]))))
              else:
                 tstruct.append((m[0],  m[1]))
           else:   
              if (type(m[1][0]) in [ type(GenericModel),type(class___) ] ):
                  tstruct.append((m[0],  (m[1][0](*(self.dicargs[self.cname+m[0]+"/"][0]),**(self.dicargs[self.cname+m[0]+"/"][1])),m[1][1])))
              else:
                 tstruct.append((m[0],  m[1]))
      print "tstruct=",tstruct
      self.structures=dict(tstruct) 


      print "INSTANTIATING SUBMDELS"      
      for m in self.submodels.items():
         print m[0], ":" , m[1]
      rd={}
      for m in self.submodels.items():
         #print "+++++" ,m
         if hasattr(m[1][0],"__call__"):
            if (m[1][1]!=None):
               ## we are bound to a structure
               ## get the datatype according to the structure...
               print m
               if (m[1][1]==tuple):
                  assert(False) # not yet implemented
               else:
                  print "M11",m[1][1]
                  if (type(m[1][1][1])==str):
                    if ((m[1][1][0])==1):
                       od=self.datatype(self._datatype)
                       dtx=self.datatype(od.get_typerelated_structures()[m[1][1][1]])
                       print "dtx",dtx
                       if (type(dtx)!=tuple):
                         dtp= dtx.output_datatype(od)
                       else:
                         pycvf_warning("Using buggy implementation, we need either to specify type of cliques either to suggest a third implementation")
                         dtp= dtx[0].output_datatype(od)
                         #assert(False)
                    else:
                      raise Exception, "Not Yet Implemented"
                  mdl=m[1][0](m[0],dtp,modelpath=self.modelpath+"/"+m[0])
            else:
               mdl=m[1][0](m[0],self.datatype(self._datatype),modelpath=self.modelpath+"/"+m[0])
         else:
            print "OVNI", self.cname, m, self.dicargs.keys()
            mdl=m[1][0]
         if m[1][1]!=None:
            if m[1][1][0]==1:
               print "linking to structure", m[1][1][1], self.structures[m[1][1][1]], type(self.structures[m[1][1][1]])
               rd[m[0]]=(mdl,self.structures[m[1][1][1]])
            else:
               raise Exception, "Not yet implemented"
         else:
            rd[m[0]]=(mdl,None)
      self.submodels=rd
      print self.submodels
      
      
      for m in self.statmodels.keys():
        try:
          os.mkdir(self.modelpath+"/"+m)
        except:
          pass     
      #print self.statmodels
      #print self.dicargs[self.cname+m[0]+"/"]
      #self.statmodels=dict([(m[0],  m[1][0](*m[1][1],**dict(m[1][2].items()+[ ('modelpath',self.modelpath+"/"+m)]) ) ) for m in self.statmodels.items() ] )
      try:
        self.statmodels=dict([(m[0],  CachedModel(m[1], lambda : m[1](*(self.dicargs[self.cname+m[0]+"/"][0]),**(self.dicargs[self.cname+m[0]+"/"][1])), self.modelpath+"/"+m[0]+"/lowlevel") )  for m in self.statmodels.items() ] )
      except KeyError:
         sys.stderr.write("#*#*#* warning some statmodels may not have been constructued")
         pass



  def substructure_init(self):
      #print self,self.submodels
      for m in self.submodels.items():
         #print m#.name
         #time.sleep(1)
         print m[1][0]
         m[1][0].recinit(self.dicargs,self.cname+m[0]+"/")
      #for m in self.statmodels.keys():
      #   m.init(argdict)


  def __del__(self):
     pass
   ##
   ## Les parametres sont precises
   ## 

  def recinit(self,dicargs,cname):
      """
       Thsi function is called to recursively instantantiate all the modules with the appropriate arguments
      """
      if (self.cname==None):
        print "setting cname", cname
        self.cname=cname
        self.dicargs=dicargs
        if (dicargs.has_key(cname)):
          self.init(*dicargs[cname][0],**dicargs[cname][1])
        else:
          sys.stderr.write( "No option option for "+ cname + " among "+str(dicargs.keys()) + "\n")
          self.init()
       
  def init(self,*args, **kwargs):
      ###
      ### we instantiate submodels and statmodels...
      ### et ont leur passe leur parametres...
      ###
      ##
      ## We shall have first have called our own init
      ## 
      self.substructure_construct()
      self.substructure_init()
      ## 
      self.metas=self.get_features_meta(self._datatype)
      for m in self.metas:
         for i in m[0][1].items():
            self.context[i[0]]=i[1]
      self.cnames=self.get_cnames()
      self.cnames_models=dict(self.get_cnames_models())
      self.ready=True
  

  def test_fusion(self,l):
     return scipy.mean(l)

  def test(self,datas, output_f=None,log=False,with_processing=True,pd0=None):
     lr=[]
     if with_processing:
        #sys.stderr.write("\n....PROCESSING DATA\n")
        pd=self.process_multiple_alt(datas)
        pd0=pd
        #sys.stderr.write("\n..../PROCESSING DATA\n")
     else: 
        pd=datas
     rstat=[]
     for m in self.submodels.items():
         #print "~~~~ testing s ",m,"~~~~~~~"
         if ((m[1][1])==None):
              #sys.stderr.write("\n....testing sm  "+repr(m[1])+"..on.."+repr(pd[1])+"\n")
              trstat=m[1][0].test(self.features_for(m[1][0],pd0), log=log,with_processing=False, pd0=pd0)
              rstat.append(trstat)
         else:
              #print "....testing sm sf  ",m[1],"..on..",pd[0][0]
              #sf=m[1][1].extract_all(self.features_for(m,pd0))               
              feat=self.features_for(m,pd[0][0])
              print feat
              sf=m[1][1].extract_all(feat)
              if (len(ffor) and fs[0]!=NotReady):
                 rstat.append(m[1][0].test(sf,with_processing=False,pd0=pd0))
              else:
                 sys.stderr.write("Object is still not ready !!!", len(ffor))
           #print "pd=",pd
           #print "pdh=",self.features_for(m[1][0],pd)
           #print m[1]
           #ffor=filter((lambda x:(x!=None) and (x[0]!=None)),self.features_for(m[1][0],pd))
           #if (len(ffor) and ffor[0]!=NotReady):
           #   rstat.append(m[1][0].test(ffor),with_processing=False)
           #else: 
           #   sys.stderr.write("Object is still not ready !!!", len(ffor))
         #else:
          # raise Exception,"Not Yet Implemented"
     rs=[]
     for m in self.statmodels.items():
           # TODO it can be nice to have a LS primitive !
           #print "~~~~ testing l ",m,"~~~~~~~"
           if (self.instantiated_datatype) and (self.instantiated_datatype.get_default_structure()):
              s=self.structures[self.instantiated_datatype.get_default_structure()]
              ## TODO ; MEANF is to be generic
              #meanf=scipy.mean
              def meanf(x):
                try:
                    return scipy.mean(x)
                except:
                    return x
              print pd[0][0]
              rs.append( meanf( self.extract_structure(pd[0],s,lambda x:m[1].test(x,log=log)) ) )
           else:
              rs.append(m[1].test(pd[0],log=log))
     #print "rs",rs
     #print "rstat", rstat
     if (output_f):
         output_f(rs,rstat)   
     return .5*self.test_fusion(rs)+.5* self.test_fusion(rstat)
    
  def features_for(self,model,pd):
    #for m in self.metas:
    #  print "* ", m, "OK"
    #sys.stdout.flush()
    #print pd
    #print "len pd",len(pd)
    #self.print_tree()
    return reduce(lambda b,x: b + ([pd[x]] if (self.metas[x][2]==model) else  []) , range(len(self.metas)), [])
    
  def train(self,datas, with_processing=True,pd0=None):
     """
       This is the function to be call to train all possible models given a set of observations...
       It will work compute all the features at once and then call all the submodels so that they broadcast result to stat models and structures ...
     """
     if with_processing:
       pd=self.process_multiple_alt(datas)
       pd0=pd
     else:
       pd=datas

     for m in self.submodels.items():             
           if ((m[1][1])==None):
              m[1][0].train(self.features_for(m[1][0],pd), with_processing=False)
           else:
              # extraction is always done from the first track.
              #TODO we have to do actually for all the elements in the query
              sf=m[1][1].extract_all(pd[0][0])
              ### EXTRACT_ALL MAY RETURN ANY TYPE OF DATA HERE
              m[1][0].train(sf)
     

     #########################################################################################
     ## FOR DEBUGGING PURPORSES
     #########################################################################################
     if with_processing:
       pd=self.process_multiple_alt_unimeta(datas)
       pd0=pd
       print len(pd0)
     else:
       pd=datas


     for m in self.statmodels.items():
           # TODO it can be nice to have a LS primitive !
           if (self.instantiated_datatype) and (self.instantiated_datatype.get_default_structure()):
              s=self.structures[self.instantiated_datatype.get_default_structure()]
              if ((type(pd)==numpy.ndarray) or ((pd!=NotReady)) and (pd!=[None])):  ## Do nothing when notready
                 print "INFO TRAIN=",s, datas.shape,pd[0].shape
                 self.extract_structure(pd,s,lambda x:m[1].train(x,online=True))
           else:
              if (pd!=NotReady):
                 assert(type(pd)==numpy.ndarray)
                 assert(pd.ndim==2)
                 m[1].train(pd,online=True)
              else:
                 pycvf_warning("model not completetly ready")






  def internal_train(self,processed_datas):
     pd=processed_data
     #for s in self.structures.items():
     #      s[1].train(pd[0])

     for m in self.submodels.items():
           m[1][0].train(self.features_for(m,pd))


     for m in self.statmodels.items():
           # TODO it can be nice to have a LS primitive !
           if (pd[0]!=NotReady):
             if (self.instantiated_datatype) and (self.instantiated_datatype.get_default_structure()):
               s=self.structures[self.instantiated_datatype.get_default_structure()]
               self.extract_structure(pd[0],s,lambda x:m[1].train(x,online=True))
             else:
               print "....training",m[1],"..on..",pd[0]   
               m[1].train(pd[0],online=True)

  #     for m in self.statmodels.items():
  #           m[1].train(pd[0],online=True)

  ##############################################################################################################################################################################
  ##############################################################################################################################################################################
  ##############################################################################################################################################################################


  def process(self,element,processf=None,metas=None):
        """
          Do process one element (apply feature filters)
        """
        if (not processf):
          processf=lambda x:x
        if metas==None:
          metas=self.metas
        self.context['src']=element
        cacheable_object=CacheableObject(element,transform_catalog=SimpleEvaluatorTransformCatalog(self.xeval))
        self.context['thesrc']=cacheable_object ## allow complex observers...
        r=[]
        for o in metas:
             try:
               r.append(cacheable_object[o[0][0]])
             except NotReady:
               r.append(NotReady)
        return processf(r)

  def get_default_structure(self):
     return self.datatype(self._datatype).get_typerelated_structures()[ self.datatype(self._datatype).get_default_structure()]

  def print_tree(self,  indent="",stream=sys.stdout):
     stream.write("*: "+self.cname+"\n")
     stream.write(indent+ "|  (submodels keys="+str(self.submodels.keys())+")\n")
     stream.write(indent+ "|  (structures keys="+str(self.structures.keys())+")\n")
     stream.write(indent+ "|  (structures items="+str(self.structures.items())+")\n")     
     stream.write(indent+ "|  (statmodel keys="+str(self.statmodels.keys())+")\n")
     stream.write(indent+"|\n")
     lsm=len(self.submodels)
     submodelsi=self.submodels.items()
     for smi in range(lsm):
        sm= submodelsi[smi]
        stream.write(indent+"+-")
        sm[1][0].print_tree(indent=indent+(((smi+1)<lsm) and "| " or "  "),stream=stream)
        stream.write(indent+"\n")
        if (smi+1!=lsm):
          stream.write(indent+"\n")
     lsm=len(self.statmodels)
     statmodelsi=self.statmodels.items()
     for smi in range(lsm):
        sm= statmodelsi[smi]
        stream.write(indent+"+-"+sm[0]+"\n")
        if (smi+1!=lsm):
          stream.write(indent+"\n")
     stream.write(indent+"\n")

  def extract_structure(self,element,structure,processf=None, recmode=False, elementaddress=NoAddress):
        """
          Extract elements from specified stucture

          ###
          ### EXTRACT STRUCTURE SHOULD BE APPLIED ELEMENT BY ELEMENT AND RETURNS AN ITERABLE OF ELEMENTS
          ### 


          Extract structure returns AN ITERATOR or AN ARRAY of all the elements of the input element
          

          2 variants may be implemented there
        """
        if (not processf):
          processf=lambda x:x
        #print structure()
        #print "element..",element
        if (type(structure)==tuple):
          #sys.stderr.write(str(structure[1])+"\n")
          #print "element :",element.shape, type(element)
          #if  True:
          #  element=numpy.vstack(element)
          if (recmode=="*"):
             r=structure[0].cliques_extract_all_rec(element,structure[1][0],*structure[1][1])
          elif (recmode=="@"):
             r=map(lambda x:(elementaddress,x),
                    structure[0].cliques_addresses(element,structure[1][0],*structure[1][1])
                )
          else:
             r=structure[0].cliques_extract_all(element,structure[1][0],*structure[1][1])
          #print r
          #sys.stderr.write("rshape="+str(r.shape)+"\n")
          return processf(r)
        else:
          return processf(structure.extract_all(element))

  def _process_multiple(self,elements,processf=None):
        if (not processf):
          processf=lambda x:x
        res=[]
        for element in elements:
          self.context['src']=element
          cacheable_object=CacheableObject(element,transform_catalog=SimpleEvaluatorTransformCatalog(self.xeval))
          self.context['thesrc']=cacheable_object ## allow complex observers...
          r=map(lambda o:cacheable_object[o[0][0]],self.metas)
          res.append(processf(r))
        return res 
    

  def get_object_by_cpath(self,cpath, cpathl=None):     
     print self.cnames_models
     return  self.cnames_models[cpath]
     #if ((cpath=="//") or (cpathl==[])):
     #   return self
     #if (type(cpath==None)):
     #  if (cpath[:2]=='//')
     #     cpath=cpath[2:]
     #  cpathl=cpath.split("/")
     #
     #print self.cnames
     #for x in self.submodels():
        
        
  def get_metas_by_query(self,x):       
       try:
         o=self.get_object_by_cpath("/".join(x.split('/')[:3])+"/")
       except KeyError:
         pycvf_warning("unable to find your submodel : "+ str( x))
         print "candidates are "+str(self.submodels.keys())
         raise
       return filter(lambda x:x[3]==o,self.metas)

  def get_metas_by_query_a(self,x):       
       #o=self.get_object_by_cpath("/".join(x.split('/'))+"/")
       try:
         o=self.submodels[x][0]
       except KeyError:
         pycvf_warning("unable to find your submodel : "+ str( x))
         print "candidates are "+str(self.submodels.keys())
         raise
       print o, self.metas
       r =filter(lambda x:x[3]==o,self.metas)
       print r
       return r





  #print "TEL",type(telements)
  ####
  #### FIRTS LEVEL : NO STRUCTURE DECOMPOSITION TO BE APPLIED
  ####
  ##print self.metas
  ##print l[0]
  #if (len(l)>1):
  #   telements=self.process_multiple_alt_unimeta(telements,metas=self.get_metas_by_query(l[0]) )
  #   cmodel=self.get_object_by_cpath("/".join(l[0].split('/'))+"/")

  #print "TEL",type(telements)
  ####
  #### INTERMEDIATES LEVEL : APPLY AND CONTINUE PROCESS
  ####
  #if (len(l)>2):
  #  for x in l[1:-1]:
  #     self.extract_structure(x)
  #     telements=self.process_multiple_alt_unimeta(telements,metas= self.get_metas_by_query(x) )
          

  def process_path(self,elements,eaddress,cpath,funcname,return_all=False):
        """ 
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
        #print "PROCESS PATH"
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
            print "filtb=",filtb
            print self.submodels
            #print telements
            telements=self.process_multiple_alt_unimeta(telements,metas= self.get_metas_by_query(filtb))

        ###
        ### DO STRUCTURE DECOMPOSITION AND RECURSION
        ###
        if (len(l) > 1):
          filt=l[1].split('/')
          filta=filt[0]
          if (filta[-1]=='*'):
            recmode="*"
            filta=filta[:-1]
          elif (filta[-1]=='@'):
            recmode="@"
            filta=filta[:-1]
          else:
            recmode=False   
          filtb="/"+"/".join(l[-1].split("/")[1:])        
          if (len(l)>1):
             print "available structures=", cmodel.structures.keys(), "len",len(l),l
             try:
               taddresses=reduce (lambda x,y: x+y,
                  [ self.extract_structure(e,cmodel.structures[filta],lambda x:x,"@", eaddress) for e in telements ],
                  []
                )
               telements=reduce (lambda x,y: x+y,
                 [ self.extract_structure(e,cmodel.structures[filta],lambda x:x,recmode, eaddress) for e in telements],
                 []
                )
             except:
               taddresses=iconcatiter(lambda e: self.extract_structure(e,cmodel.structures[filta],lambda x:x,"@", eaddress) ,telements )
               telements=iconcatiter(lambda e: self.extract_structure(e,cmodel.structures[filta],lambda x:x,recmode, eaddress) , telements)
             #print telements
             #sys.stdin.readline()
             print cmodel.structures[filta]
             print self.submodels.values()
             print filter(lambda x:x[1]==cmodel.structures[filta],self.submodels.values())
             cmodel=filter(lambda x:x[1]==cmodel.structures[filta],self.submodels.values())[0][0]
             print cmodel
             print "RESELEMS=", telements
             for x in telements:
                    print x
             
             return map(funcname,[ cmodel.process_path([e[0]],[e[1]],  '#'.join(['/'.join(filt[1:])]+l[2:]), lambda x:x, return_all) for e in zip(telements,taddresses) ])
             #assert(False)           
          ###
          #print telements
        if return_all:
          return funcname(telements), teaddresses, cmodel
        else:
          return funcname(telements)
        
  def process_all_path(self,elements,eaddress,cpath,funcname,return_all=False):
     # compute all the pathes and return results as a dictionary
    assert(False)

  def process_multiple(self,elements,processf=None,metas=None):
        """
           (within a specified model)
           Compute all the features for all the elements
        
           if meta = None then the default set of feature is used, else specified set of feature is used
   
           returns a table with element per row
        """
        if (not processf):
          processf=lambda x:x
        if metas==None:
          metas=self.metas
        res=[]
        for element in elements:
          self.context['src']=element
          cacheable_object=CacheableObject(element,transform_catalog=SimpleEvaluatorTransformCatalog(self.xeval))
          self.context['thesrc']=cacheable_object ## allow complex observers...
          r=[]
          for o in metas:
             try:
               r.append(cacheable_object[o[0][0]])
             except NotReady:
               r.append(NotReady)
          res.append(r)
        return processf(res)

  def process_multiple_tbl(self,elements,metas=None):
        """
           (within a specified model)
           Compute all the features for all the elements
        
           if meta = None then the default set of feature is used, else specified set of feature is used
   
           returns an array with one element per row
           TODO : provide optimized computations
        """
        if (not processf):
          processf=lambda x:x
        if metas==None:
          metas=self.metas
        lmetas=len(metas)
        r=numpy.zeros((lmetas,len(elements)),dtype=object)
        for e in range(len(lements)):
          self.context['src']=elements[e]
          cacheable_object=CacheableObject(element,transform_catalog=SimpleEvaluatorTransformCatalog(self.xeval))
          self.context['thesrc']=cacheable_object ## allow complex observers...
          for i in range(lmetas):
             try:
               r[e,i].append(cacheable_object[o[0][0]])
             except NotReady:
               r[e,i].append(NotReady)
        return r



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
        lmetas=len(metas)        
        le=len(elements)
        assert(lmetas==1)
        r=[]
        li=iter(elements)
        for e in range(le):
          self.context['src']=li.next()
          cacheable_object=CacheableObject(elements[e],transform_catalog=SimpleEvaluatorTransformCatalog(self.xeval))
          self.context['thesrc']=cacheable_object ## allow complex observers...
          try:
               r.append(cacheable_object[metas[0][0][0]])
          except NotReady:
               r.append(NotReady)
        return r




  def process_multiple_alt(self,elements,metas=None):
        """
           Compute all the features for all the elements
        
           if meta = None then the default set of feature is used, else specified set of feature is used
   
           returns a table with one feature per row, (suitable in case where processing is later applied hierarchically)
           TODO : provide optimized computations
        """
        print self
        if metas==None:
          metas=self.metas
        lmetas=len(metas)        
        le=len(elements)
        r=numpy.zeros((lmetas,le),dtype=object)
        li=iter(elements)
        for e in range(le):
          self.context['src']=li.next()
          cacheable_object=CacheableObject(elements[e],transform_catalog=SimpleEvaluatorTransformCatalog(self.xeval))
          self.context['thesrc']=cacheable_object ## allow complex observers...
          for i in range(lmetas):
             try:
               #print metas[i][0][0]
               r[i,e]=cacheable_object[metas[i][0][0]]
             except NotReady:
               r[i,e]=NotReady
        return r



  ##############################################################################################################################################################################
  ##############################################################################################################################################################################
  ##############################################################################################################################################################################
       
  def init_structures(self):
     it=self.input_datatype(self._datatype)
     s=it.get_structures()
     for x in s.items():
        self.structures[x[0]]=x[1]
  
  def xeval(self,s,xobject):
        return eval(s,self.context,{'xobject':xobject})

  def xeval_s(self,s,xobject):
        try :
          return eval(s,self.context,{'xobject':xobject})
        except Exception, e:
          print "Error while evalutation sub expression"
          print e
          print "s",s
          #print "xobject",xobject
          if (hasattr(sys,"last_traceback")):
               traceback.print_tb(sys.last_traceback)
          else:
               traceback.print_tb(sys.exc_traceback)
          #sys.exit(-1)
          assert(False)

  def __del__(self):
     self.save()

  def save(self):
      sys.stderr.write( "saving model "+str(self) )
      sys.stderr.write( "\n")
      for s in self.structures.items():
          try:
             sys.stderr.write( "saving model structure "+str(s) )
             s[1].save()
          except:
              sys.stderr.write( "FAILED")
              pass
          sys.stderr.write( "\n")
      for f in self.submodels.items():
          try:
              sys.stderr.write( "saving model submodels "+str(f) )
              f[1][0].save()
          except:
              sys.stderr.write( "FAILED")
              pass
          sys.stderr.write( "\n")
      for s in self.statmodels.items():
          try:
              sys.stderr.write( "saving model statmodels "+str(s) )
              s[1].save()
          except Exception,e:
              sys.stderr.write( "FAILED"+str(e))
              pass
          sys.stderr.write( "\n")         
  def join_meta(self,othermodel,datatype):
      if (othermodel[1]==None):
         return map(lambda x:((re.subn( "src" , self.featurefilter and self.featurefilter[0] or "src",x[0][0])[0],
                              x[0][1],
                              x[0][2]),
                              x[1],
                              othermodel[0],
                              x[3]), 
                    othermodel[0].get_features_meta(self.datatype(datatype))
                )
      else:
         #print "WARNING INVALID DATATYPE HERE TO BE UPDATED"
         #
         # (apriori) Datas do not have to be shared processed in structures...
         # although... can be useful... but it has to implemented cleanly....
         #
         return []#map(lambda x:((re.subn( "src" , self.featurefilter and self.featurefilter[0] or "src",x[0][0])[0],x[0][1],x[0][2]),x[1],x[2]), 
                  #  othermodel[0].get_features_meta(self.datatype(datatype))
                  # )

  def get_features_meta(self,datatype):
    r=[]
    if (self.featurefilter):
      r+=[ (self.featurefilter,self.datatype(datatype), self, self) ] 
    #print "SV",self.submodels.values()
    r+=reduce(lambda x,y:x+self.join_meta(y,datatype),self.submodels.values(),[])
    #print "/SV",self.submodels.values()
    return r

  def get_cnames(self):
    r=[]
    if (self.cname):
      r+=[ self.cname] # basecname+self.cname+"/" ] 
      r+=map(lambda x:self.cname+"#"+x,self.structures.keys())
    r+=reduce(lambda x,y:x+ y[0].get_cnames(),self.submodels.values(),[])
    return r

  def get_cnames_models(self):
    r=[]
    if (self.cname):
      r+=[ (self.cname,self)] # basecname+self.cname+"/" ] 
    r+=reduce(lambda x,y:x+ y[0].get_cnames_models(),self.submodels.values(),[])
    return r


  def get_by_cname(self,cname):
     return self.cnames_models[cname]
     

  def init_featurefilter(self, *args, **kwargs):
     pass       

  def init_submodels(self, *args, **kwargs):
     pass       

  def init_statmodels(self, *args, **kwargs):
     pass       


  def init_structures(self, *args, **kwargs):
     pass       

  @staticmethod 
  def load(basepath):
      assert(0)

  def __mult__(self,s):
     assert(type(s)==dict)
     for i in s.keys():
       self.structures[i[0]]=i[1]

  def extend_structures(self,s):
     assert(type(s)==dict)
     for i in s.items():
       self.structures[i[0]]=i[1]


  def __minus__(self,s):
     assert(type(s)==dict)
     for i in s.keys():
       self.statmodels[i[0]]=i[1]


  def extend_statmodels(self,s):
     assert(type(s)==dict)
     for i in s.items():
       self.statmodels[i[0]]=i[1]

  def __or__(self,s):
     assert(type(s)==dict)
     for i in s.keys():
       self.submodels[i[0]]=i[1]

  def extend_submodels(self,s):
     assert(type(s)==dict)
     for i in s.items():
       self.submodels[i[0]]=i[1]


  def savemodels(self):
     for x in self.submodels:
        x.save()




  