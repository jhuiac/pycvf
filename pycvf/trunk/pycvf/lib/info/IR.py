"""
This files contains element relative to information retrievial

"""

def precision(idx,query,revelantset,NMAX=None):
   res=idx.query(query,NMAX)
   resN=len(res)
   return   len(set(res).intersection( set(revelantset(query)))) / resN
   
def recall(idx,query,revelantset,NMAX=None):
   res=idx.query(query,NMAX)
   rset=set(revelantset(query))
   resN=len(res)
   return   len(set(res).intersection(reset)) / resN

def Fmeasure(idx,query,revelantset,NMAX=None,beta=1):
    p=precision(idx,query,revelantset,NMAX)
    r=recall(idx,query,revelantset,NMAX)
    F=((1+beta**2)*p*r)/(beta**2*p+r)
    
def average_precision(idx,query,revelantset,NMAX):
    rset=set(revelantset(query))
    return sum([ precision(r) * relevance(r) for r in range(N)] )/len(rset)
    
