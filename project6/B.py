import socket
import hashlib

HOST_A = 'localhost'  # A 的主机地址
PORT_A = 9000         # A 的端口号

HOST_C = 'localhost'  # C 的主机地址
PORT_C = 9001         # C 的端口号

# 创建 socket 对象
sock_a = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 连接到 A 端
sock_a.bind((HOST_A, PORT_A))
sock_a.listen()

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


print('等待 A 连接...')

# 接受 A 端的连接
conn_a, addr_a = sock_a.accept()
print('已连接 A:', addr_a)

# 连接到 C 端
sock_c.connect((HOST_C, PORT_C))
print('已连接 C:', (HOST_C, PORT_C))

while True:
    # 接收 A 发送的消息
    data1 = conn_a.recv(1024)
    if not data1:
        break
    print('来自 A 的消息:', data1.decode())

    data2 = conn_a.recv(1024)
    if not data2:
        break
    print('来自 A 的消息:', data2.decode())

    # B 发送消息给 C
    d0 = 2000 - 1978
    p = hash_iterations(data1.decode(), d0)   #data1是s


    sock_c.sendall(p.encode())
    sock_c.sendall(data2)

    print("p:",p)
    print("sig:",data2.decode())


# 关闭连接
conn_a.close()
sock_c.close()
