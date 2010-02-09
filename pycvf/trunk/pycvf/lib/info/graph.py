# -*- coding: utf-8 -*-
## graph.py
## Copyright 2009 Bertrand NOUVEL - JFLI - CNRS

####
####
####

from pycvf.lib.info.basic_graph import *

## this is a wrapper class for uniform access to various class in many algorithms
## you just need to provide the functions the algorithms are going to use...
class Graph:
    class Edge:
        def __init__(self,bo,g):
            self.bo=bo
            self.g=g
        def target(self):
            x=self.g.edge_target_f(self.g,self.bo)
            return self.g.Node(x,self.g)      
        def target_(self):
            x=self.g.edge_target_f(self.g,self.bo)
            if (self.g.allnodes):
               return self.g.allnodes[self.g.nodeid_f(x)]
            else:
               return filter(lambda n:n.bo==x ,self.g.nodes())[0]
        def source_(self):
            x=self.g.edge_source_f(self.g,self.bo)
            if (self.g.allnodes):
               return self.g.allnodes[self.g.nodeid_f(x)]
            else:
               return filter(lambda n:n.bo==x ,self.g.nodes())[0]
        def source(self):
            x=self.g.edge_source_f(self.g,self.bo)
            return self.g.Node(x,self.g)        
        def strength(self):
            return self.g.edge_strength_f(self.g.bo,self.bo)
        def id(self):
            return self.g.edgeid_f(self.g.bo,self.bo)
        def attributes(self):
            return self.g.edge_attribute_f(self.g.bo,self.bo)
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
            return [ e.target() for e in self.outedges() ]
        def explore_from_here(self,f,node_func=lambda x:x,edge_func=lambda x,s,d:x):
            visitor=self.g.get_visitor()
            rec_explore_connected_graph(self,lambda n:n.target, lambda e:e.target, visitor,node_func,edge_func)
        def sources(self):
            return [ e.source() for e in self.inedges()]
        def attributes(self):
            return self.g.node_attribute_f(self.g.bo,self.bo)
        def repr(self):
            if (self.g.node_repr_f):
                return self.g.node_repr_f(self.g.bo,self.bo)
            else:
                return str(self.bo)
        def __repr__(self):
            if (self.g.node_repr_f):
                return self.g.node_repr_f(self.g.bo,self.bo)
            else:
                return str(self.bo)
        def id(self):
            return self.g.nodeid_f(self.g.bo,self.bo)
        def random_walk_from_here(self,length=10):
            if (length<=0):
                return [self]
            return [self]+random.choice(self.targets()).random_walk_from_here(length-1)
        def prandom_walk_from_here(self,length=10,edge_filter=None):
            import scipy
            if (length<=0):
                return [self]
            if (not edge_filter):
                edge_filter=lambda x,y:1
            sm=map(lambda e:edge_filter(e,length)*e.strength(),self.outedges())
            rv=(random.random()*sum(sm))
            idx=sum((scipy.cumsum(sm)<rv).astype(int))
            return [self]+(self.outedges()[idx]).target().prandom_walk_from_here(length-1,edge_filter)
        
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
                              node_repr_f=None,
                              node_attribute_f=None,
                              edge_attribute_f=None
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
        self.node_attribute_f=node_attribute_f
        self.edge_attribute_f=edge_attribute_f
        self.node_repr_f=node_repr_f
        if (nodeid_f):
            self.nodeid_f=nodeid_f
            self.allnodes=None
        else:
            self.allnodes=self.nodes_extract_f(self.bo)
            def gen_nodeid_f(g,n):
              try:
                return self.allnodes.index(n)
              except:
                print n, type(n)
                print self.allnodes, type(self.allnodes[0])
                raise Exception, "Index Not Found"
            self.nodeid_f=gen_nodeid_f
        if (edgeid_f):
            self.edgeid_f=edgeid_f
            self.alledges=None
        else:
            self.alledges=self.edges_extract_f(self.bo)
            self.edgeid_f=(lambda g, e : self.alledges.index(e))
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
        if (isinstance(s,Graph.Node)):
            s=s.bo
        if (isinstance(d,Graph.Node)):
            d=d.bo
        self.bo=self.add_edge_f(self.bo,s,d,ss)
        self.lastvisitid=-1
        self._numedges+=1
    def remove_edge(self,s,d):
        if (isinstance(s,Graph.Node)):
            s=s.bo
        if (isinstance(d,Graph.Node)):
            d=d.bo
        self.bo=self.remove_edge_f(self.bo,s,d)
        self._numedges-=1
    def get_visitor(self):
        class Visitor:
            def __init__(self,graph,visitid):
                self.graph=graph
                self.visitid=visitid
            def has_visited(self,node):
                return self.graph.visitvector[self.graph.nodeid_f(self.graph.bo,node.bo)]==self.visitid
            def set_visited(self,node):
                self.graph.visitvector[self.graph.nodeid_f(self.graph.bo,node.bo)]=self.visitid
        self.currentvisitid+=1
        return Visitor(self,self.currentvisitid)
    def nodes(self):
        """returns a list of nodes"""
        return map(lambda n: self.Node(n,self),self.nodes_extract_f(self.bo))
    def edges(self):
        """ returns a list of edges"""
        return map(lambda e: self.Edge(e,self),self.edges_extract_f(self.bo))
    def edge_node_ratio(self):
	return float(len(self.edges()))/float(len(self.nodes()))
    def maximal_connected_components(self):
        """ seek for maximal connected components"""
        cc=int_maximal_connected_components(self.nodes(),lambda n:n.outedges(), lambda e:e.target(),self.get_visitor())
        self.currentvisitid+=1
        return cc
    def symmetric_closure(edge_projection=lambda e:(e.source(),e.target()),
                          rev_edge_projection=lambda e:(e.target(),e.source()),
                          rev_edge_arguments=lambda e:((e.target(),e.source()),{})):
	g= graph_node_edge_lists(g0.nodes(),
                                 g0.edges(),
                                 nodes_attributes_f=(lambda g,n:n.attributes()),
                                 edges_attributes_f=(lambda g,e:e.attributes())
                                 )
	ledge=set(map(edge_projection, g.edges))
	for e in ledge:
	  if rev_edge_projection(e) not in ledge:
	    rev_edge_args,rev_edge_xargs=rev_edge_arguments(e)
	    g.add_edge(*rev_edge_args,**rev_edge_xargs)
        return g
    def maximal_connected_components_graphs(self):
        return map(
                   lambda cc:
                       Graph(
                             (self, cc),
                             nodes_extract_f=lambda g:map(lambda x:x.bo, g[1]),
                             edges_extract_f=lambda g:map(lambda x:x.bo, reduce( lambda x,n:x+n.outedges(), g[1] , [])) ,
                             node_outedges_f=self.node_outedges_f,#lambda g, n:map(lambda x:x.bo,n.outedges()),
                             edge_target_f=self.edge_target_f,
                             edge_source_f=self.edge_source_f,
                             edge_strength_f=lambda g,e:self.edge_strength_f(g[0].bo,e),
                             node_attribute_f=self.node_attribute_f,
                             edge_attribute_f=self.edge_attribute_f
                             #nodeid_f=self.nodeid_f,  ## visitors expect continuous values
                             #edgeid_f=self.edgeid_f
                             )
                   ,
                   self.maximal_connected_components())
    def quick_dot_string(self):
        """ return the graphviz representation of the graph without taking in account any attributes """
        return "digraph g{\n"+"\n".join(map(lambda x:x.source().repr()+"->"+x.target().repr(), self.edges()))+"\n}\n"
    def quick_dot_show(self):
        """ display the graph within graphviz without taking in account any attributes """
        tmpfilename="/tmp/python-dot-"+str(os.getuid())+"-"+str(os.getpid())+".dot"
        f=file(tmpfilename,"w")
        f.write(self.quick_dot_string())
        f.close()
        os.system("dot "+tmpfilename+"|dotty -")
        os.remove(tmpfilename)
    def _to_tlp_string(self,property_list):
        """ """
        res=_graph_to_tlp2(self.nodes_f(self.bo),self.node_outedges_f, self.edge_target_f,self.currentvisitid,property_list)
        self.currentvisitid+=6
        return res
    def _to_dot_string(self,property_list):
        res=_graph_to_dot(self._nodes(self.bo),self.node_outedges_f, self.edge_target_f,self.currentvisitid,property_list)
        self.currentvisitid+=6
        return res
    def __to_tlp_string(self,property_list):
        res=_graph_to_tlp2(self.nodes(),lambda n:n.outedges(), lambda e:e.target(),self.get_visitor,property_list)
        #self.currentvisitid+=6
        return res
    ###############################
    def __to_dot_string(self,property_list):
        res=_graph_to_dot(self.nodes(),lambda n:n.outedges(), lambda e:e.target(),self.get_visitor,property_list)
        return res
    ##############################
    def to_dot_string(self,property_list,name="g"):
        """ This is an old version of a way of computing a graph representation of an arbitrary graph """
        buf="digraph "+name+"{"
        class NodeEdgePrintExplorer:
            def __init__(self,plist=None,buf=""):
                self.buf=buf
                self.plist=plist
            def f(self,n):
                attrs=[]
                for p in property_list:
                    if (p.has_key('node_info')):
                        x=p['node_info'](n)
                        if (x):
                            attrs.append(p['name']+'='+str(x))
                attrs=','.join(attrs)
                if (len(attrs)>0):
                    self.buf+=("n%d [%s];\n"%(n.id(),attrs))
                else:
                    self.buf+=("n%d;\n"%(n.id()))
            def ef(self,e):
                attrs=[]
                s=e.source()
                d=e.target()
                for p in property_list:
                    if (p.has_key('edge_info')):
                        x=p['edge_info'](e,s,d)
                        if (x):
                            attrs.append(p['name']+'='+str(x))
                attrs=','.join(attrs)
                if (len(attrs)>0):
                    self.buf+=("n%d->n%d [%s]\n"%(s.id(),d.id(),attrs))
                else:
                    self.buf+=("n%d->n%d\n"%(s.id(),d.id()))
        ex=NodeEdgePrintExplorer(property_list)
        for n in self.nodes():
            ex.f(n)
        for e in self.edges():
            ex.ef(e)
        buf+=ex.buf
        buf+="}\n"
        return buf;
    def to_tlp_string(self,property_list):
        """deprecated function for returning a tulip  string description of a graph"""
        buf=""
        buf+="(nodes "+' '.join(map(str,range(0,len(self.nodes()))))+")\n"
        class EdgePrintExplorer:
            def __init__(self,buf=""):
                self.buf=buf
            def f(self,e):
                s=e.source()
                d=e.target()
                self.buf+=("(edge %d %d %d)\n"%(e.id(),s.id(),d.id()))
        ex=EdgePrintExplorer()
        for e in self.edges():
            ex.f(e)
        buf+=ex.buf
        pid=0
        for p in property_list:
            buf+="(property "+str(pid)+" "+p['type']+" \""+p["name"]+"\"\n(default \""+p["default_node"]+"\" \""+p["default_edge"]+"\")"
            class PNodeExplorer:
                def __init__(self,nodeinfo=None,edgeinfo=None,buf=""):
                    self.buf=buf
                    self.nodeinfo=nodeinfo
                    self.edgeinfo=edgeinfo
                def f(self,n):
                    if (self.nodeinfo):
                        self.buf+=("(node %d \"%s\")\n"%(n['id'],str(self.nodeinfo(n))))
                def ef(self,e):
                    s=e.source()
                    d=e.target()
                    if (self.edgeinfo):
                        self.buf+=("(edge %d \"%s\")\n"%(e.id(),str(self.edgeinfo(e,s,d))))
            if (p.has_key('node_info') or p.has_key('edge_info')):
                buf+="\n"
                ex=PNodeExplorer(p.has_key('node_info') and p['node_info'] or None,  p.has_key('edge_info') and p['edge_info'] or None)
                visitor=get_visitor()
                for n in self.nodes():
                    ex.f(n)
                for e in selg.edges():
                    ex.ef(e)
                buf+=ex.buf
            buf+=")\n"
        #pid+=1# tulip does not change this value actually
        return buf;
    def to_tlp_string_new(self,nodes_property_list=None, edges_property_list=None, render_path=None):
        """new function for returning a tulip  string description of a graph based on a property list"""
        if not nodes_property_list:
            nodes_property_list=tlp_node_std_attribute_mapping
        if not edges_property_list:
            edges_property_list=tlp_edge_std_attribute_mapping
        buf=""
        buf+="(nodes "+' '.join(map(str,range(0,len(self.nodes()))))+")\n"
        class EdgePrintExplorer:
            def __init__(self,buf=""):
                self.buf=buf
            def f(self,e):
                s=e.source()
                d=e.target()
                self.buf+=("(edge %d %d %d)\n"%(e.id(),s.id(),d.id()))
        ex=EdgePrintExplorer()
        for e in self.edges():
            ex.f(e)
        buf+=ex.buf
        pid=0
        skeys=set(nodes_property_list.keys()).union(set( edges_property_list.keys()))
        for p in skeys:
            k0=p
            typeprop="int"
            try:
                node_default=nodes_property_list[k0][3]
                relname=nodes_property_list[k0][0]
                typeprop=nodes_property_list[k0][1]
            except:
                node_default=""
            try:
                edge_default=edges_property_list[k0][3]
                relname=edges_property_list[k0][0]
                typeprop=edges_property_list[k0][1]
            except:
                edge_default=""
            buf+="(property "+str(pid)+" "+typeprop+" \""+relname+"\"\n(default \""+node_default+"\" \""+edge_default+"\")"
            if (nodes_property_list.has_key(k0)):
                v1=nodes_property_list[k0][2]
                for n in  self.nodes():
                    if (n.attributes().has_key(k0)):
                        buf+="(node %d \"%s\")\n"%(n.id(), v1(self, 1, n.attributes()[k0],render_path))
            if (edges_property_list.has_key(k0)):
                v1=edges_property_list[k0][2]
                for e in  self.edges():
                    if (e.attributes().has_key(k0)):
                        buf+="(edge %d \"%s\")\n"%(e.id(), v1(self, 1, e.attributes()[k0],render_path))
            buf+="\n)\n"
        #pid+=1# tulip does not change this value actually
        return buf;
    def dot_show(self,property_list=[],remove_after=True):
        tmpfilename="/tmp/python-dot-"+str(os.getuid())+"-"+str(os.getpid())+".dot"
        f=file(tmpfilename,"w")
        f.write(self.to_dot_string(property_list))
        f.close()
        os.system("dot "+tmpfilename+"|dotty -")
        if (remove_after):
            os.remove(tmpfilename)
    def dot_render(self,filename,format="png",property_list=[],remove_after=True):
        tmpfilename="/tmp/python-dot-"+str(os.getuid())+"-"+str(os.getpid())+".dot"
        f=file(tmpfilename,"w")
        f.write(self.to_dot_string(property_list))
        f.close()
        os.system("dot "+tmpfilename+" -T"+format + " -o "+filename)
        if (remove_after):
            os.remove(tmpfilename)
    def tlp_show(self,property_list=[]):
        tmpfilename="/tmp/python-tlp-"+str(os.getuid())+"-"+str(os.getpid())+".tlp"
        f=file(tmpfilename,"w")
        f.write(self.to_tlp_string(property_list))
        f.close()
        os.system("tulip "+tmpfilename)
        os.remove(tmpfilename)
    def tlp_show_new(self,nodes_property_list=None, edges_property_list=None):
        if not nodes_property_list:
            nodes_property_list=tlp_node_std_attribute_mapping
        if not edges_property_list:
            edges_property_list=tlp_edge_std_attribute_mapping
        render_path="/tmp/python-tlp-"+str(os.getuid())+"-"+str(os.getpid())+"-"+str(time.time())
        os.mkdir(render_path)
        tmpfilename=render_path+"/tlp-file.tlp"
        f=file(tmpfilename,"w")
        f.write(self.to_tlp_string_new(nodes_property_list,edges_property_list, render_path=render_path))
        f.close()
        os.system("tulip "+tmpfilename)
        for x in (os.listdir(render_path)):
            os.remove(render_path+"/"+x)
        #os.remove(tmpfilename)
        os.rmdir(render_path)
    def indexnodes(self):
        pass
    def save(self,file):
        pickle.save(file,self,protocol=2)
    def distancematrix(self,dtype=numpy.float):
        self.indexnodes()
        DM=numpy.ndarray(shape=(self._numnodes,self._numnodes),dtype=dtype)
        if (dtype==complex):
            DM.fill(numpy.inf*(1+1J))
        else:
            DM.fill(numpy.inf)
        for n in self.nodes():
            for e in n.outedges():
                DM[ e.source().id(), e.target().id() ]= min(DM[ e.source().id(),e.target().id() ],1./e.strength())
            DM[n.id(),n.id()]=0
        return numpy.matrix(DM)
    def weightmatrix(self):
        self.indexnodes()
        DM=numpy.zeros((self._numnodes,self._numnodes))
        for n in self.nodes():
            for e in n.outedges():
                DM[e.target().id(), e.source().id() ]+= e.strength()
        return numpy.matrix(DM)
    def symmetrized_weight_matrix(self):
        self.indexnodes()
        DM=numpy.zeros((self._numnodes,self._numnodes))
        for n in self.nodes():
            for e in n.outedges():
                DM[e.target().id(), e.source().id() ]+= (e.strength()/2)
                DM[e.source().id(),e.target().id() ]+= (e.strength()/2)
        return numpy.matrix(DM)
    def degreematrix(self):
        self.indexnodes()
        DM=numpy.zeros((self._numnodes,self._numnodes))
        for n in self.nodes():
            for e in n.outedges():
                DM[e.source().id(),e.target().id() ]+= e.strength()
                DM[e.target().id(),e.source().id() ]-= e.strength()
        return numpy.matrix(DM)
    def laplacianmatrix(self):
        return self.degreematrix()-self.weightmatrix()
    def normalizedlaplacianmatrix(self):
        dm12=self.degreematrix()
        dm12=scipy.pow(dm12,-0.5)
        return numpy.eye(self._numnodes)-dm12* self.symmetrized_weight_matrix() * dm12
    def randomwalkpseudolaplacianmatrix(self):
        return numpy.eye(self._numnodes)-self.inv(self.degreematrix)*self.symmetrized_weight_matrix()
    def dualgraph(self):
        return graph_node_edge_lists(self.edges(),
                                     ( filter(lambda e,f: e.target() == f.source(), [ (e,f) for e in self.edges() for f in self.edges()  ]  ) )
                                     )
    def metagraph(self):
        nodes= map(lambda x:x.bo,self.nodes())+map(lambda x:x.bo,self.edges())
        edges=[ (e.source().bo,e.bo) for e in self.edges() ] + [ (e.bo,e.target().bo) for e in self.edges() ]
        return graph_node_edge_lists((nodes,edges))
    def cartesianproduct(self,g):
        return graph_node_edge_lists(( [ (x,y) for x in self.nodes() for y in g.nodes() ],
                                      [ ((x.source(),y.source()),(x.target(),y.target())) for x in self.edges() for y in g.edges() ] ))
    def spanning_tree(self):
        class ST_explorer:
            def __init__(self,v):
                self.v=v
                self.nodes=[]
                self.edges=[]
            def f(self,n):
                self.nodes.append(n.bo)
            def ef(self,e,s,t):
                #print e
                if (not self.v.has_visited(t)):
                    self.edges.append(e)
        v=self.get_visitor()
        ste=ST_explorer(v)
        #explore_graph(self.nodes_extract_f(self.bo), self.node_outedges_f, self.edge_target_f, v, ste.f,ste.ef )
        explore_graph(self.nodes(), lambda n:n.outedges(), lambda e:e.target(), v, ste.f,ste.ef )
        return graph_node_edge_lists((ste.nodes, map(lambda e:(e.source().bo,e.target().bo,e.bo),ste.edges)),
                                      node_attribute_f=self.node_attribute_f,
                                      edge_attribute_f=lambda g,e:self.edge_attribute_f(g,e[2]))
    def spatial_explore(self):
        class SP_explorer:
            def __init__(self,v,basepos):
                self.v=v
		self.pos=basepos
                self.nodes=[]
                self.edges=[]
            def f(self,n):
                self.nodes.append(n.bo)
            def ef(self,e,s,t):
                if (not self.v.has_visited(t)):
                    self.edges.append(e.bo)
        v=self.get_visitor()
        ste=SP_explorer(v)
        #explore_graph(self.nodes_extract_f(self.bo), self.node_outedges_f, self.edge_target_f, v, ste.f,ste.ef )
        explore_graph(self.nodes(), lambda n:n.outedges(), lambda e:e.target(), v, ste.f,ste.ef )
        return graph_node_edge_lists((ste.nodes, ste.edges))
    def topological_sort(self):
        self=g
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
    def symred(self):
        ## return a copy of the graph with only symetric edges
        new_edges=filter(lambda e:e.source().bo in map(lambda x:x.bo,e.target().targets()),self.edges())
        return subgraph(self,new_edges) 

#    def joinproduct(self,g):
#        assert(0)
#        pass
#    def normalizeddegreematrix(self):
#        self.indexnodes()
#        D=numpy.zeros(self._numnodes,self._numnodes)
#        for n in nodes():
#            for e in n.outedges():
#                D[e.destination().id(), e.source().id() ]-= e.strengh()
#                D[e.destination().id(),e.destination().id() ]+= e.strengh()

#########################################################################################################
## Utility functions to create standard type of graphs
#########################################################################################################

def tree_leaves(t):
    l=[t[0]]
    if t[1]:
        for e in t[1]:
            l.extend(tree_leaves(e))
    return l

def tree_branches(t):
    l=[]
    for e in t[1]:
        l.append((t[0],e[0]))
    for e in t[1]:
        l.extend(tree_branches(e))
    return l

def tree_findnode(t,n):
    if (t[0]==n):
        return t
    if (t[1]):
        for e in t[1]:
            r=tree_findnode(e,n)
            if (r):
                return r
    return None

def tree_nodeoutbranches(t):
    if not t:
        return []
    l=[]
    if t[1]:
        for e in t[1]:
            l.append((t[0],e[0]))
    return l


def fct_del(l,v):
    #del l[v]
    l.pop(v)
    return l

def fct_delall(l,v):
    try:
        while True:
            i=l.index(v)
            l.pop(i)
            return l
    except:
        pass


def fct_append(l,v):
    l.append(v)
    return l


#######################################################################################
## Create graphs objects from usual graph representation
#######################################################################################


def subgraph(og,edges):
    return Graph(og,
                 nodes_extract_f=(lambda g:og.nodes()),   ### obtenir les noeuds d un graphe
                 edges_extract_f=(lambda g:edges),   ###
                 node_outedges_f=(lambda g,n:filter(lambda e:e.source().bo==n.bo,edges)),   ###
                 node_inedges_f=(lambda g,n:filter(lambda e:e.target().no==n.bo,edges)),   ###
                 edge_target_f=(lambda g,e:e.target()),   ###
                 edge_source_f=(lambda g,e:e.source()),   ###
                 edge_strength_f=(lambda g,e:e.strength()),    ###
                 nodeid_f=(lambda g,n:n.id()),   ###
                 edgeid_f=(lambda g,e:edges.index(e)),   ###
#                 add_node_f=(lambda g,n:(fct_append(g[0],n),g[1])),   ###
#                 remove_node_f=None
#                 add_edge_f=None
#                 remove_edge_f=None
                 node_repr_f=(lambda g,n:repr(n)),
                 node_attribute_f=lambda g,n:n.attributes(),
                 edge_attribute_f=lambda g,e:e.attributes()
                 )

def graph_node_edge_lists(initgraph=None,xnode_repr_f=repr,node_attribute_f=None, edge_attribute_f=None):
    """ very naive graph implementation (nodes are simple datatypes, edges directly refer to nodes)"""
    if (not initgraph):
        initgraph=([],[])
    return Graph(initgraph,
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
                 remove_node_f=(lambda g,n:(fct_delall(g[0],n),g[1])),
                 add_edge_f=(lambda g,s,d,st:(g[0],fct_append(g[1],(s,d)))),
                 remove_edge_f=(lambda g,s,d:(g[0],fct_delall(g[1],(s,d)))),
                 node_repr_f=(lambda g,n:xnode_repr_f(n)),
                 node_attribute_f=node_attribute_f or (lambda g,n:[]),
                 edge_attribute_f=edge_attribute_f or (lambda g,e:[])
                 )

def graph_decorated_node_edge_lists(initgraph=None,xnode_repr_f=repr,node_attribute_f=None, edge_attribute_f=None):
    """ very naive graph implementation (nodes are tuples of id, attributes, edges are sid,destid,attributes)"""
    if (not initgraph):
        initgraph=([],[])
    return Graph(initgraph,
                 nodes_extract_f=(lambda g:g[0]),   ### obtenir les noeuds d un graphe
                 edges_extract_f=(lambda g:g[1]),   ###
                 node_outedges_f=(lambda g,n:filter(lambda e:e[0]==n[0],g[1])),   ###
                 node_inedges_f=(lambda g,n:filter(lambda e:e[1]==n[0],g[1])),   ###
                 edge_target_f=(lambda g,e:filter(lambda n:n[0]==e[1],g[0])[0]),   ###
                 edge_source_f=(lambda g,e:filter(lambda n:n[0]==e[0],g[0])[0]),   ###
                 edge_strength_f=(lambda g,e:1),    ###
                 nodeid_f=(lambda g,n:g[0].index(n)),   ###
                 edgeid_f=(lambda g,e:g[1].index(e)),   ###
                 add_node_f=(lambda g,n:(fct_append(g[0],n),g[1])),   ###
                 remove_node_f=(lambda g,n:(fct_delall(g[0],n),g[1])),
                 add_edge_f=(lambda g,s,d,st:(g[0],fct_append(g[1],(s,d)))),
                 remove_edge_f=(lambda g,s,d:(g[0],fct_delall(g[1],(s,d)))),
                 node_repr_f=(lambda g,n:xnode_repr_f(n)),
                 node_attribute_f=node_attribute_f or (lambda g,n:[]),
                 edge_attribute_f=edge_attribute_f or (lambda g,e:[])
                 )


def graph_decorated_node_edge_dicts(initgraph=None,xnode_repr_f=repr):
    """ heavy graph implementation"""
    if (not initgraph):
        initgraph=([],[])
    return Graph(initgraph,
                 nodes_extract_f=(lambda g:g[0]),   ### obtenir les noeuds d un graphe
                 edges_extract_f=(lambda g:g[1]),   ###
                 node_outedges_f=(lambda g,n:n[OUTEDGES]),   ###
                 node_inedges_f=(lambda g,n:n[INEDGES]),   ###
                 edge_target_f=(lambda g,e:e[SOURCE]),   ###
                 edge_source_f=(lambda g,e:e[TARGET]),   ###
                 edge_strength_f=(lambda g,e:e[STRENGTH]),    ###
                 nodeid_f=(lambda g,n:n[ID]),   ###
                 edgeid_f=(lambda g,e:e[ID]),   ###
                 add_node_f=(lambda g,n:None),   ###
                 remove_node_f=(lambda g,n:None),
                 add_edge_f=(lambda g,s,d,st:None),
                 remove_edge_f=(lambda g,s,d:None),
                 node_repr_f=(lambda g,n:xnode_repr_f(n))
                 )


def random_graph(nodes=20,edges=50):
    G=graph_node_edge_lists()
    for n in range(nodes):
        G.add_node(n)
    for e in range(edges):
        s,d=random.sample(range(nodes),2)
        G.add_edge(s,d)
    return G

def graph_copy(g,typeofgraph=graph_node_edge_lists):
    gr=typeofgraph()
    for n in g.nodes():
        gr.add_node(n.bo)
    for e in g.edges():
        gr.add_edge(n.bo)
    return gr


def graph_from_tree1(m):
    return Graph(m,
                 nodes_extract_f=tree_leaves,   ### obtenir les noeuds d un graphe
                 edges_extract_f=tree_branches, ###
                 node_outedges_f=(lambda g,n:tree_nodeoutbranches(tree_findnode(g,n))),
                 node_inedges_f=None,
                 edge_target_f=(lambda g,eo:eo[1]),
                 edge_source_f=(lambda g,eo:eo[0]),
                 edge_strength_f=(lambda g,eo:1),
                 nodeid_f=None,
                 edgeid_f=None
                 )



def graph_from_adjacency_matrixX(m):
    return Graph(m,
                 nodes_extract_f=(lambda m:range(m.shape[1])),   ### obtenir les noeuds d un graphe
                 edges_extract_f=(lambda m:map(lambda e:(e[0],e[1]),numpy.transpose(m.nonzero()))), ###
                 node_outedges_f=(lambda m,nsource:map(lambda e:(e,nsource), m[:,nsource].nonzero()[0].tolist())),
                 node_inedges_f=(lambda m,ntarget:map(lambda e:(ntarget,e), m[ntarget,:].nonzero()[0].tolist())),
                 edge_target_f=(lambda m,E:E[0]),
                 edge_source_f=(lambda m,E:E[1]),
                 edge_strength_f=(lambda m,E:m[E[0],E[1]]),
                 nodeid_f=(lambda m,n:n),
                 edgeid_f=(lambda m,E:((E[0]*m.shape[0])+E[1]))
                 )



def graph_from_adjacency_matrix(m):
    return Graph(m,
                 nodes_extract_f=(lambda m:range(m.shape[1])),   ### obtenir les noeuds d un graphe
                 edges_extract_f=(lambda m:map(lambda e:(e[0],e[1]),numpy.squeeze(numpy.transpose(m.nonzero())))), ###
                 node_outedges_f=(lambda m,nsource:map(lambda e:(nsource,e), numpy.squeeze(m[:,nsource].nonzero()[0]).flat)),
                 node_inedges_f=(lambda m,ntarget:map(lambda e:(e,ntarget), numpy.squeeze(m[ntarget,:].nonzero()[0]).flat)),
                 edge_target_f=(lambda m,E:E[1]),
                 edge_source_f=(lambda m,E:E[0]),
                 edge_strength_f=(lambda m,E:m[E[1],E[0]]),
                 nodeid_f=(lambda m,n:n),
                 edgeid_f=(lambda m,E:((E[1]*m.shape[0])+E[0]))
                 )



def graph_from_adjacency_matrix_thresholded(m,t):
    def threshold_func(x):
        if (x<t):
            return 0
        return x
    return Graph(numpy.vectorize(threshold_func)(m),
                 nodes_extract_f=(lambda m:map(lambda n:(m,n),range(m.shape[1]))),   ### obtenir les noeuds d un graphe
                 edges_extract_f=(lambda m:map(lambda e:(m,e[0],e[1]),numpy.transpose(m.nonzero()))), ###
                 node_outedges_f=(lambda (m,n):map(lambda e:(m,n,e), m[:,n].nonzero()[0].tolist())),
                 node_inedges_f=None,
                 edge_target_f=(lambda (m,e,f):(m,f)),
                 edge_source_f=(lambda (m,e,f):(m,e)),
                 edge_strength_f=(lambda (m,e,f):m[e,f]),
                 nodeid_f=(lambda (m,n):n),
                 edgeid_f=(lambda (m,e,f):(e*m.shape[0]+f))
                 )


##
## standard attribute mapping
##

dim_palette=["black", "blue", "green", "yellow"]
tlpdim_palette=[(0,0,0), (0,0,255), (0,255,0), (255,255,0)]

dot_edge_std_attribute_mapping={
    'dim':   lambda g, e, v: ("color=\"%s\""%dim_palette[v]),
    'image': lambda g, e, v: ("image=\"%s\""%(v))
    }

dot_node_std_attribute_mapping={
    'dim':   lambda g, e, v: ("color=\"%s\""%dim_palette[v]),
    'image': lambda g, e, v: ("image=\"%s\""%(v))
    }


def tmpimgfile(pat,rp):
    import time,random,numpy
    from pycvf.lib.graphics.imgfmtutils import NumPy2PIL
    pat=pat.astype(float)
    pat*=255
    filename=(rp+"/temp_pattern_%f_%f.png")%(time.time(),random.random())
    NumPy2PIL(pat.astype(numpy.uint8)).save(filename)
    return filename

tlp_node_std_attribute_mapping={
    'dim': [ "viewColor", "color", lambda g, e, v,rp: ("(%d,%d,%d,255)"%tlpdim_palette[v]) ,  "(255, 0, 0,255)"],
    'label':["ViewLabel",  "string", lambda g, e, v,rp: str(v),  ""],
    'pattern': ["viewTexture",  "string",  lambda g, e, v,rp: tmpimgfile(v,rp),  ""],
    'proba': ["viewMetric",  "double",  lambda g, e, v,rp: str(v),  "0."]
}

tlp_edge_std_attribute_mapping={
    'dim':   [ "viewColor", "color", lambda g, e, v,rp: ("(%d,%d,%d,255)"%tlpdim_palette[v]) ,  "(255, 0, 0,255)"],
    'proba': ["viewMetric",  "double",  lambda g, e, v,rp: str(v),  "0."]
    #'strength':   [ "viewColor", "color", lambda g, e, v: ("(%d,%d,%d)"%(v*255,v*255,v*255)) ,  "(0, 0, 0)"],
}


#def graph_for_tree(m):

# averga number of connected components in a graph
# [ (numpy.array([ len(jg.random_graph(10,k).maximal_connected_components()) for x in range(1000) ])).mean() for k in range(1,20) ]
