import socket


HOST_B = 'localhost'  # B 的主机地址
PORT_B = 9000         # B 的端口号

# 创建 socket 对象
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 连接到 B 端
sock.connect((HOST_B, PORT_B))


import random
import hashlib
import hmac

def generate_signature(message, private_key):
    # 将私钥转换为 bytes 格式
    private_key_bytes = private_key.encode('utf-8')
    # 使用 HMAC-SHA256 算法生成签名
    signature = hmac.new(private_key_bytes, message.encode('utf-8'), hashlib.sha256).hexdigest()
    return signature


def sha256_hash(message):
    # 创建 SHA256 哈希对象
    sha256_hasher = hashlib.sha256()
    # 更新哈希对象的输入
    sha256_hasher.update(message.encode("utf-8"))
    # 计算哈希值
    hash_value = sha256_hasher.hexdigest()

    return hash_value

def hash_iterations(data, iterations):
    for _ in range(iterations):
        data = sha256_hash(str(data))

    return data


#Trusted Issuer
seed=random.randint(1,2**128)
s=sha256_hash(str(seed))
k=2100-1978

private_key = "jzh"
c=hash_iterations(s,k)
sig=generate_signature(str(c),private_key)
print("c:",c)
print("s:",s)
print("sig:",sig)

# 发送消息给 B
sock.sendall(s.encode())
sock.sendall(sig.encode())


# 关闭连接
sock.close()
