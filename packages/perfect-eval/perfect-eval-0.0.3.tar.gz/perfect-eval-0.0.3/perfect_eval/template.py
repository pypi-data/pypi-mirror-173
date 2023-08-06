# -*-coding:utf-8-*-
# Author: Eason.Deng
# Github: https://github.com/holbos-deng
# Email: 2292861292@qq.com
# CreateDate: 2022/10/28 15:52
# Description:

class Tmpl:
    _str = ""

    def __init__(self, string):
        self._str = string

    def expr(self):
        return self.__template__()

    def __template__(self):
        string = self._str
        if not string.startswith("["):
            string = "\"" + string
        else:
            string = string.lstrip("[")
        if not string.endswith("]"):
            string = string + "\""
        else:
            string = string.rstrip("]")
        string = string.replace("[", "\"+").replace("]", "+\"")
        return string
