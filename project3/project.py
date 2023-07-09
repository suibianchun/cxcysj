def T(j):
    if j>=0 and j<=15:
        return int("79cc4519",16)
    elif j>=16 and j<=63:
        return int("7a879d8a",16)

def FF(X, Y, Z, j):
    return X ^ Y ^ Z if 0 <= j <= 15 else (X & Y) | (X & Z) | (Y & Z)

def GG(X, Y, Z, j):
    return X ^ Y ^ Z if 0 <= j <= 15 else (X & Y) | (~X & Z)

def zero_fill(a, n):
    return a.zfill(n)       # 将 a 补齐为 n 位的字符串

def cycle_shift_left( B, n):     # 循环左移 n 位
    n=n%32
    return ((B << n) ^ (B >> (32 - n)))%(2**32)

def P0(x):
    return x^(cycle_shift_left(x,9))^cycle_shift_left(x,17)

def P1(x):
    return x^(cycle_shift_left(x,15))^cycle_shift_left(x,23)

def message_extension(a):
    W1 = []
    W2 = []
    for i in range(int(len(a) / 8)):
        W1.append(int(a[8 * i:8 * i + 8],16))
    for j in range(16,68):
        temp=P1(W1[j-16] ^ W1[j-9] ^ cycle_shift_left(W1[j-3],15)) ^cycle_shift_left(W1[j-13],7)^W1[j-6]
        W1.append(temp)

    for j in range(0,64):
        W2.append(W1[j]^W1[j+4])

    W1.append(W2)
    return W1

#压缩函数
def CF(V,Bi):
    Bi=zero_fill(Bi,128)
    W=message_extension(Bi)   #消息扩展完的消息字
    A, B, C, D, E, F, G, H = [int(V[i:i + 8], 16) for i in range(0, 64, 8)]
    for j in range(0,64):
        temp=(cycle_shift_left(A,12) + E +cycle_shift_left(T(j),j)) %(2**32)
        SS1 = cycle_shift_left(temp, 7)
        SS2 = SS1 ^ cycle_shift_left(A, 12)
        TT1 = (FF(A, B, C, j) + D + SS2 + W[-1][j]) % (2 ** 32)
        TT2 = (GG(E, F, G, j) + H + SS1 + W[j]) % (2 ** 32)
        D, C, B, A, H, G, F, E = C, cycle_shift_left(B, 9), A, TT1, G, cycle_shift_left(F, 19), E, P0(TT2)

    result = ''.join(zero_fill(hex(X ^ int(V[i:i + 8], 16))[2:], 8) for i, X in zip(range(0, 64, 8), [A, B, C, D, E, F, G, H]))
    return result

def SM3(plaintext):
    temp = IV
    a = (len(plaintext) * 4 + 1) % 512
    if a <= 448:
        k = 448 - a
    else:
        k = 512 - a + 448
    m = plaintext + "8" + "0" * int((k + 1) / 4 - 1) + zero_fill(hex(len(plaintext) * 4)[2:], 16)
    block_len = int((len(plaintext) * 4 + k + 65) / 512)
    B = [m[128*i:128*i+128] for i in range(block_len)]
    for block in B:
        temp = CF(temp, block)
    return temp

def SM3_len_exten_attack(num_block, IV, plaintext):
    Vtemp = IV
    a = (len(plaintext) * 4 + 1) % 512
    k = 448 - a if a <= 448 else 512 - a + 448
    m = plaintext + "8" + "0" * int((k + 1) / 4 - 1) + zero_fill(hex(len(plaintext) * 4 + num_block * 512)[2:], 16)
    block_len = (len(plaintext) * 4 + k + 65) // 512
    B = [m[128*i:128*i+128] for i in range(block_len)]
    for block in B:
        Vtemp = CF(Vtemp, block)
    return Vtemp

def verify_len_extension_attack(num_block, IV2, add):
    plain_exten = '6566678'+119*'0'+'18'
    attack_plain = plain_exten + add
    if SM3(attack_plain) == SM3_len_exten_attack(num_block, IV2, add):
        return SM3(attack_plain), SM3_len_exten_attack(num_block, IV2, add), "长度扩展攻击成功"
    else:
        return None, None, "攻击失败"

if __name__ == '__main__':
    IV="7380166f4914b2b9172442d7da8a0600a96f30bc163138aae38dee4db0fb0e4e" #SM3的固定IV
    msg_hash="7e0d11e6455eaabda193edefcbc8f7a5ae68193e5ec4d27aa2fad0b11c8e5245"   #哈希值
    res = verify_len_extension_attack(1, msg_hash, "20230708")
    if res is not None:
        sm3_result, sm3_len_ex_result, status = res
        print("原始消息哈希值：",sm3_result)
        print("拓展攻击哈希值：",sm3_len_ex_result)
        print(status)
    else:
        print("攻击失败")




