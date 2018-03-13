#!/usr/bin/python
#-*-coding:utf-8 -*-
import visa
import sys
import time
import device_34972A
import device_IT6861A

class  PowerManagerBase(object):
    def __init__(self,LoadFile = False,):
        '''

        description:
            这里要做的是接口，直接面向用户的最外一层，因此需要搭建龙骨
            ps. 如果你读过优秀的开源源码的话就会发现这个base层最好把属性都定义到这里来，
                同时只定义接口跟规则，具体实现是由lib跟用户来做的，这就好比发改委是不会来做生意、耕地的活，
                他们只会引导大方向，进行宏观调控，然后传达给下一级，下一级也是如此，经过“中间层”的层层传导
                最终才传导到“人民”这儿来。
                也就是说上层只定方向、提需求，因此需要眼界、需要决策；
                中间层承上启下，需要理解（解释）和引导（链接）；
                下层唯一需要的就是执行力，快速执行快速反馈切输出输出口均是唯一的，确定的，信息熵为0的；
        LoadFile：
            假如是本地跑，就使用界面配置就好；
            假如是在ATC上跑，那么是需要传一个配置信息的；

        开启一个后台线程：
            负责寻找当前连接的设备，并作相应的注册管理及设备分类


       0  :param LoadFile:
        '''
        # default values, may be overridden in subclasses that do not support all values

        POWERDEVICE = ("IT6861A")
        DATAQCQUISITIONDEVICE = ("34972A")

        self._PowerDevice = None

        pass
    def PowerDevice(self,):
        pass