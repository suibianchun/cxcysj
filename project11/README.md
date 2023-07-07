**Project11: impl sm2 with RFC6979**

**SM2加密流程：**

![image](https://github.com/suibianchun/cxcysj/assets/138552183/8e57f2db-a6cf-4637-b111-417c625e8363)

**SM2解密流程：**

![image](https://github.com/suibianchun/cxcysj/assets/138552183/3ce52c26-8bd8-472f-ad7c-49fad97c926f)

**SM2系统参数：**

![image](https://github.com/suibianchun/cxcysj/assets/138552183/63b668e4-f54c-4129-852e-b2ea93c346d4)


**代码描述：**

首先定义了secp256k1曲线的参数，包括曲线方程的系数，素数p，基点G的坐标，私钥d等等。

接下来定义了一些基本的函数，如点加法、点乘法、置换函数P0和P1以及一些辅助函数。其中，置换函数用于对数据进行置换操作，LS函数用于逻辑左移操作，Ti函数根据索引返回常量值，Fi和Gi函数是压缩函数中的一部分，用于计算状态更新时的中间结果。

然后定义了padding函数，用于对数据进行填充，使其长度满足SHA-256算法的要求。

Extend函数将输入的数据B拆分成多个32位整数，并使用P1和LS函数对其进行扩展，得到额外的52个32位整数。

unsignedint_to_str函数用于将无符号整数转换为16进制字符串。

update函数是SHA-256算法的核心部分，实现了消息扩展和状态更新的过程。

Hash函数是SHA-256算法的入口函数，接收输入的消息m，进行填充、消息扩展和状态更新，最终返回更新后的初始向量IV。

KDF函数实现了密钥派生函数，根据输入的种子z和密钥长度klen生成密钥。（**这一步也是SM2结合RFC6979的关键**）

encrypt函数用于对消息m进行加密，首先将消息转换为二进制字符串，并进行填充，然后生成一个随机数k，并使用椭圆曲线乘法计算公钥点(x2, y2)，再使用KDF函数生成密钥t，将密钥与消息进行异或运算得到密文c2，最后生成MAC值c3。

decrypt函数用于对密文c1、c2、c3进行解密，首先根据c1计算得到私钥点(x1, y1)，再使用椭圆曲线乘法计算出私钥点(x2, y2)，使用KDF函数生成密钥t，将密文c2与密钥t进行异或运算得到明文m，再计算MAC值u，最后将密文和计算得到的MAC值与输入的MAC值c3进行比较，如果相等则解密成功，否则解密失败。

**正确性验证：**

对消息"jzh"先加密再解密，仍可得到"jzh"

![image](https://github.com/suibianchun/cxcysj/assets/138552183/304b8e4f-94e9-4afa-89b3-5894b88ec30c)


