# -*- coding:UTF-8 -*-
import os 

class BashUtil(object):
    @staticmethod
    def head(headN, src, dst):
        command = 'head'
        parms = '-n'
        streamSign = '>'
        os.system(' '.join([command, parms, str(headN), src, streamSign, dst]))
    
    @staticmethod
    def subl(src):
        command = 'subl'
        os.system(' '.join([command, src]))
    
    @staticmethod
    def s3Cp(src, dst, recursived=False):
        command = 'aws s3 cp'
        if recursived:
            os.system(' '.join([command, src, dst, '--recursive']))
        else:
            os.system(' '.join([command, src, dst]))
    @staticmethod
    def gzipDecompress(src):
        command = 'gzip'
        parms = '-dvk'
        os.system(' '.join([command, parms, src]))
    
    @staticmethod
    def move(src, dst):
        command = 'mv'
        os.system(' '.join([command, src, dst]))
    
    @staticmethod
    def gitClone(src, dst):
        command = 'git clone'
        parms = '-v'
        os.system(' '.join([command, parms, src, dst]))
    
        
    
    
    