# coding=utf-8
import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid.anchored_artists import AnchoredText

#samp cycle = 43ms(默认5位半精度)
#开机时间 = 43ms*720=30.96s左（人眼延迟）
'''

'''
class PowerCalculate(object):
    """convert datas which comes from a txt file into power value.

    Attributes:
        path: absolute path of a txt file.
        volt: the supply voltage

    """
    def __init__(self, path=None, volt = None, timeInterval= None, delt = 0):
        """

        :param path: the file path restore the reading datas
        :param volt: if volt is none then we just need to show the current and set the volt to 0V(mute the power)
        :param timeInterval: to calculate the real test time
        """
        self.path = path
        self.y = []
        self.y_lens = 0
        self.time_mins = 0
        self.delt = delt
        if volt:
            self.volt = volt
        else:
            self.volt = 0

        if timeInterval:
            self.timeInterval = timeInterval
        else:
            self.timeInterval = 0.00001



    def deal_data(self):
        '''
        the datas in file should be the pattern like this:
            for one line :
                "12,345345,123,123123,43,43,5,3,5,543,453,45,3535"
        the we can easily get the singal data and get che total count of datas
        :risk:
        if the datas too much,the mem maybe overflow.

        #相对矫正因子：
            relative correction factor ===> RCF
            用来矫正输出的，当是显示电流或者普通电压的时候是直接输出的，但是当显示采样电阻上的电压时需要乘以一个矫正因子。
        :return:
         self.y_lens
            total datas number
         self.time_mins:
            test time

        '''
        datas = 0
        with open(self.path, "r") as f:
            s = f.readline().split(",")
            for d in s:
                d_A = float(d)*(100)
                datas += d_A
        len_A = len(s)
        average_data = datas/len_A
        if average_data > 0:
            direction = 1
        else:
            direction = -1


        with open(self.path,"r") as f:
            for line in f.readlines():
                string_list = line.split(",")
                lens = len(string_list)
                for data in string_list:
                    data_A = float(data)*(100)*direction - self.delt
                    # if data_A > 0.16:
                    #    lens -=1
                    #    continue
                    self.y.append(data_A)#to A:(U/(10*10-3))=U*100 A
                self.y_lens += lens
        #print str(len(self.y)) + "data",(self.y_lens*0.043)/60,"mins"

        current_all = 0
        for current in self.y:
            current_all += current
        #print "average current={}".format(current_all/self.y_lens)
        s1 = "[average current={}".format(current_all/self.y_lens) + "A"+"]   "

        x =  range(0,self.y_lens,1)
        power = 0

        for current in self.y:
            power += self.volt*current*0.043#瞬时功耗 43ms

        average_power = power/(self.y_lens*0.043)
        #print "average power={}".format(average_power)
        s2 = "[average power={}".format(average_power) + "W"+"]"

        fig,ax = plt.subplots()

        plt.xlabel("samping datas COUNT")
        plt.ylabel("Current(A)")
        plt.title("||Scene||: "+os.path.basename(self.path).split(".")[0])
        plt.grid(True)

        at = AnchoredText(s1+s2,prop=dict(size=10),frameon=True,loc=2,)
        at.patch.set_boxstyle("round,pad=0.,rounding_size=0.5")
        ax.add_artist(at)

        at = AnchoredText("samping rate = {}".format(int(1/self.timeInterval))+"Hz", prop=dict(size=10), frameon=True, loc=4, )
        at.patch.set_boxstyle("round,pad=0.,rounding_size=0.5")
        ax.add_artist(at)

        plt.plot(x,self.y,".-")
        # Delta_curr = []
        # for i in range(self.y_lens):
        #     if i == 0 :
        #         Delta_curr.append(self.y[0])
        #     else:
        #         total_temp = 0
        #         for j in range(1+i):
        #             total_temp += self.y[j]
        #         average_temp = total_temp /(1+i)
        #         Delta_curr.append(average_temp)
        #
        # print len(self.y),len(Delta_curr)
        # plt.plot(range(len(Delta_curr)),Delta_curr,".-")
        plt.show()


if __name__ == "__main__":
    path = os.path.join(os.getcwd(), "A63-yabo-darkscreenMusic.txt")
    PowerCalculate(path=path,volt=4.1,timeInterval=0.002).deal_data()