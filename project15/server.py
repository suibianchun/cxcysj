import socket
import secrets
from SM2 import *

# 生成私钥d以及公钥P
def gen_d_P(P1):
    d = secrets.randbelow(N)
    P = EC_sub(EC_multi(inv(d, N), P1), G)
    return d, P

def receive_P1(server):
    data, addr = server.recvfrom(1024)
    data = data.decode()
    P1 = tuple(map(int, data.split(',')))
    return P1, addr


def comp_r_and_s2_3(d2, Q1, e):
    e = int(e, 16)
    k2 = secrets.randbelow(N)
    k3 = secrets.randbelow(N)
    Q2 = EC_multi(k2, G)
    x1, y1 = EC_add(EC_multi(k3, Q1), Q2)
    r = (x1 + e) % N
    if r == 0:
        return "Wrong: r = 0!"
    s2, s3 = d2 * k3 % N, d2 * (r + k2) % N
    return r, s2, s3


def receive_Q1_e(server):
    data, addr = server.recvfrom(1024)
    data = data.decode()
    index1 = data.index(',')
    index2 = data.index(';')
    Q1 = (int(data[:index1]), int(data[index1 + 1:index2]))
    e = data[index2 + 1:]
    return Q1, e, addr

# 与client的交互
def contact():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('', 8090))
    while 1:
        P1, addr = receive_P1(server)
        d2, P = gen_d_P(P1)
        # 公开公钥P,将公钥发给client
        print("公钥为:")
        print(P)
        data = str(P[0]) + ',' + str(P[1])
        server.sendto(data.encode(), addr)
        Q1, e, addr = receive_Q1_e(server)
        r, s2, s3 = comp_r_and_s2_3(d2, Q1, e)
        # 发送r,s2,s3给client
        data = str(r) + ',' + str(s2) + ';' + str(s3)
        server.sendto(data.encode(), addr)
    s.close()


if __name__ == '__main__':
    print("Server端：")
    print()
    contact()

