**project9 AES / SM4 software implementation**

我选择的是对SM4进行加速

对SM4实现了三个版本，分别是原始版本、利用循环展开加速和多线程

根据运行结果可知，循环展开可以起到加速的效果，但效果并不是很理想；

在选择进程数为**16**时，多线程可对SM4加密进行较好效果的加速，加速比可达到**8倍**左右，对比结果如下图：

![image](https://github.com/suibianchun/cxcysj/assets/138552183/f54a43d2-001d-4f6c-9603-be70bd394a81)



