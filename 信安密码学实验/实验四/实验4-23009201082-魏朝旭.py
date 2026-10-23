import random
import sympy
from sympy import isprime, randprime

# 1. 读取明文
PLAINTEXT_FILE = "secret0.txt"
try:
    with open(PLAINTEXT_FILE, "r") as f:
        plaintext = int(f.readline().strip())  # 去
except FileNotFoundError:
    print(f"错误：未找到明文文件 {PLAINTEXT_FILE}")
    exit(1)
except ValueError:
    print("错误：文件第一行必须是整数明文")
    exit(1)

# 2. 核心工具函数
def mod_pow(base, exp, mod):
    """快速模幂运算"""
    result = 1
    base %= mod
    while exp > 0:
        if exp & 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp >>= 1
    return result

def ext_gcd(a, b):
    """扩展欧几里得算法，返回(gcd, x, y)"""
    if b == 0:
        return a, 1, 0
    g, x, y = ext_gcd(b, a % b)
    return g, y, x - (a // b) * y

def find_primitive(p, q):
    """寻找模p的原根（p=2q+1，q为素数）"""
    while True:
        g = random.randint(3, p-3)  # 避开边界，提升效率
        if mod_pow(g, 2, p) != 1 and mod_pow(g, q, p) != 1:
            return g

# 3. 生成150位强素数p=2q+1（优化循环逻辑，确保符合要求）
print("=== 生成强素数p和素数q ===")
while True:
    q = randprime(10**149, (10**150 - 2) // 2)  # 确保p是150位
    p = 2 * q + 1
    if isprime(p) and len(str(p)) == 150:
        break
print(f"素数 q = {q}")
print(f"150位强素数 p = {p}\n")

# 4. 生成原根g和密钥对（补全中间数据显示）
print("=== 生成原根和密钥对 ===")
g = find_primitive(p, q)
a = random.randint(2, 15)  # 扩大范围，与原代码区分
y = mod_pow(g, a, p)  # 公钥g^a mod p
print(f"模p的原根 g = {g}")
print(f"私钥 a = {a}")
print(f"公钥 g^a mod p = {y}")
print(f"公钥对 (p, g, g^a)：\n{p}\n{g}\n{y}\n")

# 5. 加密过程（显示临时密钥k，补全要求）
print("=== 加密过程 ===")
k = random.randint(3, p-3)  # 优化k的范围，避免极端值
c1 = mod_pow(g, k, p)
c2 = (plaintext * mod_pow(y, k, p)) % p
print(f"临时密钥 k = {k}")  # 补全缺失的k显示
print(f"密文 C1 = {c1}")
print(f"密文 C2 = {c2}")
print(f"密文对 C = (C1, C2) = ({c1}, {c2})\n")

# 6. 解密过程（优化逆元计算，清晰显示对比结果）
print("=== 解密过程与验证 ===")
v = mod_pow(c1, a, p)
gcd_v, inv_v, _ = ext_gcd(v, p)
inv_v = inv_v % p  # 确保逆元为正数
decrypted = (c2 * inv_v) % p
print(f"原始明文 = {plaintext}")
print(f"解密明文 = {decrypted}")
print("=== 验证结果 ===")
print("✅ 解密正确！原始明文与解密明文一致" if plaintext == decrypted else "❌ 解密错误！明文不一致")