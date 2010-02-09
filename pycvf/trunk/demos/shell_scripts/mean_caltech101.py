#!/bin/bash
D=/databases/101ObjectCategories/PNGImages/
pycvf_model_features_view --db "imageset.directory('$D',rescale=(200,200,'T'))" \
                          --model 'free("numpy.concatenate(map(lambda x:x.reshape(x.shape+(1,)),list(x)),axis=3).mean(axis=3).squeeze().astype(numpy.uint8)",datatype=pycvf.datatypes.image.Datatype)|image.save("out-$address.png")'
                                   
pycvf_model_features_view --db "imageset.directory('$D',rescale=(200,200,'T'))" \
                          --model 'exploded_transform(image.edges.laplace(),recompose=True)'\
                                  '|free("numpy.concatenate(map(lambda x:x.reshape(x.shape+(1,)),list(x)),axis=3).mean(axis=3).squeeze().astype(numpy.uint8)",'\
                                        'datatype=pycvf.datatypes.image.Datatype)'\
                                   '|image.save("oute-$address.png")'
 