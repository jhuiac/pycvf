####
#### small graph for topological sort
####
import numpy

def explore_connected_graph(graph_root,node_edges, edge_target, visitor, node_func=lambda x:x,edge_func=lambda x,s,d:x):
    l=[graph_root]
    while (l!=[]):
        n=l[0];l=l[1:]
        visitor.set_visited(n)
        node_func(n)
        for e in node_edges(n):
            edge_func(e,n,edge_target(e))
        newnodes=filter( lambda n: not visitor.get_visited(n) , map(edge_target,node_edges(n)) )
        l.extend(newnodes)
    visitid+=1

def explore_graph(graph_nodes,node_edges, edge_target, visitor, node_func=lambda x:x,edge_func=lambda x,s,d:x ):
    for n in graph_nodes:
        if (visitor.get_visited(n)):
            explore_connected_grah(n,node_edges,edge_target, get_visited, set_visited, node_func,edge_func)


def _maximal_connected_components(graph_nodes,node_edges,edget_target, visitor):
    class mcc_aglomerator:
        def __init__(self,n):
            self.g={}
            self.cc=n
        def f(self,n):
            self.g.append(n)
    cc=0
    r=[]
    for n in graph_nodes:
        if (not get_visited(n)):
            mcc=mcc_aglomerator(cc)
            explore_connected_grah(n,node_edges,edge_target,visitor,node_func=mcc.f)
            r.append(mcc.g)
            cc+=1
    return r;

class SGraph:
    class Edge:
        def __init__(self,bo,g):
            self.bo=bo
            self.g=g
        def target(self):
            x=self.g.edge_target_f(self.g,self.bo)
            return self.g.Node(x,self.g)
        def source(self):
            x=self.g.edge_source_f(self.g,self.bo)
            return self.g.Node(x,self.g)
        def strength(self):
            return self.g.edge_strength_f(self.g.bo,self.bo)
        def id(self):
            return self.g.edgeid_f(self.g.bo,self.bo)
    class Node:
        def __init__(self,bo,g):
            self.bo=bo
            self.g=g
        def outedges(self):
            return map ( lambda x:self.g.Edge(x,self.g),self.g.node_outedges_f(self.g.bo,self.bo))
        def inedges(self):
            return map ( lambda x:self.g.Edge(x,self.g),self.g.node_inedges_f(self.g.bo,self.bo))
        def inarity(self):
            return len(self.inedges())
        def outarity(self):
            return len(self.outedges())
        def targets(self):
            for e in self.outedges():
                return e.target()
        def sources(self):
            for e in self.inedges():
                return e.source()
        def id(self):
            return self.g.nodeid_f(self.g.bo,self.bo)
    def __init__(self,base_object, nodes_extract_f=lambda x:x[0],
                              edges_extract_f=lambda x:x[1],
                              node_outedges_f=lambda n:n[1],
                              node_inedges_f=None,
                              edge_target_f=lambda e:e[2],
                              edge_source_f=None,
                              edge_strength_f=lambda e:1,
                              nodeid_f=None,
                              edgeid_f=None,
                              add_node_f=None,
                              remove_node_f=None,
                              add_edge_f=None,
                              remove_edge_f=None,
                              ):
        self.bo=base_object
        self.nodes_extract_f=nodes_extract_f
        self.edges_extract_f=edges_extract_f
        self.node_outedges_f=node_outedges_f
        self.node_inedges_f=node_inedges_f
        self.edge_target_f=edge_target_f
        self.edge_source_f=edge_source_f
        self.edge_strength_f=edge_strength_f
        self.add_edge_f=add_edge_f
        self.remove_edge_f=remove_edge_f
        self.add_node_f=add_node_f
        self.remove_node_f=remove_node_f
        if (nodeid_f):
            self.nodeid_f=nodeid_f
        else:
            self.allnodes=self.nodes_extract_f(self.bo)
            self.nodeid_f=(lambda n : self.allnodes.index(n))
        if (edgeid_f):
            self.edgeid_f=edgeid_f
        else:
            self.alledges=self.edges_extract_f(self.bo)
            self.edgeid_f=(lambda n : self.alledges.index(n))
        self.lastvisitid=-1
        self._numnodes=len(self.nodes())
        self._numedges=len(self.edges())
        self.visitvector=numpy.zeros((self._numnodes))
        self.currentvisitid=self.lastvisitid+1
       # self.nodeid=dict(zip(self.nodes(),numpy.array(range(self._numnodes))))
       # self.edgeid=dict(zip(self.edges(),numpy.array(range(self._numedges))))
    def add_node(self,x):
        self.bo=self.add_node_f(self.bo,x)
        self.lastvisitid=-1
        self._numnodes=len(self.nodes())
        self._numedges=len(self.edges())
        self.visitvector=numpy.zeros((self._numnodes))
        self.currentvisitid=self.lastvisitid+1
    def remove_node(self,x):
        self.bo=self.remove_node_f(self.bo,x)
        self.lastvisitid=-1
        self._numnodes=len(self.nodes())
        self._numedges=len(self.edges())
        self.visitvector=numpy.zeros((self._numnodes))
        self.currentvisitid=self.lastvisitid+1
    def add_edge(self,s,d,ss=1):
        if (isinstance(s,SGraph.Node)):
            s=s.bo
        if (isinstance(d,SGraph.Node)):
            d=d.bo
        self.bo=self.add_edge_f(self.bo,s,d,ss)
        self.lastvisitid=-1
        self._numedges+=1
    def remove_edge(self,s,d):
        if (isinstance(s,SGraph.Node)):
            s=s.bo
        if (isinstance(d,SGraph.Node)):
            d=d.bo
        self.bo=self.remove_edge_f(self.bo,s,d)
        self._numedges-=1
    def get_visitor(self):
        class Visitor:
            def __init__(self,graph,visitid):
                self.graph=graph
                self.visitid=visitid
            def has_visited(self,node):
                return self.graph.visitvector[self.graph.nodeid_f(node)]==self.visitid
            def set_visited(self,node):
                return self.graph.visitvector[self.graph.edgeid_f(node)]==self.visitid
        self.currentvisitid+=1
        return Visitor(self,self.currentvisit)
    def nodes(self): # returns a list of nodes
        return map(lambda n: self.Node(n,self),self.nodes_extract_f(self.bo))
    def edges(self): # returns a list of nodes
        return map(lambda e: self.Edge(e,self),self.edges_extract_f(self.bo))


def topological_sort(g):
    l=[]
    s=filter(lambda n:n.inarity()==0,g.nodes())
    try:
        while True:
            n=s.pop(0)
            l.append(n)
            for e in n.outedges():
                m=e.target()
                g.remove_edge(e.source(),e.target())
                if (m.inarity()==0):
                    #print "."
                    s.append(m)
    except IndexError:
        pass
    if ( g.edges() ):
        raise Exception,"The graph contains one cycle"+str(len(l))
    return l

def fct_del(l,v):
    del l[v]
    return l

def fct_append(l,v):
    l.append(v)
    return l

def graph_node_edge_lists(initgraph=([],[])):
    """ very naive graph implementation """
    return SGraph(initgraph,
                 nodes_extract_f=(lambda g:g[0]),   ### obtenir les noeuds d un graphe
                 edges_extract_f=(lambda g:g[1]),   ###
                 node_outedges_f=(lambda g,n:filter(lambda e:e[0]==n,g[1])),   ###
                 node_inedges_f=(lambda g,n:filter(lambda e:e[1]==n,g[1])),   ###
                 edge_target_f=(lambda g,e:e[1]),   ###
                 edge_source_f=(lambda g,e:e[0]),   ###
                 edge_strength_f=(lambda g,e:1),    ###
                 nodeid_f=(lambda g,n:g[0].index(n)),   ###
                 edgeid_f=(lambda g,e:g[1].index(e)),   ###
                 add_node_f=(lambda g,n:(fct_append(g[0],n),g[1])),   ###
                 remove_node_f=(lambda g,e:(fct_del(g[0],g[0].index(e)),g[1])),
                 add_edge_f=(lambda g,s,d,st:(g[0],fct_append(g[1],(s,d)))),
                 remove_edge_f=(lambda g,s,d:(g[0],fct_del(g[1],g[1].index((s,d)))))
                 )

def graph_copy(g,typeofgraph=graph_node_edge_lists):
    gr=typeofgraph()
    for n in g.nodes():
        gr.add_node(n.bo)
    for e in g.edges():
        gr.add_edge(n.bo)
    return gr
