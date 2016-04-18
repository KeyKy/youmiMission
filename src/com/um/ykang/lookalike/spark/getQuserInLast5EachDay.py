from com.um.ykang.mission.MissionConf import MissionConf
from com.um.ykang.mission.MissionContext import MissionContext


if __name__ == '__main__':
    mconf = MissionConf().setAppName('getQuserInLast5EachDay')
    msc = MissionContext(conf=mconf)
    msc.getFolder()
    msc.getSample('s3://datamining.ym/user_profile/last5/2016-04-14/part-00000.gz', 10, recursived=False)
    msc.getEmrFile()
    msc.submit(mem='3G', coreN='5', taskN='2', coreMulti='2')