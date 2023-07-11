import math
import random

def XGcd(a, m):
    if math.gcd(a, m) != 1:
        return None
    return pow(a, -1, m)


def EC_add(m, n):
    if (m == 0):
        return n
    if (n == 0):
        return m
    res = []
    if (m != n):
        if (math.gcd(m[0] - n[0], p) != 1 and math.gcd(m[0] - n[0], p) != -1):
            return 0
        else:
            k = ((m[1] - n[1]) * XGcd(m[0] - n[0], p)) % p
    else:
        k = ((3 * (m[0] ** 2) + a) * XGcd(2 * m[1], p)) % p
    x = (k ** 2 - m[0] - n[0]) % p
    y = (k * (m[0] - x) - m[1]) % p
    res.append(x)
    res.append(y)
    return res


def calculate_np(n, p):
    if n == 0:
        return 0
    if n == 1:
        return p
    res = p
    while (n >= 2):
        res = EC_add(res, p)
        n = n - 1
    return res

def ECdsa_Sign(m, n, G, d,k):
    R = calculate_np(k, G)
    r = R[0] % n
    e = hash(m)
    s = (XGcd(k, n) * (e + d * r)) % n
    return r, s

def ECdsa_Verify(m, n, G, r, s, P):
    e = hash(m)
    w = XGcd(s, n)
    w = EC_add(calculate_np((e * w) % n, G), calculate_np((r * w) % n, P))

    result = (w != 0) and (w[0] % n == r)
    print(str(result).lower())
    return result


# 不验证m的验证算法
def verify_without_m(e, n, G, r, s, P):
    w = XGcd(s, n)
    v1 = (e * w) % n
    v2 = (r * w) % n
    w = EC_add(calculate_np(v1, G), calculate_np(v2, P))
    if (w == 0):
        print('false')
        return False
    else:
        if (w[0] % n == r):
            print('true')
            return True
        else:
            print('false')
            return False

# pretend that you are Satoshi
def pretend(n, G, P):
    u = random.randrange(1, n - 1)
    v = random.randrange(1, n - 1)
    r1 = EC_add(calculate_np(u, G), calculate_np(v, P))[0]
    e1 = (r1 * u * XGcd(v, n)) % n
    s1 = (r1 * XGcd(v, n)) % n
    verify_without_m(e1, n, G, r1, s1, P)


if __name__ == '__main__':
    a = 3
    b = 7
    p = 23
    G = [6, 9]
    n = 29
    k = 3
    d = 7

    P = calculate_np(d, G)
    m1 = 'jzh'
    m2 = "sdu"

    print("签名和验证：")
    r,s=ECdsa_Sign(m1,n,G,d,k)
    print("签名为:",r,s)
    print("验证结果为：")
    ECdsa_Verify(m1, n, G, r, s, P)
    print()

    print("pretend that you are Satoshi：")
    print("伪装结果为：")
    pretend(n, G, P)



