Databases
=========

One of the main concept of PyCVF is the concept of **database**.

All database must inherit from **pycvf.core.database.ContentsDatabase**.

.. autoclass:: pycvf.core.database.ContentsDatabase
  :members:

 

Abstract Database Type
-----------------------


.. autoclass:: pycvf.databases.SPECS.ref.DB
 :members: __init__, __iter__, __len__, keys(), values(), items()
 
Existing Databases
==================

Work under progress...

Metadatabase
------------


.. autoclass:: pycvf.databases.from_trackfile.DB

.. autoclass:: pycvf.databases.transformed.DB

.. autoclass:: pycvf.databases.exploded.DB

.. autoclass: pycvf.databases.aggregated_database.DB

.. class: pycvf.databases.interactive.DB

.. autoclass: pycvf.databases.limit.DB

.. autoclass: pycvf.databases.filtered.DB

Vector Databases
-----------------

.. pycvf.databases.vectors.clustered_points.DB


Image related database
----------------------


.. autoclass:: pycvf.databases.image.directory.DB

.. autoclass:: pycvf.databases.image.directories.DB

.. autoclass: pycvf.databases.image.imagenet.DB

.. autoclass: pycvf.databases.image.yahoo_image.DB

.. autoclass: pycvf.databases.image.pdf.DB

.. autoclass: pycvf.databases.image.flickr.DB

.. autoclass: pycvf.databases.image.labelme.DB

.. autoclass: pycvf.databases.image.kanji.DB

.. autoclass: pycvf.databases.image.math.noise.DB

.. autoclass: pycvf.databases.image.math.xytexpr.DB

Image related pseudodatabase
-----------------------------

.. autoclass: pycvf.databases.image.v4l.DB

.. autoclass: pycvf.databases.image.v4l2.DB


Video related database
----------------------

.. autoclass: pycvf.databases.video.directory.DB

.. autoclass: pycvf.databases.video.shots_of.DB

.. autoclass: pycvf.databases.video.youtube.DB

.. autoclass: pycvf.databases.video.tv2007concept.DB


