**Project13: Implement the above ECMH scheme**

椭圆曲线使用标准secp256k1曲线参数：

![image](https://github.com/suibianchun/cxcysj/assets/138552183/f4868f22-fd2d-4faa-8df0-ca78c63008ca)

**原理图：**

![image](https://github.com/suibianchun/cxcysj/assets/138552183/593ee427-b1cc-4f37-b138-20a3193f42fb)


ECMH的思想是：将哈希后的数映射到椭圆曲线上，然后利用椭圆曲线上的加法求解得到一个新的点并最终输出哈希值。

**运行结果：**

对"jzh"和"sdu"分别进行哈希，映射到椭圆曲线上相加得到最终结果：

![image](https://github.com/suibianchun/cxcysj/assets/138552183/21809c82-9077-4916-9e50-33ca5131fe24)
