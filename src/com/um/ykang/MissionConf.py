# -*- coding:UTF-8 -*-
from com.um.ykang.Constance import Constance
import os

class MissionConf:
    def __init__(self):
        self.__workspace = Constance.WORK_SPACE
        self.__gitPath = Constance.GIT_PATH
        self.__appName = None
        self.__appPath = None
        self.__codePath = None
        self.__codeFile = None
        self.__codeTemplate = None
        self.__tmpFile = None
        self.__emrFile = None
        
    def setAppName(self, appName):
        self.__appName = appName
        self.__appPath = self.__workspace + os.sep + appName
        self.__codePath = self.__appPath + os.sep + 'code'
        self.__codeFile = self.__codePath + os.sep + self.__appName + '.py'
        self.__codeTemplate = self.__codePath + os.sep + 'app.template.py'
        self.__tmpFile = self.__appPath + os.sep + 'tmp.txt'
        self.__emrFile = 'start-spark-job.sh'
        return self
    
    def getWorkSpace(self):
        return self.__workspace
    def getAppName(self):
        return self.__appName
    def getAppPath(self):
        return self.__appPath
    def getCodePath(self):
        return self.__codePath
    def getCodeFile(self):
        return self.__codeFile
    def getCodeTemplate(self):
        return self.__codeTemplate
    def getTmpFile(self):
        return self.__tmpFile
    def getGitPath(self):
        return self.__gitPath
    def getEmrFile(self):
        return self.__emrFile