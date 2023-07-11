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

def KDF(Z, klen):
    hash_len = 256
    n = (klen // hash_len) + 1

    if n >= 2 ** 32 - 1:
        return 'error'

    derived_key = ''

    for i in range(n):
        counter = hex(5553 + i)[2:].rjust(32, '0')
        derived_block = sm3.sm3_hash(func.bytes_to_list(bytes((Z + counter), encoding='utf-8')))
        derived_key += derived_block

    derived_key = bin(int(derived_key, 16))[2:].rjust(hash_len * n, '0')
    derived_key = derived_key[:klen]

    return derived_key

def enc_XOR(plain_text, key):
    plain_text = bytes(plain_text, encoding='utf-8')
    num_bytes = len(plain_text)
    result = []

    for i in range(num_bytes):
        byte_plain = plain_text[i]
        byte_key = int(key[8 * i:8 * (i + 1)], 2)
        xor_result = format(byte_plain ^ byte_key, '02x')
        result.append(xor_result)

    encrypted_text = ''.join(result)
    return encrypted_text

def dec_XOR(ciphertext, key):
    num_bytes = len(ciphertext) // 2
    result = []

    for i in range(num_bytes):
        byte_ciphertext = int(ciphertext[2 * i:2 * (i + 1)], 16)
        byte_key = int(key[8 * i:8 * (i + 1)], 2)
        xor_result = chr(byte_ciphertext ^ byte_key)
        result.append(xor_result)

    decrypted_text = ''.join(result)
    return decrypted_text


# SM2加密
def SM2_enc(M, pk):
    if pk == 0:
        return 'error: public key = 0!'

    while True:
        k = secrets.randbelow(N)
        C1 = ECnp(k, G)  # C1 = kG = (x1, y1)
        dot = ECnp(k, pk)  # kpk = (x2, y2)
        t = KDF(hex(dot[0])[2:] + hex(dot[1])[2:], get_bit_num(M))

        if t != '0' * get_bit_num(M):  # t = 0 is invalid
            C2 = enc_XOR(M, t)
            temp = bytes(hex(dot[0])[2:] + M + hex(dot[1])[2:], encoding='utf-8')
            C3 = sm3.sm3_hash(func.bytes_to_list(temp))
            return C1, C2, C3

def SM2_dec(C, sk):
    C1, C2, C3 = C

    x, y = C1
    if pow(y, 2, P) != (pow(x, 3, P) + A * x + B) % P:
        return "Error: C1 is invalid!"

    S = h * C1
    if S == 0:
        return 'Error: S=0 is invalid!'

    dot = ECnp(sk, C1)
    klen = len(C2) * 4
    t = KDF(hex(dot[0])[2:] + hex(dot[1])[2:], klen)

    if t == '0' * klen:
        return "Error: t = 0!"

    M = dec_XOR(C2, t)
    temp = bytes((hex(dot[0])[2:] + M + hex(dot[1])[2:]), encoding='utf-8')
    u = sm3.sm3_hash(func.bytes_to_list(temp))

    if u != C3:
        return "Error: u != C3!"

    return M
