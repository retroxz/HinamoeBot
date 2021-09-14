#!/usr/bin/env python
# -*-coding:utf-8 -*-


class BasePluginConfig:

    def keys(self):
        variables = vars(self)
        keys_list = []
        for var_name in variables:
            if variables[var_name]:
                keys_list.append(var_name)
        return keys_list

    def __getitem__(self, item):
        return getattr(self, item)



