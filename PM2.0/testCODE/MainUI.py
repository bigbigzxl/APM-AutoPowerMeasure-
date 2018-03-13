#! /usr/bin/env python
# -*- coding: utf-8 -*-

import binascii
import datetime
import logging
import os
import platform
import threading
# from COM import SerialHelper
from UI import SerialTool_PM
from multiprocessing import Queue
#import  unit_test_45cur_show as curshow
# import  show_current as curshow
from multiprocessing import Process, Queue
if platform.system() == "Windows":
    from  serial.tools import list_ports
elif platform.system() == "Linux":
    import glob, os, re

import Tkinter as tk
import ttk

class MainPowerManagerToolUI(SerialTool_PM.SerialToolUI):
    def __init__(self, master=None):
        super(MainPowerManagerToolUI, self).__init__()




if __name__ == '__main__':
    '''
    main loop
    '''
    root = tk.Tk()
    root.title("PowerManager Tool")
    if SerialTool.g_default_theme == "dark":
        root.configure(bg="#292929")
        combostyle = ttk.Style()
        combostyle.theme_use('alt')
        combostyle.configure("TCombobox", selectbackground="#292929", fieldbackground="#292929",
                             background="#292929", foreground="#FFFFFF")

    MainPowerManagerToolUI(master=root)

    # if os.name == 'nt':  # 判断现在正在实用的平台，Windows 返回 ‘nt'; Linux 返回’posix'
    #     root.iconbitmap(default='swallow_128px_1139556_easyicon.net.ico')
    root.resizable(False, False)
    root.mainloop()