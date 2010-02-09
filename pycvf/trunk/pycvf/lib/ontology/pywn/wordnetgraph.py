from jfli.ontology.pywn.stdwn import *
from jfli.info.graph import *

def graph_from_word(ww,n=0):
    return Graph(impl.lookupSynsetsByForm(ww)[0],
                 nodes_extract_f=None,
                 edges_extract_f=None,
                 node_outedges_f=(lambda s,n: map(lambda e:(e[0],s,e[1]), s.rels)),
                 node_inedges_f=None,
                 edge_target_f=(lambda e,s,d:s),
                 edge_source_f=(lambda e,s,d:impl.lookupSynsetByKey(d)),
                 edge_strength_f=(lambda m,e,f:1),
                 nodeid_f=None,
                 edgeid_f=None
                 )
