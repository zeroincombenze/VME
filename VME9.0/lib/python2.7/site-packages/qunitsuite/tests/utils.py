# -*- coding: utf-8 -*-
import os

ROOT = os.path.abspath(os.path.dirname(__file__))
def path_to(*fpath):
    return os.path.join(ROOT, 'testfiles', *fpath)
