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
        self.__template__()
        return self._str

    def __template__(self):
        if not self._str.startswith("["):
            self._str = "\"" + self._str
        else:
            self._str = self._str.lstrip("[")
        if not self._str.endswith("]"):
            self._str = self._str + "\""
        else:
            self._str = self._str.rstrip("]")
        self._str = self._str.replace("[", "\"+").replace("]", "+\"")
