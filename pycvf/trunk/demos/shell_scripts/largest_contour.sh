 #!/bin/bash
 
D=/databases/altpics/06_animal/
pycvf_model_features_view --db "image.directory('$D',rescale=(320,200,'T'))"\
   -m "LF('pycvf.nodes.image.gray')|(LF('pycvf.nodes.free','x>127')|(LF('pycvf.nodes.image.normalize') |(LF('pycvf.nodes.image.edges.largest_contour')|(LF('pycvf.nodes.free','numpy.array(x)',id='2')|LF('pycvf.nodes.image.plot.contour')))))" -i 1