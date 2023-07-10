import secrets
from gmssl import sm3, func
import socket
from SM2 import *

# 生成私钥d1与P1 = d^-1 * G
def gen_d_P():
    d1 = secrets.randbelow(N)
    P1 = EC_multi(inv(d1, N), G)
    return d1, P1

def receive_P(client):
    data, addr = client.recvfrom(1024)
    data = data.decode()
    P = tuple(map(int, data.split(',')))
    return P

def send_Q1_e(client):
    server_ID = "ID0"
    client_ID = "ID1"
    Z = server_ID + client_ID
    msg = "jzh_sdu"
    print("消息为:", msg)
    print("*"*80)
    m = Z + msg
    e = sm3.sm3_hash(func.bytes_to_list(bytes(m, encoding='utf-8')))
    k1 = secrets.randbelow(N)
    Q1 = EC_multi(k1, G)
    data = f"{Q1[0]},{Q1[1]};{e}"
    client.sendto(data.encode(), ("127.0.0.1", 8090))
    return k1

def receive_r_s2_s3(client):
    data, addr = client.recvfrom(1024)
    data = data.decode()
    index1 = data.index(',')
    index2 = data.index(';')
    r = int(data[:index1])
    s2 = int(data[index1 + 1:index2])
    s3 = int(data[index2 + 1:])
    return r, s2, s3

def gen_sign(d1, k1, r, s2, s3):
    s = ((d1 * k1) % N * s2 % N + d1 * s3 - r) % N
    if s not in (0, N - r):
        return r, s
    else:
        return "Wrong!"

# 与server的交互
def contact():
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 生成私钥与P1 = d^-1 * G
    d1, P1 = gen_d_P()
    data = str(P1[0]) + ',' + str(P1[1])
    # 将P1 = d^-1 * G发送给server
    client.sendto(data.encode(), ("127.0.0.1", 8090))
    P = receive_P(client)
    k1 = send_Q1_e(client)
    r, s2, s3 = receive_r_s2_s3(client)
    # 生成最终签名
    signature = gen_sign(d1, k1, r, s2, s3)
    r, s = signature
    print("签名为:")
    print("r:", r)
    print("s:", s)
    client.close()


if __name__ == '__main__':
    print("Client端：")
    print()
    contact()
    print("*"*80)

