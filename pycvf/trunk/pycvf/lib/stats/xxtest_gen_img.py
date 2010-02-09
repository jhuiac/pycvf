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

## first image is garbage
from pycvf.nodes.images import visionmodel010 as mymodel
from jfli.databases.videos import mvp as contentdatabase

vm=visionmodel.MyModel()
db=contentdatabase.ContentsDatabase()
vr=db.all().next()
i=vr.step()[0]
r=vm.msample("/home/tranx/videodatabase/mymodel010-mvptrainingdatabase.sav/","/tmp2/sampleout.trk",vr)

#vm.init_features()
#vm.init_observed_features_statistics(basepath="/home/tranx/videodatabase/mymodel009-mvptrainingdatabase.sav/",mlop="samplev")

