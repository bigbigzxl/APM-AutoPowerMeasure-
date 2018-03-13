#! /usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Queue
#import matplotlib.axes._axes.Axes
from matplotlib.widgets import Button
import threading
import time
import random
from multiprocessing import Queue
from Queue import Empty
"""
class showcurrent(object):
    def __init__(self):
        self.i = 0
        self.xdata = range(0, 60, 1)
        self.ydata_list = [[ 1 for col in range(60)] for row in range(45)]#np.random.normal()
        self.ydata_list_status = "idle"
        self.line = ''
        self.cur_channel = 0
        self.bn_pos = []
        self.ax = None
       # self.timer = threading.Timer(1.0, self.auto_flush, ["zxl"]).start()
        #self.init_pic()#这个要放在最后面，否则的话画面就不会动了，也就是说plt.show()之后，就在这个页面循环了，那么我后面的定时器函数就不会执行了

    def init_pic(self):
        fig, self.ax = plt.subplots()
        self.ax.set_ylim([0, 500])
        plt.subplots_adjust(bottom=0.15, top=0.95, left=0.05, right=0.95)
        #self.line, = plt.plot(self.xdata, self.ydata_list[self.cur_channel], 'r-o', ms=8, alpha=0.55)
        for i in range(45):
            self.ax.plot(self.xdata,self.ydata_list[i])
        plt.show()

    def auto_flush(self,name):
        #print "hello %s\n" % name
        self.updata_data()
        self.draw_lines()

        self.timer = threading.Timer(0.5, self.auto_flush, ["zxl"])
        self.timer.start()
    def get_datalist(self):
        pass
    def start(self):
        self.init_pic()

    def updata_data(self,datalist):
        for data in datalist:
            if data >0 and data < 2000:
                pass
            else:
                print("INA219 ERROR! current=%d mA"%data)
                data = 0
            self.ydata_list[datalist.index(data)].pop(0)
            self.ydata_list[datalist.index(data)].append(data)

    def draw_lines(self):
        for i in range(45):
            self.ax.plot(self.xdata,self.ydata_list[i])
        plt.show()


    def change_pic(self,event):
        #首先获取到按键的坐标，一定要是百分比相对位置那个参数，不能是pix或者数据xdata位置的参数，因为这样随着放大变小参数是会变的；
        #然后将参数到那个数组里面去找，找到了的话就返回其索引值，代表的是点击的哪个按钮
        ax = event.inaxes #Axes(0.6055,0.07;0.03x0.04)得到的就是按钮那个小小的axes
        #plt.getp(ax_obj)#:6666666666!!! 读取属性
        '''
    adjustable = box
    agg_filter = None
    alpha = None
    anchor = C
    animated = False
    aspect = auto
    autoscale_on = True
    autoscalex_on = True
    autoscaley_on = True
    axes = Axes(0.01,0.02;0.03x0.04)
    axes_locator = None
    axis_bgcolor = (0.0, 0.5, 0.0, 1)
    axisbelow = line
    children = [<matplotlib.text.Text object at 0x0000000007955DA...
    clip_box = None
    clip_on = True
    clip_path = None
    contains = None
    cursor_props = (1, (0.0, 0.0, 0.0, 1))
    data_ratio = 1.0
    default_bbox_extra_artists = [<matplotlib.text.Text object at 0x0000000007955DA...
    facecolor = (0.0, 0.5, 0.0, 1)
    fc = (0.0, 0.5, 0.0, 1)
    figure = Figure(640x480)
    frame_on = True
    gid = None
    images = <a list of 0 AxesImage objects>
    label =
    legend = None
    legend_handles_labels = ([], [])
    lines = <a list of 0 Line2D objects>
    navigate = False
    navigate_mode = None
    path_effects = []
    picker = None
    position = Bbox(x0=0.01, y0=0.02, x1=0.04, y1=0.06)
    rasterization_zorder = None
    rasterized = None
    renderer_cache = <matplotlib.backends.backend_agg.RendererAgg objec...
    shared_x_axes = <matplotlib.cbook.Grouper object at 0x0000000004D6...
    shared_y_axes = <matplotlib.cbook.Grouper object at 0x0000000004D6...
    sketch_params = None
    snap = None
    title =
    transform = IdentityTransform()
    transformed_clip_path_and_affine = (None, None)
    url = None
    visible = True
    window_extent = Bbox(x0=2.9, y0=6.1, x1=29.1, y1=32.3)
    xaxis = XAxis(6.400000,9.600000)
    xaxis_transform = BlendedGenericTransform(CompositeGenericTransform(...
    xbound = (0.0, 1.0)
    xgridlines = <a list of 0 Line2D xgridline objects>
    xlabel =
    xlim = (0.0, 1.0)
    xmajorticklabels = <a list of 0 Text xticklabel objects>
    xminorticklabels = <a list of 0 Text xticklabel objects>
    xscale = linear
    xticklabels = <a list of 0 Text xticklabel objects>
    xticklines = <a list of 0 Text xtickline objects>
    xticks = []
    yaxis = YAxis(6.400000,9.600000)
    yaxis_transform = BlendedGenericTransform(BboxTransformTo(Transforme...
    ybound = (0.0, 1.0)
    ygridlines = <a list of 0 Line2D ygridline objects>
    ylabel =
    ylim = (0.0, 1.0)
    ymajorticklabels = <a list of 0 Text yticklabel objects>
    yminorticklabels = <a list of 0 Text yticklabel objects>
    yscale = linear
    yticklabels = <a list of 0 Text yticklabel objects>
    yticklines = <a list of 0 Line2D ytickline objects>
    yticks = []
    zorder = 0
    points = [[ 0.01  0.02]  [ 0.04  0.06]]
        '''
        bbox = plt.getp(ax,"position")# position = Bbox(x0=0.01, y0=0.02, x1=0.04, y1=0.06)
        bn_pos_x = float('%.2f'%bbox.x0)
        bn_pos_y  = float('%.2f'%bbox.y0)
        try:
            index = self.bn_pos.index([bn_pos_x,bn_pos_y])#找到当前按钮在我的按钮阵列的位置，对应的就是我的按钮号，注意：展示出来的值比计算值要多1
            self.cur_channel = index#更改通道
            print index
        except:
            ax.set_title("unrecognized")
            print "button not exsit!"
        #print ("===========channel:",bbox.x0)
'''
"""
class ShowcurrentLine(object):
    def __init__(self,q,show_rate = 0.01,ylimit = (0,5)):
        self.q = q
        self.cur_data = 0
        self.ShowRate = show_rate
        plt.style.use('fivethirtyeight')
        self.i=0
        self.line = None#['None' for i in range(45)]
        self.x =  range(0, 600,1)
       # print len(self.x),self.x
        self.y = [0 for i  in range(600) ]#[[0 for i  in range(60) ] for j in range(45)]
        #print len(self.y)#二维数组使用len（）函数时返回的是二维数组的长度：45
        #np.random.seed(19680801)

        self.fig, self.ax = plt.subplots()
        self.ax.set_ylim(ylimit[0],ylimit[1])
        self.line, = plt.plot(self.x,self.y,"o-")
        plt.subplots_adjust(bottom=0.05, top=0.95, left=0.05, right=0.95)
        '''
        for i in range(45):
            if i== 40:
                self.y[i] =  np.sin(self.x)+np.random.randint(1, 100,size=60)
                #print self.y[i]
                self.line[i], = plt.plot(self.x, self.y[i])
                #plt.draw()

                #self.y[i] = 1000
            else:
                self.y[i] = np.sin(self.x) + np.random.randint(1,50,size=60)
        '''
        self.ax.set_title("power datas")
        self.timer = threading.Timer(0.1, self.run)
        #self.timer.setDaemon(True)
        self.timer.start()
        plt.show()

    def run(self):
        self.cur_data = self.q.get(True)  # [[0,125],[1,120]·····[44,119]]
        #print "request...."
        self.y.pop(0)
        self.y.append(self.cur_data)
        #plt.plot(self.x, self.y)
        self.line.set_ydata(self.y)
        plt.draw()
        self.timer = threading.Timer(self.ShowRate/10, self.run)
        self.timer.start()


class SimulateData(object):
    def __init__(self,q):
        self.q = q
        self.datas = random.randint(1,100)
        self.q.put(self.datas)
        #print self.q.qsize()
        self.thread_data = threading.Timer(1, self.get_a_data)
        self.thread_data.setDaemon(True)
        self.thread_data.start()
    def get_a_data(self):
        for i in range(45):
            self.datas = random.randint(0,1)
        if q.full() is True:
            print("overflow````")
        else:
            self.q.put(self.datas)
        self.thread_data = threading.Timer(0.0001, self.get_a_data)
        #self.thread_data.setDaemon(True)
        self.thread_data.start()


class ShowCurrent(object):
    def __init__(self,q):
        plt.style.use('fivethirtyeight')
        self.q = q
        self.i=0
        self.cur_datas = []
        self.x =  range(0, 60,1)
        #print len(self.x),self.x
        self.ys = [[0 for i  in range(60) ] for j in range(45)]
        #print len(self.y)#二维数组使用len（）函数时返回的是二维数组的长度：45
        fig, self.ax = plt.subplots()
        plt.subplots_adjust(bottom=0.05, top=0.95, left=0.05, right=0.95)
        self.ax.set_title("45 boards current")
        self.timer = threading.Timer(1, self.run)
        self.timer.start()
        plt.show()

    def run(self):
        self.cur_datas = self.q.get(True)#[[0,125],[1,120]·····[44,119]]
        print "request...."
        for cur_data in self.cur_datas:
            if cur_data[0] in range(45):
                self.ys[cur_data[0]].pop(0)
                self.ys[cur_data[0]].append(cur_data[1])
            plt.plot(self.x,self.ys[cur_data[0]])

        plt.draw()

        self.timer = threading.Timer(0.1, self.run)
        self.timer.start()

class simulate_data(object):
    def __init__(self,q):
        self.q = q
        self.datas = [[0 for i in range(2)] for j in range(45)]
        for i in range(45):
            self.datas[i][0] = i
            self.datas[i][1] = random.randint(1,100)
        print self.datas
        self.q.put(self.datas)
        print self.q.qsize()
        self.thread_data = threading.Timer(2, self.get_45_data)
        self.thread_data.setDaemon(True)
        self.thread_data.start()
    def get_45_data(self):
        for i in range(45):
            self.datas[i][1] = random.randint(1,100)
        self.q.put(self.datas)
        self.thread_data = threading.Timer(0.3, self.get_45_data)
        self.thread_data.setDaemon(True)
        self.thread_data.start()

if __name__ == '__main__':
    q = Queue(1024)
    datas = SimulateData(q)
    dispay = ShowcurrentLine(q)










