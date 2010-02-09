#!/bin/bash

F="src/CMakeFiles/lshkit.dir/mplsh-model.cpp.o  src/CMakeFiles/lshkit.dir/mplsh.cpp.o src/CMakeFiles/lshkit.dir/apost.cpp.o src/CMakeFiles/lshkit.dir/char_bit_cnt.cpp.o  src/CMakeFiles/lshkit.dir/vq.cpp.o src/CMakeFiles/lshkit.dir/kdtree.c.o"

g++ -shared -fPIC  -o ./lib/liblshkit.so $F
