#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################################################################################
# 2009 CNRS Postdoctorate JFLI
#
# (c) All rights reserved
# ###############################################
#
#########################################################################################################################################
# Import required objects
#########################################################################################################################################


from pycvf.core.generic_application import *

class DbIdxBuilder(IndexUsingApplication):
  class ProgramMetadata(object):
      name="Index Builder Application"
      version="1.0"
      author="Bertrand Nouvel bertrand.nouvel@gmail.com"
      copyright="        COPYRIGHT Bertrand Nouvel - JFLI - CNRS 2009"
      license="GPLv3"

        

  key=CmdLineString(None,"key","modelpath","specified within the model what should be used as key when indexing","/")
  value=CmdLineString(None,"value","modelpath","specified within the model what should be used as value when indexing","@")
#  feature_select=["selected_feature"] # we only create one index here


  @classmethod
  def process(cls,*args, **kwargs):
      try:
        for e in cls.vdb:
          keys=cls.mdl.process_path([e[0]],[e[1]],cls.key.value,lambda x:x)
          values=cls.mdl.process_path([e[0]],[e[1]],cls.value.value,lambda x:x)
          for c in zip(keys,values):
               cls.idx.add(c[0],c[1])
          sys.stderr.write(".")
          sys.stderr.flush()
      except KeyboardInterrupt:
        print "Indexing stopped... Saving index.."
        pass
      try:
        cls.idx.save(cls.index_filename)
      except Exception,e:
        print "Saving of index interrupted / be carefull you're index maybe in an unstable state.."        
        print e
        import traceback
        traceback.print_tb(sys.exc_info()[2])

if __name__=="__main__":       
  DbIdxBuilder.run(sys.argv[1:])

