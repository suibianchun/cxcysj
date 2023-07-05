import time
import random
import string
from gmssl import sm3, func

def generate_random_str(length):
    characters = string.ascii_letters + string.digits + '`~!@#$%^&*'
    random_str = ''.join(random.choice(characters) for _ in range(length))
    return random_str


def find_collision(n):
    dic = {}
    data = b"202100460035"
    h = sm3.sm3_hash(func.bytes_to_list(data))
    start = time.time()

    while h[:n] not in dic:
        dic[h[:n]] = data
        s = generate_random_str(32)
        data = bytes(s.encode())
        h = sm3.sm3_hash(func.bytes_to_list(data))

    end = time.time()
    running_time=end-start
    return data, h, dic[h[:n]], running_time

if __name__ == '__main__':
    n = 8
    str1, hash1, str2, running_time = find_collision(n)

    print(f"找到 {n*4} 比特的碰撞")
    print("第一个字符串为:", str1)
    print("对应的哈希值为：",hash1)
    print("第二个字符串为:", str2)
    print("对应的哈希值为：", sm3.sm3_hash(func.bytes_to_list(str2)))   #找到碰撞
    print("运行时间为：",running_time,"s")
