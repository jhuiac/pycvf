# -*- coding: utf-8 -*-
##
## This is aimed at helping the distribution of PyCVF by clarifying the legal terms,
## and by making explicit warning when user is using some software comp

from pycvf.core.errors import *


PYCVFD_REQUIRE_PACKAGE=0
PYCVFD_SPECIFIC_LICENSE=1
PYCVFD_SPECIFIC_ACCEPT_REQUIRED=2
PYCVFD_MODULE_STATUS=3

PYCVFD_STATUS_PRODUCTION=0
PYCVFD_STATUS_BETA=1
PYCVFD_STATUS_EXPERIMENTAL=2
PYCVFD_STATUS_BUGGY=3

PYCVF_STATUS_DICT={
  PYCVFD_STATUS_PRODUCTION:"Production",
  PYCVFD_STATUS_BETA:"Beta",
  PYCVFD_STATUS_EXPERIMENTAL:"Experimental",
  PYCVFD_STATUS_BUGGY:"Buggy"
}


def pycvf_dist(pragma, value):
   
    if (pragma==PYCVFD_REQUIRE_PACKAGE):
        try:
            __import__(value,fromlist=value.split(".")[-1])
        except:
            pycvf_error("The following package is required : %s "%(value,))            
    if (pragma==PYCVFD_SPECIFIC_LICENSE):
            pycvf_warning("Please note that you are using a non LGPL module : %s"%(value,))        
    elif (pragma==PYCVFD_SPECIFIC_ACCEPT_REQUIRED):        
            pycvf_error("Before to use this file you must accept its license")
    elif (pragma==PYCVFD_MODULE_STATUS):        
            from pycvf.core.settings import PYCVF_STABILITY_LEVEL:
            if (value>PYCVF_STABILITY_LEVEL):
              pycvf_warning("You are using a package that have the status : %s" %(PYCVF_STATUS_DICT[value],))            
    pass

