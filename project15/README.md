**Project15: implement sm2 2P sign with real network communication**

**实验原理图：**

![image](https://github.com/suibianchun/cxcysj/assets/138552183/34689989-f8bd-4fd7-835f-a7c7a258ab6f)

**实现过程：**

首先实现SM2.py，在该段代码里通过实现SM2中各部件的基本功能，最后定义了SM2签名函数sm2_sign，用于对给定的消息进行签名
以及SM2验证函数sm2_verify，用于验证给定的签名是否有效。

**server.py：**

通过gen_d_P()函数生成私钥d2和对应的公钥P。

通过UDP Socket监听端口8090，等待与Client端的交互。

接收到Client发送的P1值后，调用receive_P1()函数将其接收。

将生成的公钥P发回给Client端，即通过UDP Socket向Client发送P的坐标。

接收到Client发送的Q1和e值后，调用receive_Q1_e()函数将其接收并解析为元组。

调用comp_r_and_s2_3()函数计算签名中的r、s2和s3值。

将计算得到的r、s2和s3通过UDP Socket发送给Client。

**client.py：**

首先，通过gen_d_P()函数生成私钥d1和对应的公钥P1。

创建一个UDP Socket用于与Server端进行交互。

将生成的公钥P1发送给Server端，即通过UDP Socket向Server发送P1的坐标。

接收Server返回的公钥P值，即通过UDP Socket接收P的坐标。

发送Q1和e值给Server端，即通过UDP Socket向Server发送Q1的坐标和e值。

接收Server返回的r、s2和s3值，即通过UDP Socket接收r、s2和s3。

调用gen_sign()函数生成最终的签名，打印签名结果。

**运行结果：**

![image](https://github.com/suibianchun/cxcysj/assets/138552183/5b62dd72-0117-426c-8d71-c6fbb630b43d)


