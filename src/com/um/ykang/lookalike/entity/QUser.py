# -*- coding:UTF-8 -*-
from com.um.ykang.data.format.File import SepFile, LineFile

class Quser(object):
    QUSER_ID_TXT = '/root/Downloads/look-alike/data/dict/qUserToId.txt'
    TOTAL_QUSER_TXT = '/root/Downloads/look-alike/data/payQualityUsers/payQualityUsers.txt'
    QCUSTOM_OPENPACKAGE_PATH = '/root/Downloads/look-alike/data/qCustomerOpenPackageInfo'
    
    @staticmethod
    def writeQuserToId():
        qUser = set()
        f = SepFile(',').open(Quser.TOTAL_QUSER_TXT, 'txt', 'r')
        for line in f:
            username = 'imei=' + line[0]
            if len(line[0]) == 0 and len(line[1]) != 0:
                username = 'ifa=' + line[1]
            qUser.add(username)
        qUser = list(qUser)
        f.close()
        
        f = LineFile().open(Quser.QUSER_ID_TXT, 'txt', 'w')
        for i in range(len(qUser)):
            f.writeLine(qUser[i] + '|' + str(i))
        f.close()
        
    @staticmethod
    def getQuserToId(mask=None):
        qUserToId = {}
        f = SepFile('|').open(Quser.QUSER_ID_TXT, 'txt', 'r')
        for line in f:
            if mask == None:
                qUserToId[line[0]] = line[1]
            else:
                if line[0] in mask:
                    qUserToId[line[0]] = line[1]
        f.close()
        return qUserToId
    
    @staticmethod
    def getIdToQuser(mask=None):
        idToQuser = {}
        f = SepFile('|').open(Quser.QUSER_ID_TXT, 'txt', 'r')
        for line in f:
            if mask == None:
                idToQuser[line[1]] = line[0]
            else:
                if line[1] in mask:
                    idToQuser[line[1]] = line[0]
        f.close()
        return idToQuser


if __name__ == '__main__':
#     user = set()
#     f = SepFile(',').open('/root/Downloads/look-alike/data/payQualityUsers/payQualityUsers.txt', 'txt', 'r')
#     for line in f:
#         username = line[0]
#         if len(line[0]) == 0 and len(line[1]) != 0:
#             username = line[1]
#         user.add(username)
#     f.close()
#     print len(user)
    print 'return'


        