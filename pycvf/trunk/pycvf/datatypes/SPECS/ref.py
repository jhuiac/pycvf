# -*- coding: utf-8 -*-
##
## A datatype is an abstact object, use when wanting to do IO with user about some python object.
## 

##
## Datatypes are classes
##

class Datatype:
  @classmethod
  def display(x):
       """ (mandatory) You must provide, one function that render an object 'X' to the user / here there is no control for the program on the way x is rendered/ displayed ... """
        pass

  @classmethod
  def get_display(displayname='',*args,**kwargs):
        """ (suggestion : new version), as some plugin may want their own window, it may good to provide a way to have many 'display' """

  @classmethod
  def get_widget():
        """ returns an handle on the widget used for representing the object in a compound user interface """
        pass
  
  @classmethod      
  def plot_pylab():
        """ renders the data using pylab """        
        pass

  @classmethod
  def get_typerelated_structures(cls):
        ##
        ## returns a list of quickly accessible structure for that datatype
        ## 
        return {"datas": spatial.ImageStructure(0), 
                #...
               }
  @classmethod
  def get_default_structure(cls):
       ## return the name of the default structure
       return "datas"
  