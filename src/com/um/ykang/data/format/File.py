# -*- coding:UTF-8 -*-
import gzip
from com.um.ykang.data.format.Line import SepLine, RegExpLine, JsonLine

class LineFile(object):
    def __init__(self):
        self._fhandle = None
    
    def open(self, srcPath, mode, flag):
        if self._fhandle != None:
            self._fhandle.close()
        
        if mode == 'gzip':
            self._fhandle = gzip.open(srcPath, flag)
        if mode == 'txt':
            self._fhandle = open(srcPath, flag)
        return self
    
    def __iter__(self):
        return self
    
    def next(self):
        line = self._fhandle.readline()
        if line != '':
            return line
        else:
            raise StopIteration
        
    def close(self):
        self._fhandle.close()
        self._fhandle = None

class SepFile(LineFile):
    def __init__(self, sep):
        super(SepFile, self).__init__()
        self.sep = sep
        
    def next(self):
        line = self._fhandle.readline()
        if line != '':
            return SepLine(line).format(self.sep)
        else:
            raise StopIteration

class RegExpFile(LineFile):
    def __init__(self, regExp):
        super(RegExpFile, self).__init__()
        self.__regExp = regExp
    def next(self):
        line = self._fhandle.readline()
        if line != '':
            return RegExpLine(line).format(self.__regExp)
        else:
            raise StopIteration

class JsonFile(LineFile):
    def __init__(self):
        super(JsonFile, self).__init__()
    
    def next(self):
        line = self._fhandle.readline()
        if line != '':
            return JsonLine(line).format()
        else:
            raise StopIteration
