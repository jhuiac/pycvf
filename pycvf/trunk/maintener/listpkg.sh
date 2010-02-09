#!/bin/sh
find -type d  | grep pycvf |  tr "/" "." | cut -c 3- | awk "{printf (\"'%s',\n\",\$1);}"
