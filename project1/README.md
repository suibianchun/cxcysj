**Project1: implement the naïve birthday attack of reduced SM3**

**攻击原理**

生日攻击的目标是找到两个具有相同哈希值的不同输入。攻击者首先选择一个初始的输入（也称为种子），并计算其哈希值。然后，攻击者生成一系列具有不同输入的消息，并计算它们的哈希值。攻击者在哈希值列表中搜索是否存在与初始种子的哈希值相同的值。在生日攻击下，输出长度为n的哈希函数，穷搜2^(n/2)次，即可以1/2的概率找到一次碰撞。

**代码分析**

代码的核心是find_collision(n)函数，实现搜索到碰撞的功能。首先，它初始化一个空字典dic用于存储哈希值和对应的数据。然后，给定一个初始数据data，通过调用sm3.sm3_hash函数计算其哈希值h。在一个循环中，它将当前的哈希值h的前n位作为键，将对应的数据data存入字典dic。接着，生成一个新的随机字符串s，将其编码为字节流，并使用sm3.sm3_hash函数计算新的哈希值h。如果当前哈希值的前n位在字典dic中不存在，则将其存入字典；否则，说明找到了碰撞。

**运行结果**

分别测试了24、28、32、36、40比特的碰撞，结果如下图：

![image](https://github.com/suibianchun/cxcysj/assets/138552183/16dce878-4c1e-44f2-ae9b-ea681c600ac4)

![image](https://github.com/suibianchun/cxcysj/assets/138552183/ea062735-bdc4-4690-b379-7286621445e2)

![image](https://github.com/suibianchun/cxcysj/assets/138552183/7e29d106-d637-45d5-a977-e33840b64e72)

![image](https://github.com/suibianchun/cxcysj/assets/138552183/d2b75e7c-e39a-4a09-be66-ed7ab0ba29ca)

![image](https://github.com/suibianchun/cxcysj/assets/138552183/9502d755-13e2-4bfd-b4c7-2994f347da4f)



