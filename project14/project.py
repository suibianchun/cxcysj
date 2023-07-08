from gmssl import sm2
from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT

#SM2公私钥
sk ='8a9d8be532a1079facdab30f0124e71c65baa92bc5e756a9479bd222319c62e2'
pk='3d426e0eaa1551b5a02e9716c680ac6155dedc0c7f476f0b32b5465ba6491440a680883ec4649f53bf3a55534f3f0b75041e12203606b8df892e8b6b4073d76b'


# 使用给定的公私钥创建SM2密码对象
def SM2_Encrypt(key):
    sm2_crypt = sm2.CryptSM2(public_key=pk, private_key=sk)
    enc_key = sm2_crypt.encrypt(key)
    return enc_key

def SM2_Decrypt(enc_data):
    sm2_crypt = sm2.CryptSM2(public_key=pk, private_key=sk)
    key = sm2_crypt.decrypt(enc_data)
    return key

def PGP_Encrypt(message, session_key):
    iv = b'\x00' * 16  # 初始化向量
    crypt_sm4 = CryptSM4()
    crypt_sm4.set_key(session_key, SM4_ENCRYPT)
    # 使用SM4算法的CBC模式进行加密
    enc_value = crypt_sm4.crypt_cbc(iv, message)
    # 使用SM2算法加密会话密钥
    enc_key = SM2_Encrypt(session_key)

    return enc_value, enc_key

def PGP_Decrypt(encrypt_value, enc_data):
    iv = b'\x00' * 16 
    crypt_sm4 = CryptSM4()
    session_key = SM2_Decrypt(enc_data)
    crypt_sm4.set_key(session_key, SM4_DECRYPT)
    decrypt_value = crypt_sm4.crypt_cbc(iv, encrypt_value)

    return decrypt_value, session_key

session_key = b'ABCDEFABCDEF123456789123456789'
message = b'JZH SDU'

enc_value, enc_key = PGP_Encrypt(message, session_key)
print(enc_value)
print(enc_key)

print()
decrypt_value, session_key = PGP_Decrypt(enc_value, enc_key)
print("解密的内容是：", decrypt_value)
print("会话密钥是：", session_key)




