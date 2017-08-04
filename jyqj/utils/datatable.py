#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import json


class DTCols(object):
    def __init__(self, cols):
        self._cols = []
        self._cols_name = []
        for col in cols:
            cp_col = copy.deepcopy(col)
            if 'data' not in cp_col:
                cp_col['data'] = cp_col['name']
            self._cols.append(cp_col)
            self._cols_name.append(cp_col['name'])

    def to_json(self):
        return json.dumps(self._cols)

    def to_list(self):
        return self._cols

    def index(self, name):
        return self._cols_name.index(name)

    def __getattr__(self, key):
        if key in self._cols_name:
            return self._cols[self.index(key)]
        else:
            raise AttributeError
