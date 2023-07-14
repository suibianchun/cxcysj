import socket
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

private_key = "jzh"

HOST_B = 'localhost'  # B 的主机地址
PORT_B = 9001         # B 的端口号

# 创建 socket 对象
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 绑定端口并监听 B 端连接
sock.bind((HOST_B, PORT_B))
sock.listen()

print('等待 B 连接...')

# 接受 B 端的连接
conn_b, addr_b = sock.accept()
print('已连接 B:', addr_b)


# 接收 B 发送的消息
data1 = conn_b.recv(1024)
data2 = conn_b.recv(1024)


d1 = 2100-2000
p=data1.decode()
print("p:", p)
cc = hash_iterations(p, d1)
print("cc:",cc)
sig1 = generate_signature(str(cc), private_key)
print("sig:",data2.decode())
print("sig1:",sig1)


# 关闭连接
conn_b.close()
