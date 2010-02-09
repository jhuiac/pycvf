#!/bin/bash

timelimit 20 pycvf_model_features_view   -m "free('255-x[:,:,0]')|(LF('pycvf.nodes.image.morpho.edt')|(LF('pycvf.nodes.image.segment.watershed')|LF('pycvf.nodes.image.normalize')))"  -i 1

timelimit 20 pycvf_model_features_view   -m "free('x[:,:,0]')|(LF('pycvf.nodes.image.morpho.edt')|(LF('pycvf.nodes.image.segment.watershed')|LF('pycvf.nodes.image.normalize')))"  -i 1

