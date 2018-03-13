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
import threading
class  Device_IT6861A(object):
    """
    CONFigure:
    """
    # Change this variable to the address of your instrument
    VISA_ADDRESS = "USB0::0xFFFF::0x8500::600012010687620002::INSTR"
    SerchString = 'USB?*INSTR'
    DEVICE_NAME = "IT6861A"

    def __init__(self,TestType = "Voltage",Samp_Rate = 500,filepath = None):
        '''
        initiate the device and try to open the device, if not working raise error and quit.
            first use default address to open the device: Device_IT6861A.VISA_ADDRESS
            if not work try to get the address in service_thread.
                service_tread description: automatelly recognize and update devices.
        :param TestType:
        :param Samp_Rate:
        :param filepath:
        '''
        self.path = filepath
        self.CurrentDatas = []
        self.VoltageDatas = []
        self.session = None
        self.status = None
        self.VISA_ADDRESS = None
        self.name = Device_IT6861A.DEVICE_NAME
        self.OpenDevice()

    def __del__(self):

        self.session.write("ABOR")
        self.session.close()
        self.resourceManager.close()

        print "__del__ was excuted."

    def OpenDevice(self):
        """
        open device with current setting. this may throw a PowerException
        if the device cannot be opened.
        :return: None
        """
        print("start open Device_IT6861A:")
        try:
            self.resourceManager = visa.ResourceManager()
            #print("the location of the shared library:",self.resourceManager)
            self.InitDevice()
            # Create a connection (session) to the instrument
            self.session = self.resourceManager.open_resource(self.VISA_ADDRESS)
            #self.session.write("*RST")
            self.session.write("*CLS")
            #self.session.write("DISP ON")
        except visa.Error as ex:
            print('·Could not connect to {}, exiting now...'.format(self.VISA_ADDRESS))
            print("end _init_ in Device_34972A with error.")
            sys.exit()
        print("open Device_IT6861A ok.")

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
            if Device_IT6861A.VISA_ADDRESS in devices:
                self.VISA_ADDRESS = Device_IT6861A.VISA_ADDRESS
            else:
                self.FindInService()
                print('.. only surpport 1 device!')
                self.resourceManager.close()
        else:
            print('.. didn\'t find anything!')
        print("end InitDevice.")

    def SetVoltage(self,VoltageValue = "0"):
        print("set {} output Voltage = ".format(self.name),VoltageValue,"V")
        self.session.write("SOUR:VOLT:LEVel:IMMediate:AMPLitude {}".format(VoltageValue))
        time.sleep(1)
        assert float(self.session.query("VOLTage?")) == float(VoltageValue) ,\
        "set {} output Voltage = ".format(self.name) + str(VoltageValue) + "fail"
        print("set {} output Voltage = ".format(self.name), VoltageValue,"success")

    def SetCurrent(self,CurrentValue = "2.0"):

        print("set {} output CUURent = ".format(self.name),CurrentValue,"A")

        self.session.write("SOUR:CURR:LEVel:IMMediate:AMPLitude {}".format(CurrentValue))

        time.sleep(1)

        assert float(self.session.query("CURRent?")) == float(CurrentValue) ,\
        "set {} output Voltage = ".format(self.name) + str(CurrentValue) + " fail"

        print("set {} output Voltage = ".format(self.name), CurrentValue,"success")

    def OutputOnOff(self,state = "OFF"):

        print("preset output Value is:")
        print("...{}:output Voltage = ".format(self.name), float(self.session.query("VOLTage?")),"V")
        print("...{}:output Current = ".format(self.name), float(self.session.query("CURRent?")),"A")

        assert state is ("ON" or "OFF"),"the paramater in OutputOnOff(state) is error.(should be ON or OFF)"

        self.session.write("OUTPut:STATe {}".format(state))

    def ReadVoltage(self):
        """
        FETCh[:VOLTage]?
            该命令用来读取采样缓存里的最近预处理电压读数。发出该命令后并且让仪器对话，读数发送到电脑。
            该命令不影响仪器设定。该命令不触发测量操作，仅要求最近可得的读数。在有新读数前，
            该命令返回的都是~旧~读~数。
            ps. means no buffer.
        MEASure[:VOLTage]?
            该命令用来通过电源的检测端子来量测并返回当前电压输出值。
        :return: float Voltage value.
        """
        data = self.session.query("MEASure:VOLTage:DC?")
        if  data is None:
            # means error
            return 10000.0
        else:
            return float(data)

    def ReadCurrent(self):
        """
        FETCh[:VOLTage]?
            该命令用来读取采样缓存里的最近预处理电流读数。发出该命令后并且让仪器对话，读数发送到电脑。
            该命令不影响仪器设定。该命令不触发测量操作，仅要求最近可得的读数。在有新读数前，
            该命令返回的都是~旧~读~数。
            ps. means no buffer.
        MEASure[:VOLTage]?
            该命令用来通过电源的检测端子来量测并返回当前电流输出值。
        :return: float Current value.
        """
        data = self.session.query("MEASure:CURRent:DC?")
        if  data is None:
            # means error
            return 10000.0
        else:
            return float(data)

    def ReadPower(self):
        """
        FETCh[:VOLTage]?
            该命令用来读取采样缓存里的最近预处理电流读数。发出该命令后并且让仪器对话，读数发送到电脑。
            该命令不影响仪器设定。该命令不触发测量操作，仅要求最近可得的读数。在有新读数前，
            该命令返回的都是~旧~读~数。
            ps. means no buffer.
        MEASure[:VOLTage]?
            该命令用来通过电源的检测端子来量测并返回当前电流输出值。
        :return: float Current value.
        """
        data = self.session.query("MEASure:POWer?")
        if  data is None:
            #means error
            return 10000.0
        else:
            return float(data)

    def FindInService(self):
        pass

    def PreReadCurrents(self,samp_interval=0.01,samp_count = 100):
        self.session.write("*CLS")
        time.sleep(0.1)

        print("start working!")
        datas = []
        i = 0
        reading_count = samp_count

        while i < reading_count:
            time.sleep(samp_interval)
            datas.append(float(self.session.query("MEASure:CURR:DC?")))
            i += 1
            # print(self.session.query("SYST:ERR? "))

        return datas,len(datas)

    def ReadVoltages(self, q,samp_interval = 0.01,reading_time = 300):
        #reading_time: secends,300 means 5mins
        self.session.write("*CLS")
        time.sleep(0.1)

        print("start working!")

        i = 0
        reading_count = int(reading_time / samp_interval)

        while i < reading_count:

            time.sleep(samp_interval)

            data = float(self.session.query("MEASure:VOLTage:DC?"))

            if q.full() is True:
                pass
                # print(data)
            else:
                q.put(data)
            # print(float(self.session.query("FETCh:CURRent:DC?")))
            i += 1
            # print(self.session.query("SYST:ERR? "))

    def ReadCurrents(self,q,samp_interval = 0.01,reading_time = 300):

        self.session.write("*CLS")
        time.sleep(0.1)

        # reading_time: secends,300 means 5mins
        self.session.write("*CLS")
        time.sleep(0.1)

        print("start working!")

        i = 0
        reading_count = int(reading_time / samp_interval)

        while i < reading_count:

            time.sleep(samp_interval)

            data = float(self.session.query("MEASure:CURR:DC?"))

            if q.full() is True:
                pass
                # print(data)
            else:
                q.put(data)
            # print(float(self.session.query("FETCh:CURRent:DC?")))
            i += 1
            # print(self.session.query("SYST:ERR? "))

    def ReadPowers(self, q, samp_interval=0.01, reading_time=300):

                self.session.write("*CLS")
                time.sleep(0.1)

                # reading_time: secends,300 means 5mins
                self.session.write("*CLS")
                time.sleep(0.1)

                print("start working!")

                i = 0
                reading_count = int(reading_time / samp_interval)

                while i < reading_count:

                    time.sleep(samp_interval)

                    data = float(self.session.query("MEASure:POWer?"))

                    if q.full() is True:
                        pass
                        # print(data)
                    else:
                        q.put(data)
                    # print(float(self.session.query("FETCh:CURRent:DC?")))
                    i += 1
                    # print(self.session.query("SYST:ERR? "))

    def ShowCurve(self,samp_interval = 0.1,show_interval = 0.01,test_type = "CURRent",show_time = 300,ylimit = (0,1)):

        q = Queue(1024)

        #先让生产者产生0.1s的数据
        show = threading.Timer(0.1, showcurrent.ShowcurrentLine, [q,show_interval,ylimit])
        show.setDaemon(True)
        show.start()

        if test_type is "CURRent":
            self.ReadCurrents(q, samp_interval, show_time)
        elif test_type is "VOLTage":
            self.ReadVoltages(q,samp_interval,show_time)
        elif test_type is "POWer":
            self.ReadPowers(q, samp_interval, show_time)

    def TestDemo(self):
        self.session.write("*CLS")
        self.session.write("TRIGger:COUNT 3")
        print(self.session.query("MEASure:CURRent:DC?"))

if __name__ == "__main__":
    powerdevice = Device_IT6861A()
    powerdevice.SetVoltage("4.2")
    powerdevice.SetCurrent("2.0")
    powerdevice.OutputOnOff("ON")

    # powerdevice.ShowCurve(ylimit=(0,5))
    print powerdevice.PreReadCurrents()