import secrets
from gmssl import sm3, func

A = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
B = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
P = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
N = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
Gx = 0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
Gy = 0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0
G = (Gx, Gy)
h = 1



def EC_inv(p):   #椭圆曲线逆元
    return (p[0], P - p[1])

def EC_add(p, q):
    if p == 0:
        return q
    elif q == 0:
        return p
    else:
        if p[0] == q[0]:
            if (p[1] + q[1]) % P == 0:
                return 0
            elif p[1] == q[1]:
                return EC2p(p)
        elif p[0] > q[0]:
            p, q = q, p

        slope = ((q[1] - p[1]) * pow(q[0] - p[0], -1, P)) % P
        r_x = (slope ** 2 - p[0] - q[0]) % P
        r_y = (slope * (p[0] - r_x) - p[1]) % P
        return (r_x, r_y)

def EC_sub(p, q):   # 椭圆曲线减法
    return EC_add(p, EC_inv(q))


def EC2p(p):    #p+p
    slope = (3 * p[0] ** 2 + A) * pow(2 * p[1], -1, P) % P
    r_x = (slope ** 2 - 2 * p[0]) % P
    r_y = (slope * (p[0] - r_x) - p[1]) % P
    return (r_x, r_y)


def ECnp(s, p):
    n = p
    res = 0
    s_bin = bin(s)[2:]
    s_len = len(s_bin)

    for i in reversed(range(s_len)):  # 类快速幂思想
        if s_bin[i] == '1':
            res = EC_add(res, n)
        n = EC2p(n)

    return res


def get_bit_num(x):     #获得x的比特长度
    if isinstance(x, int):  # 当 x 是整数时
        return x.bit_length()
    elif isinstance(x, str):  # 当 x 是字符串时
        return len(x.encode()) * 8
    elif isinstance(x, bytes):  # 当 x 是字节串时
        return len(x) * 8
    return 0

def precom(ID, a, b, Gx, Gy, xA, yA):
    ENTL = str(get_bit_num(ID))
    joint = ENTL + ID + str(a) + str(b) + str(Gx) + str(Gy) + str(xA) + str(yA)
    joint_b = bytes(joint, encoding='utf-8')
    digest = sm3.sm3_hash(func.bytes_to_list(joint_b))
    return int(digest, 16)

# 生成公私钥对
def key_gen():
    sk = int(secrets.token_hex(32), 16)  # private key
    pk = ECnp(sk, G)  # public key
    return sk, pk

def inv(a, n):
    inv_a = pow(a, -1, n)
    return inv_a if inv_a != 0 else -1


def sm2_sign(sk, msg, ZA):
    M = ZA + msg
    M_b = bytes(M, encoding='utf-8')
    e = int(sm3.sm3_hash(func.bytes_to_list(M_b)), 16)

    while True:
        k = secrets.randbelow(N)
        a_dot = ECnp(k, G)
        r = (e + a_dot[0]) % N
        s = (inv(1 + sk, N) * (k - r * sk)) % N if r != 0 and r + k != N else 0
        if s != 0:
            return (r, s)

def sm2_verify(pk, ID, msg, signature):
    r, s = signature
    ZA = precom(ID, A, B, Gx, Gy, pk[0], pk[1])
    gangM = str(ZA) + msg
    gangM_b = bytes(gangM, encoding='utf-8')
    e = int(sm3.sm3_hash(func.bytes_to_list(gangM_b)), 16)
    t = (r + s) % N

    dot1 = ECnp(s, G)
    dot2 = ECnp(t, pk)
    dot = EC_add(dot1, dot2)
    R = (e + dot[0]) % N
    return R == r

