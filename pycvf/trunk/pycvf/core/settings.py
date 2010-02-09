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
## xxxx
##

##
## IMPORT DEFAULT FOR VALUE FOR DIRECTORIES
##

from pycvf.core.directories import *



DEBUG_LEVEL=0

LOG_LEVEL=2

DISPLAY_DRIVER="pyglet"
#DISPLAY_DRIVER="aa"
AA_WITH_CURSES=True

AUDIO_DRIVER="alsa"

DEFAULT_FRAMEWORK="3"

DEFAULT_SESSION="std"

#DEFAULT_DATABASE="image_directory"
#DEFAULT_DATABASE_ARGS="'path':'/usr/share/tuxpaint/images/magic/','rescale':(200,320,'R')"

DEFAULT_DATABASE="image.kanji()"
DEFAULT_DATABASE_ARGS=""

DEFAULT_MODEL="naive()"
DEFAULT_MODEL_ARGS=""

DEFAULT_INDEX_CLASS="pseudoincremental(sashindex)"
#DEFAULT_INDEX_CLASS="pseudoincremental(lshindex_lshkit)"
DEFAULT_INDEX_ARGS=""

PYCVF_DATABASE_PATH=":pycvf.databases."
PYCVF_MODEL_PATH=":pycvf.nodes." #:pycvf.archives.framework02.models."
PYCVF_INDEX_PATH=":pycvf.indexes."


###
### DEFAULT INSTALLATION PATH FOR WORDNET
###


WNDICT="/usr/local/wordnet3/dict/"
WNHOME="/usr/local/wordnet3"


import os
try:
  exec file(os.path.join(os.environ["HOME"],".pycvf-settings.py")).read()
except:
  pass

try:
  exec file(os.path.join(os.getcwd(),"local-pycvf-settings.py")).read()
except:
  pass

