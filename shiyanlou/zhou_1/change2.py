#coding=utf8
#/usr/bin/env python3
import sys

yginf={}
def getTrueGongzi(gongzi):
    wuxianm=(0.08+0.02+0.005+0.06)*gongzi
    yingna=gongzi-wuxianm-3500
    if yingna<=1500:
        shuim=yingna*0.03-0
    elif yingna>1500 and yingna<=4500:
        shuim =yingna*0.1-105

    elif yingna>4500 and yingna<=9000:
        shuim =yingna*0.2-555
    elif yingna>9000 and yingna<=35000:
        shuim =yingna*0.25-1005
    elif yingna>35000 and yingna<=55000:
        shuim =yingna*0.3-2755
    elif yingna>55000 and yingna<=80000:
        shuim =yingna*0.35-5505
    else:
        shuim = yingna * 0.45 - 13505
    result=gongzi-wuxianm-shuim
    return result

def printResult():
    for key,val in yginf.items():
        print("{key:val}".format(key=key,val=format(val,".2f")))

def getGongzi(gonghao,gongzi):
    result=getTrueGongzi(gongzi)
    # global yginf
    yginf[gonghao]=result


def getarg():
    if len(sys.argv)<=1:
        print("请输入薪资")
        exit(0)

    for arg in sys.argv[1:]:
        gonghao,gongzi=arg.split(":")
        try:
            gonghao=int(gonghao)
            gongzi=int(gongzi)
        except Exception as e:
            print("Parameter Error")
            exit(1)

        getGongzi(gonghao,gongzi)

if __name__=="__main__":
    getarg()