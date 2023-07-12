import hashlib


def EC_add(p1, p2):
    if (p1 is None):
        return p2
    if (p2 is None):
        return p1
    if (p1[0] == p2[0] and p1[1] != p2[1]):
        return None
    if (p1 == p2):
        lam = (3 * p1[0] * p1[0] * pow(2 * p1[1], p - 2, p)) % p
    else:
        lam = ((p2[1] - p1[1]) * pow(p2[0] - p1[0], p - 2, p)) % p
    x3 = (lam * lam - p1[0] - p2[0]) % p
    return (x3, (lam * (p1[0] - x3) - p1[1]) % p)


def calculate_np(p, n):
    res = None
    for i in range(256):
        if ((n >> i) & 1):
            res = EC_add(res, p)
        p = EC_add(p, p)
    return res


def point_to_bytes(p):
    return (b'\x03' if p[1] & 1 else b'\x02') + p[0].to_bytes(32, byteorder="big")


def sha256(m):
    return int.from_bytes(hashlib.sha256(m).digest(), byteorder="big")


#检查点是否在椭圆曲线上
def on_curve(point):
    return (pow(point[1], 2, p) - pow(point[0], 3, p)) % p == 7


def jacobi(x):
    return pow(x, (p - 1) // 2, p)


def Schnorr_Sign(msg, seckey):
    k = sha256(seckey.to_bytes(32, byteorder="big") + msg)
    R = calculate_np(G, k)
    if jacobi(R[1]) != 1:
        k = n - k
    e = sha256(R[0].to_bytes(32, byteorder="big") + point_to_bytes(calculate_np(G, seckey)) + msg)
    return R[0].to_bytes(32, byteorder="big") + ((k + e * seckey) % n).to_bytes(32, byteorder="big")


def Schnorr_Verify(msg, pubkey, sig):
    if (not on_curve(pubkey)):
        return False
    r = int.from_bytes(sig[0:32], byteorder="big")
    s = int.from_bytes(sig[32:64], byteorder="big")
    if r >= p or s >= n:
        return False
    e = sha256(sig[0:32] + point_to_bytes(pubkey) + msg)
    R = EC_add(calculate_np(G, s), calculate_np(pubkey, n - e))
    if R is None or jacobi(R[1]) != 1 or R[0] != r:
        return False
    return True


def Schnorr_Batch_Verify(pubkeys, ms, sigs):
    S = 0
    Rs = None
    Ps = None
    rands=[0]*len(pubkeys)  #初始化
    for i in range(len(pubkeys)):
        pubkey = pubkeys[i]
        sig = sigs[i]
        msg = ms[i]
        rands[i]=i+1
        if (not on_curve(pubkey)):
            return False
        r = int.from_bytes(sig[0:32], byteorder="big")
        s = int.from_bytes(sig[32:64], byteorder="big")
        if r >= p or s >= n:
            return False
        e = sha256(sig[0:32] + point_to_bytes(pubkey) + msg)
        c = pow(r, 3, p) + 7
        y = pow(c, (p + 1) // 4, p)
        if pow(y, 2, p) != c:
            return False

        a = rands[i]
        S = S + s * a
        Rs = EC_add(Rs, calculate_np((r, y), a))
        Ps = EC_add(Ps, calculate_np(pubkey, a * e))

    if calculate_np(G, S) != EC_add(Rs, Ps):
        return False
    return True


if __name__=='__main__':

    p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
    n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
    G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
     0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)

    k = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
    pk = calculate_np(G, k)

    #第一个签名验证
    msg1=0x0123456789012345678901234567890123456789abcdefabcedfabcdefabcedf.to_bytes(32, byteorder="big")
    sig1=Schnorr_Sign(msg1,k)
    print("第一个签名验证结果：",Schnorr_Verify(msg1,pk,sig1))

    #第二个签名验证
    msg2 = 0xabcdefabcedfabcdefabcedf0123456789012345678901234567890123456789.to_bytes(32, byteorder="big")
    sig2 = Schnorr_Sign(msg2, k)
    print("第二个签名验证结果：",Schnorr_Verify(msg2, pk, sig2))

    #第三个签名验证
    msg3 = 0xabcdefabcedfa25097bcdefabcedf01234567987465489198984894984987074.to_bytes(32, byteorder="big")
    sig3 = Schnorr_Sign(msg3, k)
    print("第三个签名验证结果：",Schnorr_Verify(msg3, pk, sig3))


    #以三个签名验证为例 batch verification
    msg=[msg1,msg2,msg3]
    sig=[sig1,sig2,sig3]
    print("Schnorr Batch Verify的结果：",Schnorr_Batch_Verify([pk], msg, sig))
