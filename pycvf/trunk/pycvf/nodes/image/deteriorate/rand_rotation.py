from pycvf.nodes.image import map_coordinates

def rand_rotation(amount=30,random_generator=lambda amount:numpy.random.normal(0,amount/100*numpy.pi)):
    return map_coordinates.__call__("x*numpy.exp(1J*%f)"%(random_generator(amount=30)))

Model=rand_rotation
__call__=Model
