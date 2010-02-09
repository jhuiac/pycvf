#!/bin/bash

pycvf_model_features_view   -m "free('255-x[:,:,0]')|(LF('pycvf.models.image.morpho.edt')|(LF('pycvf.models.image.segment.watershed')|LF('pycvf.models.image.normalize')))"  -i 1

pycvf_model_features_view   -m "free('x[:,:,0]')|(LF('pycvf.models.image.morpho.edt')|(LF('pycvf.models.image.segment.watershed')|LF('pycvf.models.image.normalize')))"  -i 1

