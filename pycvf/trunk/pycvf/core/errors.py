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
import sys,logging,logging.handlers,sys

from pycvf.core import settings

LOG_FILENAME = settings.PYCVF_LOG_DIR+ '/messages.log'

pycvf_logger = logging.getLogger('PYCVF - '+sys.argv[0])
pycvf_logger.setLevel(logging.DEBUG)
# create formatter
pycvf_log_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# add formatter to ch


# Add the log message handler to the logger
pycvf_log_handler = logging.handlers.RotatingFileHandler(  LOG_FILENAME, maxBytes=1024*1024*10, backupCount=10)
pycvf_log_handler.setFormatter(pycvf_log_formatter)
pycvf_logger.addHandler(pycvf_log_handler)


def pycvf_error(errmsg):
   try:
     from termcolor import colored
   except:
     def colored(x,*args,**kwargs):
        return x
   if (type(errmsg)==unicode):
      errmsg=errmsg.encode('utf8')
   sys.stderr.write(colored(errmsg,'red','on_white'))
   sys.stderr.write("\n")
   pycvf_logger.error(errmsg)

   
def pycvf_warning(errmsg):
   try:
     from termcolor import colored
   except:
     def colored(x,*args,**kwargs):
        return x
   if (type(errmsg)==unicode):
      errmsg=errmsg.encode('utf8')
   sys.stderr.write( colored(errmsg,'blue','on_white'))
   sys.stderr.write("\n")
   pycvf_logger.warning(errmsg)

pycvf_debug_level=20

def pycvf_debug(dbglevel,errmsg):
   if (dbglevel<pycvf_debug_level):
     try:
       from termcolor import colored
     except:
       def colored(x,*args,**kwargs):
          return x
     if (type(errmsg)==unicode):
        errmsg=errmsg.encode('utf8')
     sys.stderr.write( colored(errmsg,'green','on_white'))
     sys.stderr.write("\n")
     pycvf_logger.debug(errmsg)


