##
## This is aimed at helping the distribution of PyCVF by clarifying the legal terms,
## and by making explicit warning when user is using some software comp

from pycvf.core.errors import *

PYCVFD_REQUIRE_PACKAGE=0
PYCVFD_SPECIFIC_LICENSE=1
PYCVFD_SPECIFIC_ACCEPT_REQUIRED=2

def pycvf_dist(pragma, value):
    if (pragma==PYCVFD_REQUIRE_PACKAGE):
        try:
            __import__(value,fromlist=value.split(".")[-1])
        except:
            pycvf_error("The following package is required : %s "%(value,))            
    if (pragma==PYCVFD_SPECIFIC_LICENSE):
            pycvf_warning("Please note that you are using a non LGPL module : %s"%(value,))        
    elif (pragma==PYCVFD_SPECIFIC_ACCEPT_REQUIRED):        
            pycvf_error("Before to use this file you must accept its license")
    pass