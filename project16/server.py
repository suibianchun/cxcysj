import socket
from SM2 import *

# 生成私钥d以及公钥P
def gen_d_P(P1):
    d = secrets.randbelow(N)
    P = EC_sub(ECnp(inv(d, N), P1), G)
    return d, P

def receive_P1(server):
    data, addr = server.recvfrom(1024)
    data = data.decode()
    P1 = tuple(map(int, data.split(',')))
    return P1, addr


def recv_T1_and_comp_T2(d2, server):
    data, addr = server.recvfrom(1024)
    data = data.decode()
    try:
        T1_x, T1_y = map(int, data.split(','))
        d2_inv = inv(d2, N)
        T2_x, T2_y = ECnp(d2_inv, (T1_x, T1_y))
        # 将 T2 转换为字符串并发送回客户端
        response = f"{T2_x},{T2_y}"
        server.sendto(response.encode(), addr)
    except ValueError:
        print("Invalid data format.")


def contact():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('', 13800))
    while 1:
        P1, addr = receive_P1(server)
        d2, P = gen_d_P(P1)
        # 对消息进行加密,生成密文
        msg = "jzh_sdu"
        print("Client需要恢复的明文消息为:", msg)
        ciphertext = SM2_enc(msg, P)
        # 将密文发送给client
        data = str(ciphertext)
        server.sendto(data.encode(), addr)
        recv_T1_and_comp_T2(d2, server)
    server.close()

if __name__ == '__main__':
    print("Server端：")
    print()
    contact()
