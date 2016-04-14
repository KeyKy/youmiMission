# -*- coding:UTF-8 -*-
from com.um.ykang.data.format.File import SepFile, LineFile

class Qpackage(object):
    QPACKAGE_SCORE_TXT = '/root/Downloads/look-alike/data/dict/qPackageToScore.txt'
    QPACKAGE_ID_TXT = '/root/Downloads/look-alike/data/dict/qPackageToId.txt'
    
    @staticmethod
    def writeQpackageToId():
        f = SepFile(':').open(Qpackage.QPACKAGE_SCORE_TXT, 'txt', 'r')
        idx = 0
        writer = LineFile().open(Qpackage.QPACKAGE_ID_TXT, 'txt', 'w')
        for line in f:
            writer.writeLine(line[0] + '|' + str(idx))
            idx += 1
        writer.close()
        f.close()
    
    @staticmethod
    def getQpackageToId(mask=None):
        print 'Info: loading QpackageToId'
        qPackageToId = {}
        f = SepFile('|').open(Qpackage.QPACKAGE_ID_TXT, 'txt', 'r')
        for line in f:
            if mask == None:
                qPackageToId[line[0]] = line[1]
            else:
                if line[0] in mask:
                    qPackageToId[line[0]] = line[1]
        f.close()
        return qPackageToId
    
    @staticmethod
    def getIdToPackage(mask=None):
        idToQpackage = {}
        f = SepFile('|').open(Qpackage.QPACKAGE_ID_TXT, 'txt', 'r')
        for line in f:
            if mask == None:
                idToQpackage[line[1]] = line[0]
            else:
                if line[1] in mask:
                    idToQpackage[line[1]] = line[0]
        f.close()
        return idToQpackage
        
        
        
        
        
        
        
        
        
            