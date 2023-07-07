import random
from gmssl import sm3

#secp256k1曲线
p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
a = 0
b = 7
n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
Gx = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
Gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8


def mod_inverse(a, m):
    def extended_gcd(a, b):
        if b == 0:
            return a, 1, 0
        else:
            gcd, x, y = extended_gcd(b, a % b)
            return gcd, y, x - (a // b) * y

    gcd, x, _ = extended_gcd(a, m)
    if gcd == 1:
        return x % m
    else:
        raise ValueError("模逆不存在")

#求解勒让德符号和计算平方根
def get_QR(n, p):
    # 求勒让德符号
    def legendre(a, p):
        return pow(a, (p - 1) >> 1, p)

    class T:
        def __init__(self):
            self.p = 0
            self.d = 0

    w = 0

    def multiply_er(a, b, m):
        ans = T()
        ans.p = (a.p * b.p % m + a.d * b.d % m * w % m) % m
        ans.d = (a.p * b.d % m + a.d * b.p % m) % m
        return ans

    def power(a, b, m):
        ans = T()
        ans.p = 1
        ans.d = 0

        while b:
            if b & 1:
                ans = multiply_er(ans, a, m)
                b -= 1
            b >>= 1
            a = multiply_er(a, a, m)

        return ans

    while True:
        a = random.randrange(1, p)
        t = a * a - n
        w = t % p
        if legendre(w, p) + 1 == p:
            break

    tmp = T()
    tmp.p = a
    tmp.d = 1
    ans = power(tmp, (p + 1) >> 1, p)

    if ans.p < p - ans.p:
        y1 = ans.p
        y2 = p - ans.p
    else:
        y1 = p - ans.p
        y2 = ans.p

    return y1, y2

# 计算两个点的和
def calculate_p_and_q(x1, y1, x2, y2, a, p):
    if (x1, y1) == (x2, y2):
        m = (3 * x1 * x1 + a) % p
        inv = mod_inverse(2 * y1, p)
    else:
        m = ((y2 - y1) % p + p) % p
        inv = mod_inverse((x2 - x1) % p, p)

    k = (m * inv) % p
    x3 = (k * k - x1 - x2) % p
    y3 = (k * (x1 - x3) - y1) % p

    return [x3, y3]

#计算椭圆曲线上的点乘
def calculate_2p(p_x, p_y, a, p):
    return calculate_p_and_q(p_x, p_y, p_x, p_y, a, p)

def calculate_np(p_x, p_y, n, a, b, p):
    p_value = ["0", "0"]
    while n != 0:
        if n & 1:
            p_value = calculate_p_and_q(*p_value, p_x, p_y, a, p)
        n >>= 1
        p_temp = calculate_2p(p_x, p_y, a, b, p)
        p_x, p_y = p_temp[0], p_temp[1]
    return p_value

def get_bitsize(num):
    size = 0
    while num > 0:
        size += 1
        num //= 256
    return size

def int_to_bytes(num):
    return num.to_bytes(get_bitsize(num), byteorder='big', signed=False)

def bytes_to_int(byte_array):
    return int.from_bytes(byte_array, byteorder='big')

# 将消息哈希值映射到椭圆曲线上的点
def hash_to_ECpoint(msg):
    if isinstance(msg, str):
        num = msg.encode()
    else:
        num = int_to_bytes(msg)

    temp = sm3.sm3_hash(list(num))
    x = int(temp, 16)
    num_i = bytes_to_int(num)
    x_bytes = int_to_bytes(x)
    i = 0

    while True:
        temp = int_to_bytes(i) + x_bytes
        temp = sm3.sm3_hash(list(temp))
        x = int(temp, 16) % p
        y1, y2 = get_QR(x, p)

        if y1 != 0:
            y = y1 if num_i % 2 == 0 else y2
            return x, y
        else:
            i += 1

if __name__ == '__main__':
    # 计算点G1和点G2的和
    G1=hash_to_ECpoint("jzh")
    G2=hash_to_ECpoint("sdu")
    G3=calculate_p_and_q(*G1,*G2,a,p)
    print(G3)
