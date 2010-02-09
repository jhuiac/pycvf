# -*- coding: utf-8 -*-
from pycvf.core.errors import pycvf_warning
from pycvf.core import settings
from pycvf.core import autoimp


#from autoimp import pycv
autoimp._import_all()
models=autoimp.pycvf.nodes
#models.image
#models.video
#structures=autoimp.pycvf.structures




##
## In framework2 things used to be much more complicated but with autoimp : things are easy as 1,2,3
## 
import sys,autoimp
import cPickle as pickle

def module_context(module):
  r={}
  for x in dir(module):
    r[x]=getattr(module,x) 
  return r

def load_force(_modname,*args,**kwargs):
    f=__import__(_modname,fromlist=_modname.split('.')[:-1])
    if hasattr(f,'__call__'):
       return f.__call__(*args,**kwargs)
    else:
       return f
   
def load_force_ml(_modname,*args,**kwargs):
    _modname="pycvf.stats."+_modname
    f=__import__(_modname,fromlist=_modname.split('.')[:-1])
    if hasattr(f,'__call__'):
       return f.__call__(*args,**kwargs)
    else:
       return f
   
def load_force_node(_modname,*args,**kwargs):
    _modname="pycvf.nodes."+_modname
    return load_force(_modname,*args,**kwargs)

def load_force_database(_modname,*args,**kwargs):
    _modname="pycvf.databases."+_modname
    return load_force(_modname,*args,**kwargs)

def load_force_datatype(_modname,*args,**kwargs):
    _modname="pycvf.datatypes."+_modname
    return load_force(_modname,*args,**kwargs)

def load_force_structure(_modname,*args,**kwargs):
    _modname="pycvf.structures."+_modname
    return load_force(_modname,*args,**kwargs)

def select_open_file():
    import pycvf.lib.ui.qt
    import PyQt4, PyQt4.QtGui
    qfd=PyQt4.QtGui.QFileDialog()
    return unicode(qfd.getOpenFileName()).encode('utf8')


def select_save_file():
    import pycvf.lib.ui.qt
    import PyQt4, PyQt4.QtGui
    qfd=PyQt4.QtGui.QFileDialog()
    return unicode(qfd.getSaveFileName()).encode('utf8')


def select_existing_directory():
    import pycvf.lib.ui.qt
    import PyQt4, PyQt4.QtGui
    qfd=PyQt4.QtGui.QFileDialog()    
    return unicode(qfd.getExistingDirectory()).encode('utf8')

def piped_models(*l):
    l=list(l)[:-1]
    r=l[-1]
    l.reverse()
    for x in l:
        r=x|r
    return r

def add_context_basics(context):
  context["LF"]=load_force
  context["LN"]=load_force_node
  context["DB"]=load_force_database
  context["LD"]=load_force_datatype
  context["LS"]=load_force_structure
  context["ML"]=load_force_ml
  context["PM"]=piped_models  
  context["select_open_file"]=select_open_file
  context["select_save_file"]=select_save_file  
  context["select_existing_file"]=select_open_file  
  context["select_existing_directory"]=select_existing_directory  
  
def database_builder(expr, database_path=settings.PYCVF_DATABASE_PATH):
  #errs=[]
  context=globals().copy()
  context["__all__"]=context.keys()
  add_context_basics(context)
  autoimp.import_all_as_context(context,database_path.split(':'))
  return eval(expr,context)

def database_pickle_loader(filename, database_path=settings.PYCVF_DATABASE_PATH):
  context=globals().copy()
  context["__all__"]=context.keys()
  add_context_basics(context)  
  autoimp.import_all_as_context(context,database_path.split(':'))
  expr="pickle.load(file(filename))"
  return eval(expr,{'filename':filename},context)
  
def model_builder(expr, model_path=settings.PYCVF_MODEL_PATH):
  context=globals().copy()
  context["__all__"]=context.keys()
  add_context_basics(context)  
  autoimp.import_all_as_context(context,model_path.split(':'))
  return eval(expr,context)


def model_pickle_loader(filename, model_path=settings.PYCVF_MODEL_PATH):
  context=globals().copy()
  context["__all__"]=context.keys()
  add_context_basics(context)  
  autoimp.import_all_as_context(context,model_path.split(':'))
  expr="unpickler.load(file(filename))"
  unpickler=pickle.Unpickler(file(filename))
  def myresolve(modulename, name):
      return getattr(eval(modulename,context),name)
  unpickler.find_global=myresolve
  return unpickler.load()
    
def pycvf_builder(expr):
  context=globals().copy()
  context["__all__"]=context.keys()
  add_context_basics(context)    
  autoimp.import_all_as_context(context,settings.PYCVF_MODEL_PATH.split(":")+ settings.PYCVF_DATABASE_PATH.split(":") )
  return eval(expr,context)  

def pycvf_pickle_loader(filename):
  context=globals().copy()
  context["__all__"]=context.keys()
  add_context_basics(context)    
  autoimp.import_all_as_context(context,settings.PYCVF_MODEL_PATH.split(":")+ settings.PYCVF_DATABASE_PATH.split(":") )
  expr="unpickler.load(file(filename))"
  unpickler=pickle.Unpickler(file(filename))
  def myresolve(modulename, name):
      return getattr(eval(modulename,context),name)
  unpickler.find_global=myresolve
  return unpickler.load()


def index_builder(expr, model_path=settings.PYCVF_INDEX_PATH):
  context=globals().copy()
  context["__all__"]=context.keys()
  add_context_basics(context)    
  autoimp.import_all_as_context(context,model_path.split(':'))
  return eval(expr,context)

#def index_builder(expr):
#  if not '(' in expr:
#     expr=expr+"()"
#  try:
#     return eval(expr)
#  except:
#     return eval("pycvf.indexes."+expr)
