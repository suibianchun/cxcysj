**Project12: verify the above pitfalls with proof-of-concept code**

**实验任务图：**

![image](https://github.com/suibianchun/cxcysj/assets/138552183/6326fdfb-1ecd-41f3-a62a-ad0fcd3f89f2)

完成了对ECDSA，leaking k导致d泄露、reusing k导致d泄露、两个user使用相同的k,可以互相推测对方的私钥、
验证(r,s) and (r,-s)均为合法签名、ECdsa与Schnorr使用相同的d和k导致d泄露这几项的实现。

**介绍：**

![image](https://github.com/suibianchun/cxcysj/assets/138552183/db6dd54d-b522-4c77-b4a3-c3b0150bb095)

**实验过程：**

首先，实现了ECDSA签名算法。ECDSA是一种基于椭圆曲线的数字签名算法，用于对消息进行签名和验证。通过给定的私钥和随机数，可以生成消息的签名，然后通过公钥来验证签名的有效性。这部分核心代码是ECdsa_Sign和ECdsa_Verify函数。

其次，实现了泄露随机数k导致私钥泄露的攻击。当随机数k泄露后，可以利用已知的签名值r、参数n、随机数k、签名值s和消息m，计算出私钥d的值。这部分核心代码是leaking_k函数。

然后，实现了重复使用随机数k导致私钥泄露的攻击。当随机数k被重复使用时，可以利用已知的签名值r、签名值s、消息m1、消息m2和参数n，计算出私钥d的值。这部分核心代码是reusing_k函数。

接下来，代码实现了相同随机数k导致互相推测私钥的攻击。当相同的随机数k被用于不同的签名时，可以利用已知的签名值s1、消息m1、签名值s2、消息m2、签名值r、私钥d1、私钥d2和参数n，来判断是否能够互相推测出对方的私钥。这部分核心代码是same_k函数。

最后，代码实现了Schnorr签名算法的签名操作，并展示了当Schnorr签名和ECDSA签名使用相同的私钥和随机数时，可以通过已知的签名值推测出私钥的攻击方式。这部分核心代码是Schnorr_Sign和Schnorr_and_ECdsa函数。

**运行结果：**

![image](https://github.com/suibianchun/cxcysj/assets/138552183/cd087edd-deb5-4ce3-ad31-10a5825548f0)





