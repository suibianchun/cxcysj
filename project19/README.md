**Project19: forge a signature to pretend that you are Satoshi**

**实验原理图：**

![image](https://github.com/suibianchun/cxcysj/assets/138552183/5c93226b-00fe-42fd-8853-fb509a683e8a)

**主要函数：**

verify_without_m(e, n, G, r, s, P): 在不检查消息m的情况下进行验证。输入消息的哈希值e，随机数k，椭圆曲线的基点G，公钥P以及签名的两个部分r和s，验证签名的有效性并返回验证结果。

pretend(n, G, P): 模拟一个假设的身份，生成伪装的签名。随机选择两个数u和v，根据椭圆曲线上的运算生成伪装的签名，并使用verify_without_m函数验证签名的有效性。

**运行结果：**

![image](https://github.com/suibianchun/cxcysj/assets/138552183/c028feab-7dc2-48d9-a7fc-c6e758c2ea47)

