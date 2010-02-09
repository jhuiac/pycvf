# -*- coding: utf-8 -*-
from pycvf.lib.info.options import *
from pycvf.core import settings
from pycvf.core import builders
from pycvf.core.errors import *
from pycvf.core.genericmodel import STATUS_READY, NotReady,STATUS_NOT_READY,STATUS_ERROR
from pycvf.core import settings
from pycvf.core import directories

import datetime,os,sys,stat
import re, os, math, random, time,sys, traceback, getopt,itertools,gc

def setprocname(name):
    try:
      import ctypes
      libc = ctypes.CDLL('libc.so.6')
      libc.prctl(15, name, 0, 0, 0)
    except:
      pass


def namerecode(s): 
        r=""
        for c in s:
          r+=(c if c.isalnum() else "%%%02d"%(ord(c)))
        return r


class GenericApplication(object):
  class ProgramMetadata(object):
      name="PyCvF Application"
      version="0.1"
      author="Bertrand Nouvel bertrand.nouvel@gmail.com"
      copyright="        COPYRIGHT Bertrand Nouvel - JFLI - CNRS 2009"

  
  help_option=CmdLineOption('h','help',None,'Displays this help message and exit',print_help_and_exit)
  debugger_option=CmdLineString('D','debugger',"bool",'Runs in debugger',"0")
  profiler_option=CmdLineString(None,'profiler',"filename",'Runs in debugger',"")  

  @classmethod  
  def prepare_process(cls, *args, **kwargs):
    pass

  @classmethod  
  def finish(cls, *args, **kwargs):
    pass

  @classmethod  
  def run(cls,cmdlineargs, *args,**kwargs):
     #print cls
     cls._options=filter(lambda x:isinstance(x,CmdLineOption), map(lambda x:eval("cls."+x,{'cls':cls}),dir(cls)))
     do_parse_options(cls.ProgramMetadata,cls._options)
     setprocname(sys.argv[0].split('/')[-1])
     if (int(cls.debugger_option.value)):
       if (int(cls.debugger_option.value)==1):
         import pdb
         try:
           pdb.run("cls.prepare_process()",globals(),{'cls':cls})
           pdb.run("cls.process()",globals(),{'cls':cls})
           pdb.run("cls.finish()",globals(),{'cls':cls})
         except:
           pdb.post_mortem(sys.exc_info()[2])
       elif (len(cls.profiler_option)):
           import cProfile
           cProfile.run("cls.prepare_process()",cls.profiler_option+"-prepare")
           cProfile.run("cls.process()",cls.profiler_option+"-process")           
           cProfile.run("cls.finish()",cls.profiler_option+"-finish")           
       else:
          cls.prepare_process()
          sys.call_tracing(lambda :cls.process(),[])
          cls.finish()
     else:
       cls.prepare_process()
       cls.process()
       cls.finish()       

  @classmethod
  def process(cls,*args,**kwargs):
     nq=int(number_query.value)
     for e in vdb:
       print mdl.process(e[0],processf=lambda x:idx.query([x],nq)) 


def x__dbhelp(cls):
    try:
       exec("from "+ cls.database.value +" import *")
    except:
       exec("from pycvf.databases."+ cls.database.value +" import *")    
    import inspect
    print DB.__doc__
    print "--------------------------"
    print inspect.getargspec(DB.__init__)
    print "--------------------------"
    try:
       print ContentsDatabase.labels()
    except:
       print "This database is not a labeled database or is not able to provide you any information on its label if not instantiated."
    sys.exit(-1)

def dblist():
     print "Global databases :"
     for x in globals().values():
        try:
          if issubclass(x,pycvf.core.database.ContentsDatabase):
             print "*  ", x
        except:
          pass
     dbl=settings.PYCVF_DATABASE_PATH.split(':')
     for p in dbl:
        print "Databases that are accessible from standard path %s:"%(p,)
        if (p):
          for x in os.listdir(builders.pycvf_builder(p[:-1]).__path__[0]):
            if (x[-3:]==".py") and (x!="__init__.py"):
              print "*  ",x[:-3]
            elif ("." not in x):
              dj=os.path.join(builders.pycvf_builder(p[:-1]).__path__[0],x)
              if (stat.S_ISDIR(os.stat(dj)[0])):
                try:
                  os.stat(os.path.join(dj,"__init__.py"))
                  builders.load_force(p+x)                  
                  dbl.append(p+x+".")
                except OSError:
                  pass
     sys.exit(0) 
    

class DatabaseUsingApplication(GenericApplication):   
  database=CmdLineString(None,"db","database","set the database to be read",settings.DEFAULT_DATABASE)
  #databaseargs=CmdLineString(None,"dbargs","database_arguments","set database options",settings.DEFAULT_DATABASE_ARGS) 
  dbhelp_option=CmdLineOption(None,"dbhelp",None,"show info on parameters required by the database",lambda :x__dbhelp(DatabaseUsingApplication))    

  list_databases=CmdLineOption(None,'dblist',None,'List databases in current context',dblist) 

  @classmethod
  def prepare_process(cls, *args, **kwargs):
     #try:
     #   exec("from "+ cls.database.value +" import ContentsDatabase")
     #except:
     #   exec("from pycvf.databases."+ cls.database.value +" import ContentsDatabase")    
     #cls.ContentsDatabase=ContentsDatabase
     #if (len(cls.databaseargs.value)):
     #   cls.vdb=ContentsDatabase( **eval('{'+cls.databaseargs.value+'}'))
     #else:
     #   cls.vdb=ContentsDatabase()      
     cls.vdb=builders.database_builder(cls.database.value)



def x__modelhelp(cls):
    try :
      exec("from "+ cls.mymodel.value +" import *")
    except ImportError:
      exec("from pycvf.nodes."+ cls.mymodel.value +" import *")
    import inspect
    print inspect.getargspec(Model.__init__)
    sys.exit(-1)


class ModelUsingApplication(DatabaseUsingApplication):   
  frameworkv=CmdLineString(None,"framework_version","frameworkv","version of the framework to be used",settings.DEFAULT_FRAMEWORK)
  mymodel=CmdLineString('m',"model","model","set the model to be used",settings.DEFAULT_MODEL)
  #mymodelargs=CmdLineString(None,"modelargs","model_arguments","set model options",settings.DEFAULT_MODEL_ARGS) 
  session=CmdLineString('s',"session",'name_of_session',"name of the session",settings.DEFAULT_SESSION)                             

  @classmethod
  def prepare_process(cls, *args, **kwargs):
     super(ModelUsingApplication,cls).prepare_process(*args,**kwargs)
     pycvf_debug(10,"MODELINIT")         
     cls.mdl=builders.model_builder(cls.mymodel.value)
     cls.mdl.init('/',cls.vdb.datatype(),cls,directory=os.path.join(settings.PYCVF_MODEL_DIR,cls.session.value))
     cls.mdl.metainfo_curdb=cls.vdb
     pycvf_debug(10,"/MODELINIT")
     assert(cls.mdl.get_curdb()==cls.vdb)
     cls.mmeta=cls.mdl.get_features_meta()
     cls.preprocess() 
  
  @classmethod
  def preprocess(cls, *args, **kwqrgs):
      pycvf_debug(2,"PREPROCESS")
      cls.mdl.print_tree()
      cont=True
      # while the model is in a learning stqte (returning NotReady) train the model
      ei=iter(cls.vdb)
      c=0
      while cont:
          try:
              c+=1
              status=cls.mdl.get_status()
              if (status!=STATUS_READY):
                if(status==STATUS_ERROR):
                  raise Exception, "Error State"
                sys.stderr.write("\riter =%d"%(c))
                e=ei.next()
                cls.mdl.process(e[0],addr=e[1])
              else:
                pycvf_debug(10,"STATUS=READY -> LAUNCHING APP")
                cont=False
          except StopIteration:
              pycvf_error("Your database appear to be too small for using this model")
          except NotReady:
              sys.stderr.write("/!\ NOTREADY")
              pass
          except:
              raise
      cls.mdl.metainfo_curaddr=None
      pycvf_debug(2," /PREPROCESS")
  
  @classmethod
  def finish(cls, *args, **kwqrgs):
      pycvf_debug(2,"CLEANUP")
      cls.mdl.destroy()
      del cls.mdl
      del cls.mmeta
      gc.collect()
      pycvf_debug(2,"/CLEANUO")      

  modelhelp_option=CmdLineOption(None,"modelhelp",None,"show info on parameters required by the database",lambda :x__modelhelp(ModelUsingApplication))                             

def x__idxhelp():
    try:
       exec("from "+ indexclass.value +" import *")
    except:
       exec("from pycvf.indexes."+ indexclass.value +" import *")    
    import inspect
    print inspect.getargspec(Indexer.__init__)
    sys.exit(-1)


class IndexUsingApplication(ModelUsingApplication):
  """
   This class is for applications using a single index structure based on a single model and a single single database.
  """
  indexpath=CmdLineString(None,"idxpath","indexpath","directory where are stored the indexes",directories.PYCVF_INDEX_DIR+"/$sessionname/")
  indexclass=CmdLineString(None,"idx","indexclass","set the index structure to be used",settings.DEFAULT_INDEX_CLASS)#"index_vectors")
  #indexargs=CmdLineString(None,"idxargs","index_arguments","set index options","") 
  session=CmdLineString('s',"session",'name_of_session',"name of the session",settings.DEFAULT_SESSION)                             
  indexhelp_option=CmdLineOption(None,"idxhelp",None,"show info on parameters required by the index",x__idxhelp)                             

  @classmethod
  def prepare_process(cls, *args, **kwargs):
     super(IndexUsingApplication,cls).prepare_process(*args,**kwargs)
     #try:
     #    exec("from "+ cls.indexclass.value +" import *")
     #except:
     #    exec("from pycvf.indexes."+ cls.indexclass.value +" import *")   

     cls.idx=builders.index_builder(cls.indexclass.value)
          
     ipv=cls.indexpath.value
     ipv=ipv.replace('$modelname',namerecode(cls.mymodel.value.split('.')[-1]))
     ipv=ipv.replace('$contentname',namerecode(cls.database.value.split('.')[-1]))
     ipv=ipv.replace('$indexname',namerecode(cls.indexclass.value.split('.')[-1]))
     ipv=ipv.replace('$sessionname',namerecode(cls.session.value))
     try:
       os.mkdir(ipv)
     except:
       pass
     cls.index_filename=ipv
     #if (len(cls.indexargs.value)):
     #   cls.idx=indexschema_init(ipv,cls.mdl,(cls.mmeta if not cls.feature_select else cls.feature_select), **eval('{'+cls.indexargs.value+'}'))
     #else:
     #cls.idx.init(ipv,cls.mdl, cls.mmeta)      


  
