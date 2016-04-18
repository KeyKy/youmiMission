import numpy
import os
import gzip
from scipy.sparse import csc_matrix
from sklearn import svm
from com.um.ykang.lookalike.entity.Candidate import Candidate
from com.um.ykang.lookalike.entity.Qpackage import Qpackage
from com.um.ykang.lookalike.entity.QUser import Quser
import gc
from com.um.ykang.data.CrossValid import crossValidSplit
import random

class OneClassSVM(object):
    def __init__(self):
        self.model = None
    
    @staticmethod
    def sparseX(qUserPath, qPackageToId, mask=None):
        row = []
        col = []
        val = []
        users = {}
        idx = 0
        for file_ in os.listdir(qUserPath):
            f = gzip.open(qUserPath+os.sep+file_, mode='rb')
            for line in f:
                spl = line.strip().split('|')
                username = spl[0]
                if mask != None:
                    if username in mask:
                        for i in range(1, len(spl)):
                            sp = spl[i].split(':')
                            if sp[0] in qPackageToId:
                                row.append(idx)
                                col.append(qPackageToId[sp[0]])
                                val.append(int(sp[1]))
                    users[username] = idx
                    idx += 1
                else:
                    for i in range(1, len(spl)):
                        sp = spl[i].split(':')
                        if sp[0] in qPackageToId:
                            row.append(idx)
                            col.append(qPackageToId[sp[0]])
                            val.append(int(sp[1]))
                    users[username] = idx
                    idx += 1
            f.close()
        
        
        sparseX = csc_matrix((val, (row, col)), shape=(len(users), len(qPackageToId.keys())))
        return sparseX, users
    
    def train(self, sparseX, **kargv):
        print 'Info: Training One-Class-SVM'
        self.model = svm.OneClassSVM(kernel=kargv['kernel'], gamma=kargv['gamma'], nu=kargv['nu'])
        self.model.fit(sparseX)
    
    @staticmethod
    def sparsePX(candPartPath, qPackageToId, mask=None):
        row = []
        col = []
        val = []
        users = {}
        idx = 0
        f = gzip.open(candPartPath, mode='rb')
        for line in f:
            spl = line.strip().split('|')
            username = spl[0]
            if mask != None:
                if username not in mask:
                    for i in range(1, len(spl)):
                        sp = spl[i].split(':')
                        row.append(idx)
                        col.append(qPackageToId[sp[0]])
                        val.append(int(sp[1]))
                    users[username] = idx
                    idx += 1
            else:
                for i in range(1, len(spl)):
                    sp = spl[i].split(':')
                    row.append(idx)
                    col.append(qPackageToId[sp[0]])
                    val.append(int(sp[1]))
                users[username] = idx
                idx += 1
        f.close()
        
        sparsePX = csc_matrix((val, (row, col)), shape=(len(users), len(qPackageToId.keys())))
        return sparsePX, users
    
    def predict(self, sparsePX):
        print 'Info: predicting'
        return self.model.predict(sparsePX)
    

if __name__ == '__main__':
    #candToId = Candidate.getCandidateToId()
    qPackageToId = Qpackage.getQpackageToId()
    sparseX, users = OneClassSVM.sparseX(Quser.QUSER_OPENPACKAGE_PATH, qPackageToId)
    sparsePX, cands = OneClassSVM.sparsePX(Candidate.PART_FILE_NAME[0], qPackageToId, mask=users)
    
    avgErrorRate = 0
    times = 0
    model1 = OneClassSVM()
    for (trainSlice, testSlice) in crossValidSplit(len(users.keys())):
        print 'predicting slice ' + str(times)
        model1.train(sparseX[trainSlice,:], kernel='rbf', gamma=0.001, nu=0.7)
        res = model1.predict(sparseX[testSlice, :])
        sampleNum = random.sample(range(len(cands.keys())), int(0.01*len(cands.keys())))
        res2 = model1.predict(sparsePX[sampleNum, :])
        groundTruePostive = res[res == 1].size
        groundTrueNegative = res[res == -1].size
        
        candPostive = res2[res2 == 1].size
        candNegative = res2[res2 == -1].size
        
        precision = groundTruePostive * 1.0 / (groundTruePostive + candPostive)
        recall = groundTruePostive * 1.0 / (groundTrueNegative + groundTruePostive)
        print groundTruePostive, groundTrueNegative, candPostive, candNegative
        print 'precision = %f' % precision
        print 'recall = %f' % recall 
        print 'candPostiveRatio = %f' % (candPostive * 1.0 / len(sampleNum))
        break
    #print avgErrorRate / times
    
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        