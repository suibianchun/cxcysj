import math

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


#泄露k导致密钥泄露
def leaking_k(r, n, k, s, m):
    e = hash(m)
    d = (XGcd(r, n) * (k * s - e)) % n
    return d


def reusing_k(r1,s1,m1,s2,m2,n):
    e1=hash(m1)
    e2=hash(m2)
    d=((s1 * e2 - s2 * e1) * XGcd((s2 * r1 - s1 * r1), n)) % n
    return d


def same_k(s1,m1,s2,m2,r,d1,d2,n):
    e1=hash(m1)
    e2=hash(m2)
    dd1 = ((s1 * e2 - s2 * e1 + s1 * r * d2) * XGcd(s2 * r, n)) % n
    dd2 = ((s2 * e1 - s1 * e2 + s2 * r * d1) * XGcd(s1 * r, n)) % n
    if(dd1==d1 and d2==dd2):
        print("互相计算私钥成功")
        return True
    else:
        print("互相计算私钥失败")
        return False


def Schnorr_Sign(m, n, G, d,k):
    r = calculate_np(k, G)
    e = hash(str(r[0]) + m)
    s = (k + e * d) % n
    return r, s

# Schnorr_Sign签名、ecdsa签名使用相同的d，k，导致密钥泄露
def Schnorr_and_ECdsa(r1, s1, R, s2, m, n):
    e1 = int(hash(m))
    e2 = int(hash(str(R[0]) + m))
    d = ((s1 * s2 - e1) * XGcd((s1 * e2 + r1), n)) % n
    return d


if __name__ == '__main__':
    a = 2
    b = 2
    p = 17
    G = [5, 1]
    n = 19
    k = 2
    d = 5

    P = calculate_np(d, G)
    m1 = 'jzh'
    m2 = "sdu"

    print("1.签名和验证：")
    r,s=ECdsa_Sign(m1,n,G,d,k)
    print("签名为:",r,s)
    print("验证结果为：")
    ECdsa_Verify(m1, n, G, r, s, P)
    print()

    print("2.泄露k导致泄露d：")
    if (d == leaking_k(r,n,k,s,m1)):
        print("succeed")
    print()


    print("3.重用k导致泄露d：")
    r_1,s_1=ECdsa_Sign(m2,n,G,d,k)
    r_2,s_2=ECdsa_Sign(m1,n,G,7,k)
    if (d == reusing_k(r,s,m1,s_1,m2,n)):
        print("succeed")
    print()


    print("4.use the same k，互相推测私钥：")
    print("验证结果为：",same_k(s_1,m2,s_2,m1,r,5,7,n))
    print()


    print("5. 测试 r,-s是否为有效签名：")
    print("测试结果为：")
    ECdsa_Verify(m1, n, G, r, -s, P)
    print()


    print("6. Schnorr_Sign签名、ECdsa签名使用相同的d，k，导致泄露d：")
    r3, s3 = Schnorr_Sign(m1, n, G, d, k)
    dd = Schnorr_and_ECdsa(r, s, r3, s3, m1, n)
    print("破解是否成功：")
    print(d == dd)


