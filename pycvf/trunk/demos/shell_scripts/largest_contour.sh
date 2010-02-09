 #!/bin/bash
 
 D=/databases/altpics/06_animal/
 pycvf_model_features_view --db "image.directory('$D',rescale=(320,200,'T'))"\
   -m "LF('pycvf.models.image.gray')|(LF('pycvf.models.free','x>127')|(LF('pycvf.models.image.normalize') |(LF('pycvf.models.image.edges.largest_contour')|(LF('pycvf.models.free','numpy.array(x)',id='2')|LF('pycvf.models.image.plot.contour')))))" -i 1