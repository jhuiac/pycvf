# -*- coding: utf-8 -*-
#########################################################################################################################################
#
# VideoModel based Segmenter
# 2009 CNRS Postdoctorate JFLI
#
# (c) All rights reserved
# ###############################################
#
#########################################################################################################################################
# Import required objects
#########################################################################################################################################

import re, os, math, random, time,sys, traceback, getopt



def print_help_and_exit(retcode=0):
        sys.stderr.write("""           
        #######################################################################################
        train_model.py
        #######################################################################################
        COPYRIGHT Bertrand Nouvel - JFLI - CNRS 2009 v0.1                                      
        #######################################################################################
        run local models macro-economical simulations                                          
        #######################################################################################
          -m model         : name of the model to import
          -rb filename         : name of the trackfile                                                                              
          -db database         : name of the model to import                                                 
          -h               : displays this helps message
        #######################################################################################
        Example :
            Determine the influence of the xxx parameter over a certain number of initial parameters
        #######################################################################################
        """
        )
        sys.exit(retcode)

        
visionmodel=None
trackfile=None
videodatabase="mvptrainingdatabase"
videodatabaseargs=""
modelpath=None
                                                                                                       
go=getopt.getopt(sys.argv[1:],'Ot:m:h','Odb:')
for o in go[0]:                                
    if (len(o)):                                 
        if (o[0]=='-m'):
                    visionmodel=o[1]
        elif (o[0]=='-t'):
                    trackfile=o[1]
        elif (o[0]=='-h'):                                                                                                    
                    print_help_and_exit()                                                                                             
        
if not modelpath:
    modelpath="/home/tranx/videodatabase/"+visionmodel+"-"+videodatabase+"/"


assert(visionmodel)

exec("from "+ visionmodel +" import VisionModel")
exec("from "+ videodatabase +" import VideoDatabase")



if __name__=="__main__":
  import datetime
  if (len(videodatabaseargs)):
    vdb=VideoDatabase( *eval(videodatabaseargs))
  else:
    vdb=VideoDatabase()      
  vi=VisionModel(vdb)
  vi.segment(basepath=modelpath,trkfilename=trackfile)
