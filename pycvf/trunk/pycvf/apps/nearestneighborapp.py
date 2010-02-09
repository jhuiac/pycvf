#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pycvf.lib.info.graph import *
from pycvf.core.generic_application import *
from pycvf.core.errors import *

class NearestNeighborsGraphApp(IndexUsingApplication):
  class ProgramMetadata(object):
      name="Nearest Neighbors Graph Application"
      version="0.1"
      author="Bertrand Nouvel bertrand.nouvel@gmail.com"
      copyright="        COPYRIGHT Bertrand Nouvel - JFLI - CNRS 2009"

  number_query=CmdLineString('n',"numberofneighbors",'number',"name of neighbours","3")

  @classmethod
  def process(cls,nrels=1,*args,**kwargs):
       nq=int(cls.number_query.value)
       bykey=False
       if (bykey):
         nodeshape=iter(cls.vdb).next()[0].shape
         pycvf_debug(10,"computing nodes")
         nodes=map(lambda x:x, cls.idx.keys())
         pycvf_debug(10,"computing edges")
         edges=[]
         for n in nodes:
            qr=cls.idx.query([n],nq)
            te=map(lambda x: (n,cls.vdb[x[0][0]]),qr[0])  
            edges.extend(te)
   
         pycvf_debug(10,"rendering graph")
         g=Graph((nodes,edges),                              
                              nodes_extract_f=lambda g:nodes,
                              edges_extract_f=lambda g:edges,
                              node_outedges_f=lambda g, n:map(lambda x: (n,cls.vdb[x[0][0]]),cls.idx.query([n],mq)[0]),
                              node_inedges_f=None,
                              edge_target_f=lambda g, e:e[1],
                              edge_source_f=lambda g, e:e[0],
                              edge_strength_f=lambda g, e:1,
                        )
       else:
         nodeshape=iter(cls.vdb).next()[0].shape
         pycvf_debug(10,"computing nodes :shape=%r"%(nodeshape,))
         nodes=map(lambda x:x, cls.idx.values())
         print "%d Nodes Found." %(len(nodes),)
         pycvf_debug(10,"computing edges")
         edges=[]
         for n in nodes:
            print n,nq
            qr=cls.idx.query([cls.vdb[n[0]]],nq)
            te=map(lambda x: (n,x[0][0]),qr[0])  
            edges.extend(te)
         print "%d Edges Found." %(len(edges),)            
   
         pycvf_debug(10,"rendering graph")
         g=Graph((nodes,edges),                              
                              nodes_extract_f=lambda g:nodes,
                              edges_extract_f=lambda g:edges,
                              node_outedges_f=lambda g, n:map(lambda x: (n,x[0][0]),cls.idx.query(cls.vdb[n[0]],mq)[0]),
                              node_inedges_f=None,
                              edge_target_f=lambda g, e:e[1],
                              edge_source_f=lambda g, e:e[0],
                              edge_strength_f=lambda g, e:1,
                        )
        
       g.tlp_show()

       

NearestNeighborsGraphApp.run(sys.argv[1:])
