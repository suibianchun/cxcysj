**Project16: implement sm2 2P decrypt with real network communication**

**实验原理图：**

![image](https://github.com/suibianchun/cxcysj/assets/138552183/5aa227c9-0b58-4cc5-9287-cfca055efde5)

**实验过程：**

首先实现SM2.py，在该段代码里通过实现SM2中各部件的基本功能，最后定义了SM2加密和解密函数，加密函数将明文 M 使用公钥 pk 进行加密，返回密文 C，
解密函数将密文 C 使用私钥 sk 进行解密，返回明文 M。

**server.py：**

**密钥生成：**

gen_d_P(P1) 函数用于生成服务器端的私钥 d 和公钥 P。它接受客户端发送的 P1 值作为参数，通过生成随机数 d 和椭圆曲线运算得到公钥 P。
接收客户端的请求：

receive_P1(server) 函数用于从客户端接收 P1 值，并将其解析为点坐标。

recv_T1_and_comp_T2(d2, server) 函数接收客户端发送的 T1 值，通过椭圆曲线运算计算出 T2 值，并将其转换为字符串发送回客户端。

**加密和解密：**

contact() 函数是服务器的主函数，其中包含了循环等待客户端连接的逻辑。

在循环中，调用 receive_P1(server) 函数接收客户端发送的 P1 值。

根据接收到的 P1 值，调用 gen_d_P(P1) 生成服务器的私钥 d 和公钥 P。

调用 SM2_enc(msg, P) 对明文消息 msg 使用公钥 P 进行加密，并将密文发送给客户端。

最后，调用 recv_T1_and_comp_T2(d2, server) 函数接收客户端发送的 T1 值，计算出 T2 值，并将其发送回客户端。

**client.py：**

**生成私钥和公钥：**

gen_d_P() 函数生成客户端的私钥 d1 和公钥 P1。它通过生成随机数 d1 和椭圆曲线运算得到公钥 P1。

**校验并计算 T1：**

check_and_comp(d1, C1) 函数接收服务器端发送的 C1，并校验其是否为零。如果 C1 等于零，则返回错误；否则，计算出 T1 = d1^-1 * C1。

**恢复明文消息：**

recov_msg(T2, C1, C2, C3) 函数根据服务器端发送的 T2、C1、C2 和 C3 恢复出明文消息。

首先，使用 T2 和 C1 进行点减法运算得到 (x2, y2)。

然后，将 x2、y2、C2 拼接在一起，使用 KDF 函数生成密钥 t。

使用 t 对 C2 进行异或解密得到明文消息 M。

最后，将 x2、M 和 y2 拼接在一起进行消息认证，计算出 u。

如果 u 等于 C3，则返回明文消息 M；否则，返回 "Wrong!"。

**与服务器端的交互：**

在 contact() 函数中，创建一个 UDP Socket，并连接到服务器端的地址和端口。

调用 gen_d_P() 生成客户端的私钥和公钥。

将公钥 P1 发送给服务器端。

接收服务器端发送的密文数据，包括 C1、C2 和 C3。

根据收到的数据调用 check_and_comp(d1, C1) 计算出 T1，并将 T1 发送给服务器端。

接收服务器端发送的 T2。调用 recov_msg(T2, C1, C2, C3) 恢复明文消息。


**运行结果**

![image](https://github.com/suibianchun/cxcysj/assets/138552183/0f68e697-deff-4d0a-bf53-64d3e85d77bc)
