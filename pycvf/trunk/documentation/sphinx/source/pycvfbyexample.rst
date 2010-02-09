PyCVF by Example
================

Command line programs
---------------------

Browsing databases
^^^^^^^^^^^^^^^^^^

Display default database:: 

  python_dbshow


Displaying the content of a directory:: 

  python_dbshow --db 'image.directory(select_existing_folder())'


Note that the argument of "--db" is a python expression, that is normally evaluated by using a lazy autoloader for modules.
This one is sometime buggy. You may then use the "LF" command with a complete path::

  python_dbshow --db 'LF('pycvf.databases.image.directory',select_existing_folder())'

Extract all 'tomato' image from yahoo image and divide each image into 9 pieces:: 

  python_dbshow --db "exploded(image.yahoo('tomato'),pycvf.structures.spatial.Subdivide((3,3,1)))"

If you don't remember the name of your database you may always use:: 

  python_dbshow --db "interactive()"

For complex databases that you use often you may create new database file to implement them::

  from pycvf.databases.image import directories
  from pycvf.databases import limit
  from pycvf.datatypes import image

  D="/databases/101ObjectCategories/PNGImages/"
  datatype=lambda:image.Datatype
  __call__=lambda:directories.__call__(D,dbop=lambda x:limit.__call__(x,30),rescale=(256,256,'T'))


Using models
^^^^^^^^^^^^

If you want to compute and visualzie the HOG descriptors of the image in a folder you may do ::

  python_model_features_show --db 'image.directory(select_existing_folder())' --model 'image.descriptors.HOG()'


You may save the result of this computation by using "pycvf_compute_features" ::

  pycvf_compute_features --db 'image.directory(select_existing_folder())' --model 'image.descriptors.HOG()' -t "trackHOG.tf"


The **free** model allow you to manipulate data in python directly::

  pycvf_compute_features --db 'image.directory(select_existing_folder())' --model 'free("scipy.stats.entropy(x**2)")' -t "trackfile.tf"


Models maybe combined together using the keyword "PL" or the operator | (beware that the operator "|" in python has not the good precedence in parsing, so for long pipes use PL)::

  python_model_features_show --db 'image.directory(select_existing_folder())' --model 'free("x**2")|(image.edges.laplace()|free("x**.5"))' 
  python_model_features_show--db 'image.directory(select_existing_folder())' --model 'PL(free("x**2"),image.edges.laplace(),free("x**.5")'


Computing indexes
^^^^^^^^^^^^^^^^^

First example : 

  pycvf_build_index -s "std"
  

More 
^^^^

Have a look at the demo folder in your PyCVF directory.



