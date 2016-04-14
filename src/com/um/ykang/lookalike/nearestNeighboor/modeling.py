# -*- coding:UTF-8 -*-
import os
from scipy.sparse import csc_matrix
from sklearn.neighbors.unsupervised import NearestNeighbors
import gzip
from com.um.ykang.lookalike.entity.Candidate import Candidate
from com.um.ykang.lookalike.entity.Qpackage import Qpackage
from com.um.ykang.lookalike.entity.QUser import Quser
from com.um.ykang.data.CrossValid import crossValidSplit
import gc

class NearestNeighboor(object):
    def __init__(self):
        self.model = None
    #preprocessing, featuring, training, predicting, parsing, evaluation
    @staticmethod
    def sparseX(candPartPath, qUserPath, candToId, qPackageToId, matShape):
        row = []
        col = []
        val = []
        for file_ in os.listdir(qUserPath):
            f = gzip.open(qUserPath+os.sep+file_, mode='rb')
            for line in f:
                spl = line.strip().split('|')
                username = spl[0]
                if username not in candToId:
                    continue
                for i in range(1, len(spl)):
                    sp = spl[i].split(':')
                    if sp[0] in qPackageToId:
                        row.append(candToId[username])
                        col.append(qPackageToId[sp[0]])
                        val.append(int(sp[1]))
            f.close()
        
        f = gzip.open(candPartPath, mode='rb')
        for line in f:
            spl = line.strip().split('|')
            username = spl[0]
            for i in range(1, len(spl)):
                sp = spl[i].split(':')
                row.append(candToId[username])
                col.append(qPackageToId[sp[0]])
                val.append(int(sp[1]))
        f.close()
        
        sparseX = csc_matrix((val, (row, col)), shape=matShape)
        return sparseX
    
    def train(self, sparseX, **kargv):
        print 'Info: Training KNN'
        if 'algorithm' not in kargv:
            self.model = NearestNeighbors(kargv['topK'], metric=kargv['metric'])
        else:
            self.model = NearestNeighbors(kargv['topK'], metric=kargv['metric'], algorithm=kargv['algorithm'])
        self.model.fit(sparseX)
    
    def predict(self, sparsePX):
        pred = self.model.kneighbors(sparsePX, return_distance = True)
        dist = pred[0]
        idx = pred[1]
        return (dist, idx)

if __name__ == '__main__':
    candToId = Candidate.getCandidateToId()
    qPackageToId = Qpackage.getQpackageToId()
 
    sparseX = NearestNeighboor.sparseX(Candidate.PART_FILE_NAME[0], 
                                             Quser.QCUSTOM_OPENPACKAGE_PATH, 
                                             candToId, qPackageToId, 
                                             (len(candToId.keys()),len(qPackageToId.keys())))
     
    qUserToId = Quser.getQuserToId()
    qUserInCand = set([i for i in qUserToId.keys() if i in candToId])
    del candToId, qPackageToId
    gc.collect()
    qUserInCandToId = Candidate.getCandidateToId(qUserInCand)
    qUserInCand = list(qUserInCand)
    model1 = NearestNeighboor()
    model1.train(sparseX,topK=100,metric='euclidean')
    start = 0
    for (trainSlice, testSlice) in crossValidSplit(len(qUserInCand)):
        print 'predicting slice ' + str(start)
        writer = open('/root/Downloads/look-alike/data/res/'+str(start)+'.txt','w')
        
        testQUser = [int(qUserInCandToId[qUserInCand[i]]) for i in testSlice]
        testWriter = open('/root/Downloads/look-alike/data/res/t'+str(start)+'.txt','w')
        for tester in testQUser:
            testWriter.write(str(tester) + os.linesep)
        testWriter.close()
        
        trainQUser = [int(qUserInCandToId[qUserInCand[i]]) for i in trainSlice]
        for idx in trainQUser:
            print 'predicting ' + str(idx)
            res = model1.predict(sparseX[idx,:])
            dist = [str(i) for i in res[0][0]]
            topKs = [str(i) for i in res[1][0]]
            for i in range(len(topKs)):
                feats = str(sparseX[int(topKs[i]), :]).split('\n')
                feats = [j.strip() for j in feats]
                writer.write(str(idx) + '&' + dist[i] + '&' + topKs[i] + '&' + '&'.join(feats) + '\n')
            writer.flush()
        writer.close()
        start += 1
    
    
    
    
    
    