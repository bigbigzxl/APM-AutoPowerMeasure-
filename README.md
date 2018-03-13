# APM-AutoPowerMeasure-

AutoPowerMeasure System. Include hardware design, software, driver and so on.
**目前仅实现功能能用，代码完全还没组织、重构过，因此后续有时间慢慢修改！代码还是要简洁的好啊！**

# 自动化功耗测试系统

目标设备是平板、手机等中等功耗的设备，测试其整机工作电流、漏电流、模块分量电流等。

![](https://upload-images.jianshu.io/upload_images/4749583-2e50b616c6e75d5d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![](https://upload-images.jianshu.io/upload_images/4749583-5c186bf8a73fb22b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

## 系统结构

+ **硬件设备（包括测量设备、测量电路等）**


![](https://upload-images.jianshu.io/upload_images/4749583-1f4f6c24b45f3a5a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![](https://upload-images.jianshu.io/upload_images/4749583-fbdb7adb9d2b6834.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



+ **设备驱动（如VISA、下位机自定义驱动等）**

![](https://upload-images.jianshu.io/upload_images/4749583-3d0f12c4470c6573.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![](https://upload-images.jianshu.io/upload_images/4749583-6fc5c383b5383c4b.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![](https://upload-images.jianshu.io/upload_images/4749583-ae64eb2149a64e8f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


+ **上位机功能测试模块（如功耗测试、设备管理、功耗显示等）**

![](https://upload-images.jianshu.io/upload_images/4749583-621d3b070ec1c820.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![](https://upload-images.jianshu.io/upload_images/4749583-a59dc5af07de07dd.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
