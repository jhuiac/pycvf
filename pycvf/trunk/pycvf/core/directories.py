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
## This files setup the default directories for the JFLI Python Computer Vision's Framework
## 

try:
  from termcolor import colored
except:
  pass

import os

PYCVF_STATICDATA=os.path.join(os.path.dirname(__file__),"..","..","datas")

PYCVF_ROOT=os.environ.get("PYCVF_ROOT", os.environ["HOME"]+ "/pycvf-datas")
PYCVF_DATABASE_DIR=os.environ.get("PYCVF_DATABASE_DIR",PYCVF_ROOT+"/databases")
PYCVF_INDEX_DIR=os.environ.get("PYCVF_INDEX_DIR",PYCVF_ROOT+"/indexes")
PYCVF_MODEL_DIR=os.environ.get("PYCVF_MODEL_DIR",PYCVF_ROOT+"/models")
PYCVF_HLMODEL_DIR=os.environ.get("PYCVF_HLMODEL_DIR",PYCVF_ROOT+"/HLmodels")
PYCVF_WEIGHT_DIR=os.environ.get("PYCVF_WEIGHT_DIR",PYCVF_ROOT+"/weights")
PYCVF_CACHE_DIR=os.environ.get("PYCVF_CACHE_DIR",PYCVF_ROOT+"/cache")
PYCVF_LOG_DIR=os.environ.get("PYCVF_LOG_DIR",PYCVF_ROOT+"/log")
PYCVF_PROJECTS_DIR=os.environ.get("PYCVF_PROJECTS_DIR",PYCVF_ROOT+"/project")

for d in [ PYCVF_ROOT, PYCVF_DATABASE_DIR, PYCVF_INDEX_DIR, PYCVF_MODEL_DIR, PYCVF_WEIGHT_DIR, PYCVF_CACHE_DIR, PYCVF_LOG_DIR, PYCVF_PROJECTS_DIR ]:
  try:
    os.stat(d)
  except:
    try:
      os.mkdir(d)
    except:
       import sys
       sys.stderr.write("Failed to access/create necessary framework directory : '"+d+"'\n")
       sys.exit(-1)
  