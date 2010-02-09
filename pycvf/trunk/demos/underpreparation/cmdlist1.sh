pycvf_dbshow --db "transformed(imgkanji(), pycvf.models.image.laplace())"


pycvf_dbshow --db "exploded(exploded(transformed(video_directory('/usr/share/panda3d/samples/Media-Player/'),pycvf.models.video.images(5)),pycvf.structures.list.DefaultStructure()),pycvf.structures.spatial.Subdivide((2,2,1)))" -A 1 -i 1
