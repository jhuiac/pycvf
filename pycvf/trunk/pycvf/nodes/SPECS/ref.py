from pycvf.core import genericmodel
from pycvf.core.autoimp import *


class Model(genericmodel.Model):
        """
         Nodes or Models are means to transform information.
         
         
         Abstractly each node is assumed to have :
             1 Input
             1 Output 
             1 Set of parametes
            
         This interface constraint is actually not really a constraint since not that much drastic, 
         since user may provide different outputs by outputing tuples. And may get different inputs by inputing
         tuples our using the parameters as inputs.
         
         Note that there exists convenients decorators pycvf_model_function and pycvf_model_class for transforming any function or class into a PyCVF model.
         
         
        """
        def input_datatype(self,x):
            """
            The input datatype function is used to compute and check the declared datatype according to the type coming in as effective input
            """
        def output_datatype(self,x):
            """
            The output datatype function is used to compute and check the declared datatype according to the type coming in as effective input
            """            
            return (self.type_out if (self.type_out!=None) else x)
        def init_model(self,*args,**kwargs):
            """
            The real initiatlization of a Model are actually done in the init_model function.
            
            Compared to __init__ some global pre-initialization has been made and node have a slighty better idea of what their environement
            will be looking like.
            """
            
__call__=Model
