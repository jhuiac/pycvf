# -*- coding: utf-8 -*-
from pycvf.framework03.core.genericmodels import GenericModel

class NaiveModel(GenericModel):
  processing=[lambda x:x]
  