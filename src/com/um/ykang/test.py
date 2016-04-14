# 
# from com.um.ykang.mission.MissionConf import MissionConf
# from com.um.ykang.mission.MissionContext import MissionContext
# 
# mconf = MissionConf().setAppName('test')
# (msc, app) = MissionContext(conf=mconf).getFolder()
# msc.getSample('s3://datamining.ym/dmuser/ykang/results/test2/part-00000.gz', 20).getEmrFile()
from com.um.ykang.data.format.File import SepFile
import os

# writer = open('/root/test.txt', 'w')
# writer.writelines('123')
# writer.close()

f = SepFile('\t').open('/home/bk25103378/dataExchangeYiGuan/overlap_full_label.txt', 'txt', 'r')
writer = open('/home/bk25103378/dataExchangeYiGuan/label.txt', 'w')
for line in f:
    writer.write(line[2] + '\t' + line[3].strip() + os.linesep)
writer.close()