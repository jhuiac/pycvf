# -*- coding: utf-8 -*-
#########################################################################################################################################
#
# VideoModel Trainer builder By Bertrand NOUVEL
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
          -S               : save model after each processed video (may be useful when video processing time is long)
          -db database         : name of the model to import                                                 
          -h               : displays this helps message
        #######################################################################################
        Example :
            Determine the influence of the xxx parameter over a certain number of initial parameters
        #######################################################################################
        """
        )
        sys.exit(retcode)

        
visionmodel="visionmodel008"
videodatabase="mvptrainingdatabase"
videodatabaseargs=""
outpath=None
saveaftereachvideo=False
                                                                                                       
go=getopt.getopt(sys.argv[1:],'Om:hS','db=')
for o in go[0]:                                
    if (len(o)):                                 
        if (o[0]=='-m'):
                    visionmodel=o[1]
        elif (o[0]=='-S'):
                    saveaftereachvideo=True
        elif (o[0]=='-h'):                                                                                                    
                    print_help_and_exit()                                                                                                                        
        elif (o[0]=='--db'):
                    videodatabase=o[1]
        elif (o[0]=='--help'):                                                                                                    
                    print_help_and_exit()                                                                                             

print go
        
if not outpath:
    outpath="/home/tranx/videodatabase/"+visionmodel+"-"+videodatabase+"/"


exec("from "+ visionmodel +" import *")
exec("from "+ videodatabase +" import *")
trkfilename=None


if __name__=="__main__":
  import datetime
  if (len(videodatabaseargs)):
    vdb=VideoDatabase( *eval(videodatabaseargs))
  else:
    vdb=VideoDatabase()      
  vi=VisionModel(vdb)
  vi.train(outpath,saveaftereachvideo=saveaftereachvideo)
