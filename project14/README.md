**Project14: Implement a PGP scheme with SM2**

**背景介绍**

PGP（Pretty Good Privacy）是一种常用的加密和认证方案，用于保护电子邮件和文件的机密性和完整性。SM2是中国国家密码管理局颁布的一种国家密码算法标准，基于椭圆曲线密码体制（ECC）。

PGP scheme with SM2是指将SM2算法与PGP方案结合使用，以提供更强大的加密和认证功能。在传统的PGP方案中，通常使用RSA或DSA算法来实现数字签名和加密操作。而PGP scheme with SM2则使用SM2算法来代替RSA或DSA算法。

SM2算法基于椭圆曲线密码体制，比传统的RSA或DSA算法具有更小的密钥尺寸和更高的安全性。通过结合PGP方案和SM2算法，可以在保护邮件和文件的机密性和完整性方面提供更强的保障。

**原理图**

![image](https://github.com/suibianchun/cxcysj/assets/138552183/e0a9c192-d86c-436e-85be-69b1f5334e94)

**实验过程**

加密时使用对称加密算法SM4加密消息，非对称加密算法SM2加密会话密钥；

解密时先使用SM2解密求得会话密钥，再通过SM4和会话密钥求解原消息。

在推荐参数的基础下，生成SM2的公私钥：

![image](https://github.com/suibianchun/cxcysj/assets/138552183/c6f17a41-2702-4c60-bc40-ac148ad6874d)

![image](https://github.com/suibianchun/cxcysj/assets/138552183/217014e3-7ee7-4562-b569-e5c040e9ceae)

**代码主要思路**

定义函数SM2_Encrypt和SM2_Decrypt，使用SM2算法加密和解密密钥。

定义函数PGP_Encrypt和PGP_Decrypt，用于使用SM4算法（CBC模式）加密和解密消息，并使用SM2加密和解密会话密钥。

定义会话密钥session_key和消息message。

调用PGP_Encrypt函数使用会话密钥将消息加密，返回加密后的值enc_value和加密后的会话密钥enc_key。

调用PGP_Decrypt函数解密加密后的值，并获取解密后的消息和会话密钥。

**运行结果**


![image](https://github.com/suibianchun/cxcysj/assets/138552183/ba4bc4c4-7e14-40f1-9b13-a6db09c0cef2)







