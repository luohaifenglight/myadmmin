#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Enumeration(object):
    """
    A small helper class for more readable enumerations,
    and compatible with Django's choice convention.
    You may just pass the instance of this class as the choices
    argument of model/form fields.

    Example:
        MY_ENUM = Enumeration([
            (100, 'MY_NAME', 'My verbose name'),
            (200, 'MY_AGE', 'My verbose age'),
        ])
        assert MY_ENUM.MY_AGE == 100
        assert MY_ENUM[1] == (200, 'My verbose age')
    """

    def __init__(self, enum_list):
        """
            enum_list: list[item]
            item[0] 表示实际保存的Value, item[1] 表示可以直接使用的变量, item[2] 表示描述
        """
        self.enum_list = [(item[0],item[1], item[2]) for item in enum_list]
        self.enum_dict = {}
        self.choices = []
        for item in enum_list:
            self.enum_dict[item[1]] = item[0]
            self.choices.append([item[0], item[2]])

    def __contains__(self, v):
        return (v in self.enum_list)

    def __len__(self):
        return len(self.enum_list)

    def __getitem__(self, v):
        # 如果v是字符串，那么给定 变量名，得到实际的Value
        import string
        if isinstance(v, string):
            return self.enum_dict[v]
        elif isinstance(v, int):
            # 如果v是int, 则得到(Value, ValueDesc)
            return self.enum_list[v]

    def __getattr__(self, name):
        return self.enum_dict[name]

    def __getdesp__(self, key):
        # 获取Value的描述
        for item in self.enum_list:
            if item[0] == key:
                return item[2]

    def getDesc(self, key, defaultValue=None):
        # 获取Value的描述
        for item in self.enum_list:
            if item[0] == key:
                return item[2]
        else:
            return defaultValue

    def getKey(self, key, defaultValue=None):
        for item in self.enum_list:
            if item[0] == key:
                return item[1]

    def __iter__(self):
        return self.enum_list.__iter__()

    def get_key_from_desc(self, desc):
        for item in self.enum_list:
            if item[2] == desc:
                return item[0]

    def result(self, code):
        return {"error": code, "message": self.getDesc(code)}
