#!/usr/bin/env python3
#coding=utf8

"""
1.接受参数（记录三个文件的路径，并判断文件是否存在）
（错误打印退出）
2.读配置
3.计算社保，计算个税，计算税后（所有计算机结果保留2位小数）
4.结果写入文件


实现过程：配置文件写成配置类
        self._config = {} 来存储每个配置项和值
        获得配置信息的方法可以定义为 def get_config(self)，使用类似 config.get_config('JiShuH')。
员工工资信息：
    员工数据类 UserData，来获取并存储员工数据，
    同样 def __init__(self, userdatafile)
    中定义一个字典 self.userdata = {} 存储文件中读取的用户 ID及工资，
    并实现相应的金额计算的方法def calculator(self)

处理命令行参数的方式：

首先使用 args = sys.argv[1:] 获得所有的命令行参数列表，
即包括 -c test.cfg -d user.csv -o gongzi.csv 这些内容。
使用 index = args.index('-c') 获得 -c 参数的索引，那么配置文件的路径就是 -c 后的参数即 configfile = args[index+1]，
同样，其他的 -d 和 -o 参数也用这种方法获得。

在3基础的改进：增加多进程和queue
在4基础的上改进：
1。使用 getopt 模块处理命令行参数
2.使用 Python3 中的 configparser 模块读取配置文件
3.使用 datetime 模块写入工资单生成时间
"""

import sys
import os
import json
from multiprocessing import Process,Queue
from getopt import getopt
from datetime import datetime
from configparser import ConfigParser
confDict={}

class UserInfor(object):
    def __init__(self,inf,confIns):
        self._infDict=inf
        self._confIns=confIns

    ##计算社保
    def getSheBao(self):
        """
        JiShuL = 2193.00
        JiShuH = 16446.00

        YangLao = 0.08
        YiLiao = 0.02
        ShiYe = 0.005
        GongShang = 0
        ShengYu = 0
        GongJiJin = 0.06
        :return:
        """
        # print (self._confIns.getConfig('YangLao'))
        # print(self._confIns.getConfig('JiShuH'.lower()))

        if self._infDict.get('gongzi')>self._confIns.getConfig('JiShuH'.lower()):
            gongzi=self._confIns.getConfig('JiShuH'.lower())
        elif self._infDict.get('gongzi')<self._confIns.getConfig('JiShuL'.lower()):
            gongzi=self._confIns.getConfig('JiShuL'.lower())
        else:
            gongzi=self._infDict.get('gongzi')
        
        Shebao=gongzi*(self._confIns.getConfig('YangLao'.lower())+self._confIns.getConfig('YiLiao'.lower())+self._confIns.getConfig('ShiYe'.lower())+self._confIns.getConfig('GongShang'.lower())+self._confIns.getConfig('ShengYu'.lower())+self._confIns.getConfig('GongJiJin'.lower()))
        return Shebao

    ##计算个人税
    def getShui(self):
        """
        应纳税所得额 = 工资金额 － 各项社会保险费 - 起征点(3500元)
        纳税 = 应纳税所得额 × 税率 － 速算扣除数

        :return:
        """
        shuim=0.00
        yingnaPre = self._infDict.get('gongzi') - self.getSheBao()
        if yingnaPre > 3500:
            yingna = yingnaPre-3500
            if yingna <= 1500:
                shuim = yingna * 0.03 - 0
            elif yingna > 1500 and yingna <= 4500:
                shuim = yingna * 0.1 - 105
            elif yingna > 4500 and yingna <= 9000:
                shuim = yingna * 0.2 - 555
            elif yingna > 9000 and yingna <= 35000:
                shuim = yingna * 0.25 - 1005
            elif yingna > 35000 and yingna <= 55000:
                shuim = yingna * 0.3 - 2755
            elif yingna > 55000 and yingna <= 80000:
                shuim = yingna * 0.35 - 5505
            else:
                shuim = yingna * 0.45 - 13505
        return shuim

    ##计算税后工资
    def getAfterGongzi(self):
        """
        税后工资=工资-社保-个税
        :return:
        """
        AfterGongzi=self._infDict.get('gongzi')-self.getSheBao()-self.getShui()
        return AfterGongzi

    def getResult(self):
        return "{gonghao},{gongzi},{shebao},{shui},{gongziafter},{caTime}\n".format(gonghao=self._infDict.get("number"),gongzi=self._infDict.get("gongzi"),shebao=format(float(self.getSheBao()),'.2f'),shui=format(float(self.getShui()),'.2f'),gongziafter=format(float(self.getAfterGongzi()),'.2f'),caTime=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    ##每次打开文件，是否会增加io
    def writeInf(self,dst):
        """
        工号,税前工资,社保金额,个税金额,税后工资
        :param dst:
        :return:
        """
        with open(dst,'a') as file:
            file.write("{gonghao},{gongzi},{shebao},{shui},{gongziafter}\n".format(gonghao=self._infDict.get("number"),gongzi=self._infDict.get("gongzi"),shebao=format(float(self.getSheBao()),'.2f'),shui=format(float(self.getShui()),'.2f'),gongziafter=format(float(self.getAfterGongzi()),'.2f'),))



class Conf(object):
    def __init__(self,confDict):
        """
        JiShuL = 2193.00
        JiShuH = 16446.00
        YangLao = 0.08
        YiLiao = 0.02
        ShiYe = 0.005
        GongShang = 0
        ShengYu = 0
        GongJiJin = 0.06

        :param confDict:
        """
        self._config=confDict

    def getConfig(self,value):

        return self._config.get(value)

def readConfFile(filename):
    with open(filename) as file:
        return file.read()

def readUserFile(filename):
    with open(filename) as file:
        for line in file:
            yield line
def caculateTax(queue,confIns,queueWriteFile):
    while True:
        try:
            data=queue.get(timeout=2)

            userIns=UserInfor(data,confIns)
            result=userIns.getResult()
            # print(result)
            queueWriteFile.put(result)
        except Exception as err:
            # print("进程2")
            print(err)
            break


def writeFile(queue,dst):
    # file=open(dst,'w')
    with open(dst,'w') as file:
        while True:
            try:
                data=queue.get(timeout=5)
                # print("进程3：",data)
                file.write(data)

            except Exception as err:
                print(err)
                break





def getUserInf(srcDir,queueUser):
    """
      101,3500
      203,5000
      309,15000
      1.获取一个信息
      2.处理
      3.写入一个人的信息
      """
    userInGenerator=readUserFile(srcDir)
    # print(type(userInGenerator))
    # print(dir(userInGenerator))
    userConf=userInGenerator.__next__().strip('\n')
    while userConf:
        # print(userConf)
        number,gongzi=userConf.split(',')
        queueUser.put({"number":number.strip(' '),"gongzi":int(gongzi.strip(' '))})
        # userIns=UserInfor({"number":number.strip(' '),"gongzi":int(gongzi.strip(' '))},confIns)
        # userIns.writeInf(dst)
        try:
            userConf = userInGenerator.__next__().strip('\n')
        except StopIteration:
            # print('StopIteration')
            break



def getarg():
    global confDict
    options,argv=getopt(sys.argv[1:],"hC:c:d:o:",["help"])
    optDict=dict(options)
    if '-h' in optDict.keys() or '--help' in optDict.keys():
        print("Usage: calculator.py -C cityname -c configfile -d userdata -o resultdata")
        exit(0)
    if '-C' in optDict.keys():
        cityname=optDict.get('-C').upper()
    else:
        cityname="DEFAULT"

    confDir=optDict.get('-c')
    srcDir=optDict.get('-d')
    dstDir=optDict.get('-o')
    # argvs=sys.argv[1:]
    # confDir=argvs[argvs.index('-c')+1]
    # srcDir = argvs[argvs.index('-d') + 1]
    # dstDir = argvs[argvs.index('-o') + 1]
    # print(confDir,srcDir,dstDir)
    # confDir="test.cfg"
    # srcDir="user.csv"
    # dstDir="userAfter.csv"

    ##判断前2个文件路径是否存在
    if not os.path.exists(confDir):
        print("conf file not exist")
        exit(1)
    if not os.path.exists(srcDir):
        print("user file not exist")
        exit(1)


    ##读配置
    """
    JiShuL = 2193.00
    JiShuH = 16446.00
    """
    conf=ConfigParser()
    conf.read(confDir)
    # print(conf.options(cityname))
    for option in conf.options(cityname):
        # print(option)
        confDict[option]=float(conf.get(cityname,option))
    # print(confDict)


    # fileResult=readConfFile(confDir)
    # for line in fileResult.split('\n'):
    #     if not line:
    #         continue
    #     confKey,confVal=line.split('=')
    #     confDict[confKey.strip(' ')]=float(confVal.strip(' '))

    confIns=Conf(confDict)

    queueUser=Queue(maxsize=50)
    queueWriteFile=Queue(maxsize=50)

    getUserInfPro = Process(target=getUserInf, args=(srcDir,queueUser,))
    calculateTaxPro=Process(target=caculateTax, args=(queueUser,confIns,queueWriteFile,))
    writeFilePro = Process(target=writeFile, args=(queueWriteFile,dstDir,))

    getUserInfPro.start()
    calculateTaxPro.start()
    writeFilePro.start()
    getUserInfPro.join()
    calculateTaxPro.join()
    writeFilePro.join()


    # ##读取员工信息
    # getUserInf(srcDir,confIns,dstDir)


if __name__=="__main__":
    getarg()