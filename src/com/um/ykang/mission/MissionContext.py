import os
from com.um.ykang.mission import MNode
from com.um.ykang.util.BashUtil import BashUtil



class MissionContext:
    def __init__(self, conf):
        self.conf = conf
    
    def __isUnderWorkSpace(self, appPath):
        return MNode.isUnder(appPath, self.conf.getWorkSpace())
    
    def getFolder(self):
        appPath = self.conf.getAppPath()
        if self.__isUnderWorkSpace(appPath):
            return (self, appPath)
        else:
            os.mkdir(appPath)
            return (self, appPath)
    
    def getSample(self, s3SrcPath, headN, recursived=False):
        appPath = self.conf.getAppPath()
        tmpFile = self.conf.getTmpFile()
        if recursived:
            BashUtil.s3Cp(s3SrcPath, appPath, True)
        else:
            srcFilename = os.path.basename(s3SrcPath)
            dstPath = appPath + os.sep + srcFilename
            if os.path.exists(dstPath):
                print 'WRAN: downloading from s3, but file existed'
                BashUtil.subl(tmpFile)
                return self
            else:
                BashUtil.s3Cp(s3SrcPath, dstPath, False)
                [name, ext] = os.path.splitext(srcFilename)
                if ext == '.gz':
                    BashUtil.gzipDecompress(dstPath)
                    BashUtil.head(headN, appPath + os.sep + name, tmpFile)
                    BashUtil.subl(tmpFile)
                elif ext == '.txt':
                    BashUtil.head(headN, dstPath, tmpFile)
                    BashUtil.subl(tmpFile)
                else:
                    BashUtil.head(headN, dstPath, tmpFile)
                    BashUtil.subl(tmpFile)
        return self
    
    def getEmrFile(self):
        codePath = self.conf.getCodePath()
        codeTemplate = self.conf.getCodeTemplate()
        codeFile = self.conf.getCodeFile()
        gitPath = self.conf.getGitPath()
        if os.path.exists(codePath):
            if os.path.exists(codeTemplate):
                BashUtil.move(codeTemplate, codeFile)
            BashUtil.subl(codeFile)
        else:
            BashUtil.gitClone(gitPath, codePath)
            BashUtil.move(codeTemplate, codeFile)
            BashUtil.subl(codeFile)
        return self
    
    def submit(self, mem='3G', coreN='4', taskN='3', coreMulti='1'):
        os.system(' '.join(['cd', self.conf.getCodePath(), '&&', \
                             './'+self.conf.getEmrFile(), self.conf.getAppName(),\
                              mem, coreN, taskN, coreMulti]))
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    

