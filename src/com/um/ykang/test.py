'''
Created on Apr 12, 2016

@author: root
'''
from com.um.ykang.mission.MissionConf import MissionConf
from com.um.ykang.mission.MissionContext import MissionContext

mconf = MissionConf().setAppName('test')
(msc, app) = MissionContext(conf=mconf).getFolder()
msc.getSample('s3://datamining.ym/dmuser/ykang/results/test2/part-00000.gz', 20).getEmrFile()