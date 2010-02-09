# -*- coding: utf-8 -*-
#########################################################################################################################################
#
# Video Database builder By Bertrand NOUVEL
# 2009 CNRS Postdoctorate JFLI
#
# (c) All rights reserved
# ###############################################
#
#########################################################################################################################################
# Import required objects
#########################################################################################################################################

import re, os, math, random, time,sys, traceback
from pycvf.lib.info.observations import *
from pycvf.lib.info.track import *

import os
import sys
import time
import logging

     

from jfli.project_specific.videoindex.reportgenerator import *

if __name__=="__main__":
   if len(sys.argv)<3:
       print "makereport trackfile.trk report.pdf [speed]"
   track=OnDiskMultiTrackLargeZ(sys.argv[1])
   layout=makesimplelayoutfromtrack(track,track.meta)
   speed=250
   if (len(sys.argv)>=4):
       speed=int(sys.argv[3])
   rg=ReportGenerator(sys.argv[2],track,layout,speed=speed)
   del rg
   del track


