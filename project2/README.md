**Project2: implement the Rho method of reduced SM3**

**攻击原理**

从一个初始值出发，不断计算SM3值，就可能形成环，即通过迭代计算不断逼近碰撞。

![image](https://github.com/suibianchun/cxcysj/assets/138552183/450bee3a-9bb0-453a-98d2-31463bf39942)

**代码实现**

实现SM3算法，再通过Rho_attack函数进行攻击，该函数的作用是通过计算哈希值的方式寻找一个哈希碰撞，即找到两个不同的输入值，但它们经过哈希函数处理后得到相同的哈希值（前n比特）。

**核心函数**

![image](https://github.com/suibianchun/cxcysj/assets/138552183/07a6db69-d2a3-4e9a-a539-bd9ce483b39f)


**运行结果**

**8-bit：**

![image](https://github.com/suibianchun/cxcysj/assets/138552183/8172ef1f-5ac4-48b9-bd0a-a25b5a5ad072)

**16-bit：**

![image](https://github.com/suibianchun/cxcysj/assets/138552183/4e1c4c20-0369-4793-8cf2-815db6685277)



