#!/usr/bin/python
#-*-coding:utf-8 -*-
#adb logcat -v time -d > log.txt
import visa
import sys
import time
import re
import os
from multiprocessing import Queue
import showcurrent
import device_IT6861A
class  Device_34972A(object):
    """
    CONFigure:
        1. the CONFigure command dose not place the instrument in the "wait for trigger" state.
        use the INITiate or READ? command in conjunction with CONFigure to place the instrument
        in the "wait for trigger" state.
        2. Because this command resets all measurement parameters on the specified to their default values,
        be sure to send the CONFigure command before setting any other measurement parameters.

    """
    # Change this variable to the address of your instrument
    VISA_ADDRESS = "USB0::0x0957::0x2007::MY57001614::INSTR"#""USB0::2391::8199::MY57001614::1::INSTR"
    SerchString = 'USB?*INSTR'

    def __init__(self,TestType = "Voltage",Samp_Rate = 500,):

        self.CurrentDatas = []
        self.VoltageDatas = []
        self.session = None
        self.status = None
        self.delt = 0  #10mR电阻的误差补偿
        self.OpenDevice()

    def OpenDevice(self):
        """
        open device with current setting. this may throw a PowerException
        if the device cannot be opened.
        :return: None
        """
        print("start open Device_34972A:")
        try:
            self.resourceManager = visa.ResourceManager()
            #print("the location of the shared library:",self.resourceManager)
            self.InitDevice()
            # Create a connection (session) to the instrument
            self.session = self.resourceManager.open_resource(self.VISA_ADDRESS,open_timeout=10000)
            self.session.write("*RST")
            self.session.write("*CLS")
            self.session.write("DISP ON")
        except visa.Error as ex:
            print('·Could not connect to {}, exiting now...'.format(self.VISA_ADDRESS))
            print("end _init_ in Device_34972A with error.")
            sys.exit()
        print("open Device_34972A ok.")

    def InitDevice(self):
        print("start InitDevice:")
        print('.Find with search string \'%s\':' % self.SerchString)
        devices = self.resourceManager.list_resources(self.SerchString)
        if len(devices) == 1:
            if self.VISA_ADDRESS in devices:
                pass
            else:
                try:
                    self.VISA_ADDRESS = devices[0]
                except:
                    self.VISA_ADDRESS = devices
            print "·· Found device:",devices[0]
        elif len(devices) > 1:
            if Device_34972A.VISA_ADDRESS in devices:
                self.VISA_ADDRESS = Device_34972A.VISA_ADDRESS
            else:
                print('no right device found!')
                self.resourceManager.close()
        else:
            print('.. didn\'t find anything!')
        print("end InitDevice.")

    def __del__(self):

        self.session.write("ABOR")
        self.session.close()
        self.resourceManager.close()

        print "__del__ was excuted."

    def PowerRead(self,CurChannel = "None",VolChannel = "None"):

        pass
    def CurRead(self,filepath = None,Channel="122",CurrType="DC",CurrRange = "AUTO",Resolution="DEF",\
                reading_time = "300"):
        """
        three level: 10mA,100mA,1A

        :param filepath:
        :param Channel:
        :param CurrType:
        :param CurrRange:
        :param Resolution:
        :param reading_time:
        :return:
        """
        try:
            # if the type of param "chanel" wrong,maybe raise a error and be catched by exception.
            channel_int = int(Channel) - 100
            #assert str(channel_int) is ("21" or "22"),"chanel number error."
            global q
            self.path = filepath

            command_string = "CONF:VOLT:" + CurrType + " " + CurrRange + "," + Resolution + "," + "(@{})".format(Channel)
            self.session.write(command_string)

            ReadNumbers = self.resolution_2_readnumbers(Resolution, int(reading_time))

            print ReadNumbers

            self.session.write("TRIG:COUN {}".format(ReadNumbers))
            self.session.write("INIT")
            time.sleep(0.5)

            if ReadNumbers == 0:
                data = self.unicode_2_string(self.session.query("R? 1"))
                return float(data)

            print("Start to read datas.")
            total_read = 0
            while total_read < int(ReadNumbers):
                try:
                    if int(self.session.query("DATA:POINts?")) >= 100:
                        # strip the head or index of a reading !
                        # reading: "#228-4.30000000E-08,00000000.370"
                        datas = self.session.query("R? 100")
                        # like this: "#-4.30000000E-08,00000000.370"
                        datas_string = self.unicode_2_stringList(datas)
                        with open(self.path, "a+") as f:
                            f.writelines(datas_string)
                            f.flush()
                            total_read += 100
                            print "channel{}".format(Channel), "reading 100 datas."
                    else:
                        time.sleep(0.4)
                except Exception as e:
                    quit()
                    print("##############quit ok!###############", e)
        except Exception as e:
            print("open chanel failed.",e)

        pass

    def VolRead(self,filepath = None,Channel="120",VolType="DC",VolRange = "AUTO",Resolution="DEF",\
                InputResisitance = None,reading_time = "300",current_resistor = "0.01"
                 ):
        """get datas base on the setting(default range is AUTO,default resolution is 6.5).

        :param
            Channal: the chanel you are going to ReadVoltage.
            InputResisitance: default is "10M"
            reading_time ： secends
            VolRange: 100mV,1V,10V,100V,300V.

        :rtype: float or FILE*


        self.session.write("VOLT:DC:RES 0.00005,(@118)")
            the command sets the <resolution> to 50 microvolts for the channels shown.
        #self.session.write("VOLT:DC:NPLC 200,(@118)")
        #self.session.write("CALC:SCAL:GAIN 1000,(@118)")
        #self.session.write("CALC:SCAL:OFFS 5,(@118)")
        # self.session.write("R?80")
        #self.session.write("FORM:READ:TIME:TYPE ABS")  # 没有这句默认就是相对时间，#228-4.30000000E-08,00000000.370
        #self.session.write("FORM:READ:TIME ON")#不开的话就是这样，没时间的。#215-2.15000000E-08
        # no unit:   #239-1.29000000E-07,2017,07,02,11,15,48.778
        """
        global q
        self.path = filepath

        command_string = "CONF:VOLT:" + VolType + " " + VolRange + "," + Resolution +","+ "(@{})".format(Channel)
        self.session.write(command_string)

        ReadNumbers = self.resolution_2_readnumbers(Resolution,int(reading_time))

        self.session.write("TRIG:COUN {}".format(ReadNumbers))
        self.session.write("INIT")
        time.sleep(0.5)

        if ReadNumbers == 0:
            data = self.unicode_2_string(self.session.query("R? 1"))
            return float(data)

        total_read = 0
        while total_read < int(ReadNumbers):
            try:
                if int(self.session.query("DATA:POINts?")) >= 100:
                    #strip the head or index of a reading !
                    #reading: "#228-4.30000000E-08,00000000.370"
                    datas =  self.session.query("R? 100")
                    #like this: "#-4.30000000E-08,00000000.370"
                    datas_string= self.unicode_2_stringList(datas)
                    with open(self.path,"a+") as f:
                        f.writelines(datas_string)
                        f.flush()
                        total_read +=100
                        print "channel{}".format(Channel), "reading 100 datas."
                else:
                    time.sleep(0.4)
            except Exception as e:
                quit()
                print("##############quit ok!###############",e)
    def resolution_2_readnumbers(self,Resolution,reading_time):
        """
        #与电压范围没有关系
        #resolution:
        #   MIN:7951ms
        #   DEF:43ms
        #   MAX:2ms
        #   <0.001 x Range:--------------> 2ms
        #   <0.0001 x Range1:------------> 2ms
        #   <0.00001 x Range3:-----------> 43ms
        #   <0.0000022 x Range:----------> 78ms
        #   <0.000001 x Range:-----------> 398ms
        #   <0.0000008 x Range:----------> 798ms
        #   <0.0000003 x Range:----------> 3951ms
        #   <0.00000022 x Range:---------> 7951ms
        :param Resolution: str
        :param reading_time: int seconds
        :return: int type,the number of datas;if the param:"Resolution" is error,the use the default resolution.
        """
        return {
            "DEF":        lambda reading_time: int(reading_time / 0.043),
            "MIN":        lambda reading_time: int(reading_time / 7951),
            "MAX":        lambda reading_time: int(reading_time / 0.002),
            "0.001":      lambda reading_time: int(reading_time / 0.002),
            "0.0001":     lambda reading_time: int(reading_time / 0.002),
            "0.00001":    lambda reading_time: int(reading_time / 0.043),
            "0.0000022":  lambda reading_time: int(reading_time / 0.078),
            "0.000001":   lambda reading_time: int(reading_time / 0.398),
            "0.0000008":  lambda reading_time: int(reading_time / 0.798),
            "0.0000003":  lambda reading_time: int(reading_time / 3951),
            "0.00000022": lambda reading_time: int(reading_time / 7951)
        }[Resolution](reading_time)

    def unicode_2_stringList(self,datas):

        #input a format unicode,return float_list and the length of the list
        #datas = "#247-2.15000000E-08,-1.71900000E-07,+0.00000000E+00"
        float_datas = []
        if datas.startswith("#"):
            if datas.startswith("#10"):
                print "get no datas"
                return float_datas, len(float_datas)
            assert (int(datas[1:2]) + 2 + int(datas[2: 2 + int(datas[1:2])])) == len(datas) - 1, "datas missing."
            return datas[(int(datas[1:2]) + 2):]
        else:
            print("Error datas.")
            return ''

    def Configue_session(self,conf=None,route = None,trig=None):

        self.session.write("CONF:VOLT:DC 10,MAX,(@118)")
        self.session.write("ROUT:SCAN (@118)")
        #self.session.write("FORM:FETC:TIME:TYPE ABS")
        #self.session.write("FORM:FETC:TIME ON")

        self.session.write("TRIG:COUN 3")
        self.session.write("INIT")

    '''
    this is a class discription docs.
    once you complete a case ,then clear the vironment automatlly.

    Parameters:
        type  - DC:only support DC now.
        count - this is the number of values you are going to read.
        channel - the channel number you are goning to deal.
                - (1,2,3)2(1,2),for example: 122 means slot 1 , 22 channel.
        range - 10mA: 6欧姆
              - 100mA：6欧姆
              - 1A：0.6欧姆
        resolution  - MIN：selects the smallest value accepted,which gives the highest resolution.
                    - MAX: selects the largest value accepted ,which gives the least resolution.
                    -
        scan_list   - "122"
                    - "122,221,322"
    '''
    def CurrentTest(self,type = "DC",count = None,channel = None,range = None,resolution = None):

        CONF_string = "CONF:CURR:"

        if type != "DC":
            print(type, "is not support now.")
        CONF_string += "DC "

        if range:
            CONF_string += range + ","
        else:
            #for default
            CONF_string += "1,"

        if resolution:
            CONF_string += resolution + ","
        else:
            CONF_string +="MAX,"

        assert channel , "you didnt input the channel number in class CurrentTest."

        CONF_string += "(@" + channel + ")"

        # 10,100代表mA，1代表A，MAX表示最高精度，简书上的截图可查询如何设置精度
        self.session.write(CONF_string)


        #扫描列表
        self.session.write("ROUT:SCAN (@{})".format(channel))
        # self.session.write("FORM:FETC:TIME:TYPE ABS")
        # self.session.write("FORM:FETC:TIME ON")
        CNT_string = None
        if count:
            if int(count) < 0:
                CNT_string = "INF"
            else:
                CNT_string = count
        #default
        else:
            CNT_string = "1"
        self.session.write("TRIG:COUN {}".format(CNT_string))

        self.session.write("INIT")

        time.sleep(1)


        #after congfiguration there only 3 states
        #start to read datas
        if CNT_string == "1":
            unicode_datas = self.session.query("R? ")
            float_datas,lens= self.unicode_2_float(unicode_datas)
            if lens != len(float_datas):
                print "data missing No.2."
            self.CurrentDatas = float_datas
            print self.CurrentDatas
        elif CNT_string == "INF":
            pass
        else:
            pass

    def unicode_2_float(self,datas):

        #input a format unicode,return float_list and the length of the list
        #datas = "#247-2.15000000E-08,-1.71900000E-07,+0.00000000E+00"
        float_datas = []
        if datas.startswith("#"):
            if datas.startswith("#10"):
                print "get no datas"
                return float_datas, len(float_datas)
            #print datas,(int(datas[1:2]) + 2 + int(datas[2: 2 + int(datas[1:2])])),len(datas)
            assert (int(datas[1:2]) + 2 + int(datas[2: 2 + int(datas[1:2])])) == len(datas) - 1, "datas missing."
            datas_list = datas[(int(datas[1:2]) + 2):].split(",")

            for index in range(len(datas_list)):
                float_datas.append(float(datas_list[index]))
            return float_datas, len(float_datas)
        else:
            print("Error datas.")
            return float_datas, len(float_datas)

    def power_case(self,VOLT_channel = None,CURR_channel = None,):
        pass

    def test_demo(self):
        #READ?是自带初始化的，其他的读取方式是需要手动初始化的INIT，同时切记不要初始化后马上就去取数据，这很有可能是取不到的。
        #       #print(self.session.write("R?"))
        # print self.session.read()
        self.Configue_session()

        time.sleep(1)#要等待初始化完成
        # FETC?指令会等待你的采集完了方会去获取数据，因此当我们采用无限循环采集数据的时候就会会问题啊！因为会一直等直到超时溢出啊！
        #print(self.session.query("R?"))
        #print (type(self.session.query("FETC?")))#unicode
        #unicode to str
        #data_unicode = self.session.query("R? 2")
        self.session.write("R? 2")
        print self.session.read().encode("utf-8")
        #print self.session.write("TRIG:COUN?")
        #print(data_unicode, type(data_unicode), len(data_unicode))
        #data_str = str(data_unicode)
        #print(data_str.strip("\n"),type(data_str),len(data_str))
        #print(self.session.query("R?"))
        #R?指令允许你在任何时间从易失性内存中读取数据，读一个少一个，这就允许你可以

    def test_demo2(self):
        #配置好之后，假如不配置TRIG的话，就算你R？ 4读取到的数据也只有1个。
        #注意在INIT之后一定要延时一段时间让机器去采数据。

        self.session.write("CONG:FREQ 100,(@118)")
        self.session.write("ROUT:SCAN (@118)")
        #self.session.write("TRIG:COUN 3")没有TRIG就是读取一次
        self.session.write("INIT")
        time.sleep(1)
        self.session.write("R?")#(4L, <StatusCode.success: 0>)表示成功发送2（默认）+N个字符,在没有指明trig的情况下，你R？3也是拿不到三个数据的，只有一个。
        print self.session.read()#.decode("utf-8")#"#10"表示没有数据啊，0个数据
        #”#215-1.09419200E-03“ 这种读取方式是会带上#215头的

    def test_demo3A(self):
        #配置好之后，假如不配置TRIG的话，就算你R？ 4读取到的数据也只有1个。
        #注意在INIT之后一定要延时一段时间让机器去采数据。
        self.session.write("*CLS")
        self.session.write("CONG:FREQ 10000,(@118)")
        self.session.write("ROUT:SCAN (@118)")
        #self.session.write("TRIG:COUN 3")没有TRIG就是读取一次
        #self.session.write("READ?")#(4L, <StatusCode.success: 0>)表示成功发送2（默认）+N个字符,在没有指明trig的情况下，你R？3也是拿不到三个数据的，只有一个。
        time.sleep(1)
        #print type(self.session.read())#.decode("utf-8")#"#10"表示没有数据啊，0个数据
        #-1.60342400E-03，unicode,但是不会有前缀#231跟后缀换行符了。

        print self.session.write("READ?")
        time.sleep(0.1)#这里延时0.1s是不够的
        print type(self.session.read_raw())#-3.07300000E-05, type:str

        quit()

    # 测试采样周期的边界
    def test_demo3B(self):
        self.session.write("*CLS")
        #与电压范围没有关系
        #resolution:
        #   MIN:7951ms
        #   DEF:43ms
        #   MAX:2ms
        #   <0.001 x Range:--------------> 2ms
        #   <0.0001 x Range1:------------> 2ms
        #   <0.00001 x Range3:-----------> 43ms
        #   <0.0000022 x Range:----------> 78ms
        #   <0.000001 x Range:-----------> 398ms
        #   <0.0000008 x Range:----------> 798ms
        #   <0.0000003 x Range:----------> 3951ms
        #   <0.00000022 x Range:---------> 7951ms
        self.session.write("CONF:VOLT:DC 1,DEF,(@120)")
        #self.session.write("FORM:READ:TIME:TYPE ABS")#没有这句默认就是相对时间，#228-4.30000000E-08,00000000.370
        self.session.write("FORM:READ:TIME ON")#不开的话就是这样，没时间的。#215-2.15000000E-08
        # no unit:   #239-1.29000000E-07,2017,07,02,11,15,48.778
        # with unit on:#243-1.07500000E-07 ADC,2017,07,02,11,16,44.859
        # self.session.write("FORM:READ:UNIT ON")
        # self.session.write("R?80")
        self.session.write("TRIG:COUN 3")
        self.session.write("ROUT:SCAN (@120)")
        self.session.write("INIT")
        #self.session.write("VOLT:DC:NPLC 200,(@120)")
        #self.session.write("CALC:SCAL:GAIN 1000,(@118)")
        # self.session.write("CALC:SCAL:OFFS 5,(@118)")

        while int(self.session.query("DATA:POINts?")) < 3:
            time.sleep(1)
            print int(self.session.query("DATA:POINts?"))
        datas = self.session.query("R? 10")
        # like this: "#-4.30000000E-08,00000000.370"
        datas_string = self.unicode_2_stringList(datas)
        with open("test.txt", "w") as f:
            f.writelines(datas_string)
            f.flush()
            print "channel{}".format("120"), "reading 100 datas."

    def Current_read(self):
        #channel:19;DC10V;4.5分辨率
        self.session.write("*CLS")
        self.session.write("CONF:CURR:DC 10,MAX,(@122)")#这里的10是有问题的啊！？

        #self.session.write("CONF:VOLT:DC 10,MAX,(@120)")
        #self.session.write("FORM:READ:TIME:TYPE ABS")#没有这句默认就是相对时间，#228-4.30000000E-08,00000000.370
        #self.session.write("FORM:READ:TIME ON")#不开的话就是这样，没时间的。#215-2.15000000E-08
        # no unit:   #239-1.29000000E-07,2017,07,02,11,15,48.778
        #with unit on:#243-1.07500000E-07 ADC,2017,07,02,11,16,44.859
        #self.session.write("FORM:READ:UNIT ON")


        #self.session.write("R?80")
        self.session.write("TRIG:COUN INF")
        self.session.write("ROUT:SCAN (@122)")
        self.session.write("INIT")
        i=0
        while i<10:
            #self.session.write("R? 5")
            #print self.session.read()
            #self.session.write("ROUT:SCAN (@122)")
            time.sleep(1)
            print self.unicode_2_float(self.session.query("R? 1"))
            #print self.CurrentDatas

            time.sleep(1.5)
            print self.session.query("DATA:POINts?")
            time.sleep(1.5)

            #self.session.write("ROUT:SCAN (@120)")
            #self.session.write("TRIG:COUN 3")
            #self.session.write("INIT")
            #time.sleep(1)
            #self.session.query("R? 3")
            #time.sleep(2)
            i +=1

    def reset(self):
        print "start restart...."
        self.session.write("RST")

    def abort(self):
        print "start abort...."
        self.session.write("ABOR")

    def quit(self):
        self.session.write("ABOR")
        self.session.close()
        self.resourceManager.close()

    def CompareDemo(self,q):
        self.session.write("CONF:VOLT:DC 1,MAX,(@120)")
        # self.session.write("FORM:READ:TIME:TYPE ABS")#没有这句默认就是相对时间，#228-4.30000000E-08,00000000.370
        #self.session.write("FORM:READ:TIME ON")  # 不开的话就是这样，没时间的。#215-2.15000000E-08

        self.session.write("TRIG:COUN INF")
        self.session.write("ROUT:SCAN (@120)")
        self.session.write("INIT")
        time.sleep(1)
        i=0
        while i<10000:#int(self.session.query("DATA:POINts?")) < 3:
            time.sleep(0.01)
            #print int(self.session.query("DATA:POINts?"))
            data_uni = self.session.query("R? 1")
            data_string = self.unicode_2_string(data_uni)
            #print(data_string)
            data = float(data_string)*(-100)
            if q.full() is True:
                print(data)
            else:
                q.put(data)
                # print(float(self.session.query("FETCh:CURRent:DC?")))
            i += 1

    def unicode_2_string(self, data):
        # input a format unicode,return float_list and the length of the list
        # datas = "#247-2.15000000E-08"
        float_datas = []
        if data.startswith("#"):
            if data.startswith("#10"):
                print "get no datas"
                return float_datas, len(float_datas)
            # print datas,(int(datas[1:2]) + 2 + int(datas[2: 2 + int(datas[1:2])])),len(datas)
            assert (int(data[1:2]) + 2 + int(data[2: 2 + int(data[1:2])])) == len(data) - 1, "datas missing."
            return data[(int(data[1:2]) + 2):]
        else:
            print("Error datas.")
            return ''

    def quicktest_volt(self,path):
        """
        101: volt
        120: charger current ====> Rs ====> Vrs
        122: charger current


        :param readingtime:
        :param Channel:
        :return:
        """

        #1、误差补偿
        #preProcced
        PD6861 = device_IT6861A.Device_IT6861A()
        currents_PD6861 , lens = PD6861.PreReadCurrents()
        total = 0
        for data in currents_PD6861:
            total += data
        average_current_PD6861 = total / lens
        print "average_current_PD6861=",average_current_PD6861

        #34972A precced
        self.session.write("CONF:VOLT:DC 0.1,MAX,(@120)")  # 43ms@ 0.1 DEF
        self.session.write("ROUT:SCAN (@120)")
        self.session.write("TRIG:COUN {}".format(lens+20))
        self.session.write("INIT")
        time.sleep(3)


        current_34972 = []
        while len(current_34972) < 100:
            if int(self.session.query("DATA:POINts?")) >= 10:
                data_uni = self.session.query("R? 1")
                data_string = self.unicode_2_string(data_uni)
                data = float(data_string) * (100)
                if data < 0:
                    data *= -1
                current_34972.append(data)
            else:
                time.sleep(1)

        total1 = 0
        for data1 in current_34972:
            total1 += data1
        average_current_34972 = total1 / len(current_34972)
        print "average_current_34972=",average_current_34972

        if average_current_34972 < 0:
            self.delt_flag = -1
        else:
            self.delt_flag = 1

        self.delt = average_current_34972*self.delt_flag - average_current_PD6861
        print "delt={} A".format(self.delt)



        #2、电压补偿
        i = 0
        volt = 0
        self.session.write("CONF:VOLT:DC AUTO,DEF,(@101)")
        #10v,MAX = 531ms   ?????????????哈哈哈，这里我是每次读一个啊，不连续的啊，肯定时间差不多且很长~用无限读取的方式可解决。
        #10V,DEF = 528ms
        #self.session.write("FORM:READ:TIME:TYPE ABS")
        #self.session.write("FORM:READ:TIME ON")
        self.session.write("ROUT:SCAN (@101)")
        self.session.write("TRIG:COUN 1")
        self.session.write("INIT")
        time.sleep(3)
        while i < 10:  # int(self.session.query("DATA:POINts?")) < 3:

            if int(self.session.query("DATA:POINts?")) >=1:
                data_uni = self.session.query("R? 1")
                data_string = self.unicode_2_string(data_uni)
                data = float(data_string) #* (-100)
                volt += data
                volt /= 2
                print("volt data:{} into list.".format(data))
                i += 1

                self.session.write("TRIG:COUN 1")
                self.session.write("INIT")

            else:
                time.sleep(0.5)



        #3、正式开始测试电流值
        self.session.write("*RST")

        # raise "stop handlly !!!"

        self.session.write("CONF:VOLT:DC 0.1,MAX,(@120)")#43ms@ 0.1 DEF
        #self.session.write("FORM:READ:TIME:TYPE ABS")
        #self.session.write("FORM:READ:TIME ON")
        self.session.write("ROUT:SCAN (@120)")
        self.session.write("TRIG:COUN INF")
        self.session.write("INIT")
        time.sleep(1)
        total_read = 0
        total_time = 0
        ReadNumbers = 300/0.002#300s reading datas
        with open(path, "w+") as f:

            while total_read < int(ReadNumbers) and total_time < 10:
                try:
                    #print("start to read current.......")
                    if int(self.session.query("DATA:POINts?")) >= 50:
                        # 连续进入无数据状态20次也就是10s内再也没数据了就认为采集结束了
                        total_time = 0
                        # strip the head or index of a reading !
                        # reading: "#228-4.30000000E-08,00000000.370"
                        datas = self.session.query("R? 50")
                        # like this: "#-4.30000000E-08,00000000.370"
                        datas_string = self.unicode_2_stringList(datas)

                    # with open(path, "a+") as f:
                        f.writelines(datas_string)
                        f.flush()
                        total_read += 50
                        print "channel_{}".format(120), "reading 50 datas."

                    else:
                        # 连续进入无数据状态10次也就是3s内再也没数据了就认为采集结束了
                        time.sleep(0.5)
                        total_time += 1
                except Exception as e:
                    self.quit()
                    print("##############quit failed!###############", e)

        #stop infinite loop
        self.session.write("ABORT")
        self.session.write("*RST")
        self.quit()



        from powercalculate import PowerCalculate
        PowerCalculate(path=path, volt=volt, timeInterval=0.002,delt = self.delt).deal_data()

    def quicktest_volts(self, path):
        """
        101: volt
        120: charger current ====> Rs ====> Vrs
        122: charger current


        :param readingtime:
        :param Channel:
        :return:
        """
        i = 0
        volt = 1
        self.session.write("CONF:VOLT:DC 10,MAX,(@120)")
        # 10v,MAX = 531ms   ?????????????哈哈哈，这里我是每次读一个啊，不连续的啊，肯定时间差不多且很长~用无限读取的方式可解决。
        # 10V,DEF = 528ms
        # self.session.write("FORM:READ:TIME:TYPE ABS")
        # self.session.write("FORM:READ:TIME ON")
        self.session.write("ROUT:SCAN (@120)")
        self.session.write("TRIG:COUN INF")
        self.session.write("INIT")
        time.sleep(3)
        total_read = 0
        total_time = 0
        ReadNumbers = 60 / 0.002  # 300s reading datas
        with open(path, "w+") as f:

            while total_read < int(ReadNumbers) and total_time < 10:
                try:
                    # print("start to read current.......")
                    if int(self.session.query("DATA:POINts?")) >= 50:
                        # 连续进入无数据状态20次也就是10s内再也没数据了就认为采集结束了
                        total_time = 0
                        # strip the head or index of a reading !
                        # reading: "#228-4.30000000E-08,00000000.370"
                        datas = self.session.query("R? 50")
                        # like this: "#-4.30000000E-08,00000000.370"
                        datas_string = self.unicode_2_stringList(datas)

                        # with open(path, "a+") as f:
                        f.writelines(datas_string)
                        f.flush()
                        total_read += 50
                        print "channel_{}".format(120), "reading 50 datas."

                    else:
                        # 连续进入无数据状态10次也就是3s内再也没数据了就认为采集结束了
                        time.sleep(0.5)
                        total_time += 1
                except Exception as e:
                    self.quit()
                    print("##############quit failed!###############", e)
        self.session.write("ABORT")
        print("start show...................")
        from powercalculate import PowerCalculate
        PowerCalculate(path=path, volt=volt, timeInterval=0.002).deal_data()



        self.session.write("*RST")

        self.session.write("CONF:CURR:DC 1,MAX,(@122)")  # 43ms@ 0.1 DEF
        # self.session.write("FORM:READ:TIME:TYPE ABS")
        # self.session.write("FORM:READ:TIME ON")
        self.session.write("ROUT:SCAN (@122)")
        self.session.write("TRIG:COUN INF")
        self.session.write("INIT")
        time.sleep(1)
        total_read = 0
        total_time = 0
        ReadNumbers = 300 / 0.002  # 300s reading datas
        with open(path, "w+") as f:

            while total_read < int(ReadNumbers) and total_time < 10:
                try:
                    # print("start to read current.......")
                    if int(self.session.query("DATA:POINts?")) >= 50:
                        # 连续进入无数据状态20次也就是10s内再也没数据了就认为采集结束了
                        total_time = 0
                        # strip the head or index of a reading !
                        # reading: "#228-4.30000000E-08,00000000.370"
                        datas = self.session.query("R? 50")
                        # like this: "#-4.30000000E-08,00000000.370"
                        datas_string = self.unicode_2_stringList(datas)

                        # with open(path, "a+") as f:
                        f.writelines(datas_string)
                        f.flush()
                        total_read += 50
                        print "channel_{}".format(120), "reading 50 datas."

                    else:
                        # 连续进入无数据状态10次也就是3s内再也没数据了就认为采集结束了
                        time.sleep(0.5)
                        total_time += 1
                except Exception as e:
                    self.quit()
                    print("##############quit failed!###############", e)

        # stop infinite loop
        self.session.write("ABORT")
        self.quit()

        #from powercalculate import PowerCalculate
        PowerCalculate(path=path, volt=volt, timeInterval=0.002).deal_data()

    def quicktest(self,path,readingtime,Channel):

        self.session.write("CONF:CURR:DC 1,DEF,(@{})".format(Channel))

        ReadNumbers = self.resolution_2_readnumbers("DEF", int(readingtime))

        print ReadNumbers

        self.session.write("TRIG:COUN {}".format(ReadNumbers))
        self.session.write("INIT")
        time.sleep(0.5)

        if ReadNumbers == 0:
            data = self.unicode_2_string(self.session.query("R? 1"))
            return float(data)

        print("Start to read datas.")
        total_read = 0
        total_time = 0
        with open(path, "w+") as f:
            while total_read < int(ReadNumbers) and total_time < 10:
                try:
                    if int(self.session.query("DATA:POINts?")) >= 50:
                        # 连续进入无数据状态20次也就是10s内再也没数据了就认为采集结束了
                        total_time = 0
                        # strip the head or index of a reading !
                        # reading: "#228-4.30000000E-08,00000000.370"
                        datas = self.session.query("R? 50")
                        # like this: "#-4.30000000E-08,00000000.370"
                        datas_string = self.unicode_2_stringList(datas)

                    # with open(path, "a+") as f:
                        f.writelines(datas_string)
                        f.flush()
                        total_read += 50
                        print "channel_{}".format(Channel), "reading 50 datas."

                    else:
                        # 连续进入无数据状态10次也就是3s内再也没数据了就认为采集结束了
                        time.sleep(0.5)
                        total_time += 1
                except Exception as e:
                    self.quit()
                    print("##############quit failed!###############", e)


        last_datas = int(self.session.query("DATA:POINts?"))
        datas = self.session.query("R? {}".format(last_datas))
        datas_string = self.unicode_2_stringList(datas)
        with open(path, "a+") as f:
            f.writelines(datas_string)
            f.flush()
            total_read += 100
            print "channel_{}".format(Channel), "Last reading {} datas.".format(last_datas)

        self.quit()
        print("##############quit ok!###############")



if __name__ == "__main__":

    path = os.path.join(os.getcwd(), "A63-yabo-YOUKUV1RC3.txt")
    power_device = Device_34972A()
    CURR_CHANNEL = 122
    READING_TIME = 10
    #power_device.quicktest(path=path,readingtime=300,Channel=122)
    power_device.quicktest_volt(path=path)
    #power_device.quit()
    #power_device.CurRead(filepath = path)
    '''
    power_device.quicktest(path,READING_TIME,CURR_CHANNEL)

    print "start to show datas"
    from powercalculate import PowerCalculate
    PowerCalculate(path=path,volt=3.8,timeInterval = 0.043).deal_data()
    '''
    #Device_34972A().test_demo3()

    '''
    from multiprocessing import Queue
    q = Queue(1024)
    import showcurrent
    import threading
    print("step 1")
    show = threading.Timer(1, showcurrent.ShowcurrentLine,[q])
    show.setDaemon(True)
    show.start()
    print("step 2")
    Device_34972A().VolRead(q)
    '''

