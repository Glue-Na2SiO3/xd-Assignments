import random
import binascii

def mod_inverse(a, n):
    temp_t, new_temp = 0, 1
    remainder, new_remainder = n, a
    while new_remainder != 0:
        quotient = remainder // new_remainder
        # 调整赋值顺序，先更新remainder相关
        remainder, new_remainder = new_remainder, remainder - quotient * new_remainder
        temp_t, new_temp = new_temp, temp_t - quotient * new_temp
    if remainder > 1:
        raise ValueError("No modular inverse exists")
    return temp_t + n if temp_t < 0 else temp_t

small_prime_factors = [2, 3, 5, 7, 11, 13, 17, 19, 23]

def has_small_factor(p):
    for prime in small_prime_factors:
        if p % prime == 0:
            return True
    return False

def is_likely_prime(p, rounds=5):
    if p % 2 == 0:
        return p == 2  # 快速排除偶数（除2外）
    for _ in range(rounds):
        a = random.randint(1, p - 1)
        if pow(a, p - 1, p) != 1:
            return False
    return True

def get_likely_prime(bit_length):
    while True:
        # 用getrandbits生成指定比特数的随机数
        p = random.getrandbits(bit_length)
        # 确保在[2^(bit_length-1), 2^bit_length - 1]范围内
        p |= (1 << (bit_length - 1)) | 1  # 保证最高位为1且为奇数
        if not has_small_factor(p) and is_likely_prime(p):
            return p

def generate_rsa_keys(key_size):
    public_exp = 3
    half_bits = (key_size + 1) // 2 + 1  # 每个素数的比特数
    
    # 生成p，确保(p-1)不被3整除
    p = 7
    while (p - 1) % public_exp == 0:
        p = get_likely_prime(half_bits)
    
    # 生成q，确保q≠p且(q-1)不被3整除
    q = p
    while q == p or (q - 1) % public_exp == 0:
        q = get_likely_prime(half_bits)
    
    modulus = p * q
    totient = (p - 1) * (q - 1)
    private_exp = mod_inverse(public_exp, totient)
    return (public_exp, modulus), (private_exp, modulus)

def encrypt_number(pub_key, m):
    e, n = pub_key
    if not (0 <= m < n):
        raise ValueError(f"Message {m} out of range [0, {n-1}]")
    return pow(m, e, n)

def decrypt_number(priv_key, c):
    d, n = priv_key
    if not (0 <= c < n):
        raise ValueError(f"Ciphertext {c} out of range [0, {n-1}]")
    return pow(c, d, n)

def bytes_to_num(byte_str):
    # 用binascii转十六进制再转整数
    return int(binascii.hexlify(byte_str), 16) if byte_str else 0

def num_to_bytes(num):
    if num == 0:
        return b""
    # 计算所需字节数，确保无前置零
    byte_length = (num.bit_length() + 7) // 8
    return num.to_bytes(byte_length, byteorder='big')

def encrypt_byte_string(pub_key, byte_data):
    e, n = pub_key
    # 计算每块最大字节数
    max_block_len = (n.bit_length() - 1) // 8
    blocks = [byte_data[i:i+max_block_len] for i in range(0, len(byte_data), max_block_len)]
    encrypted_blocks = []
    for block in blocks:
        m = bytes_to_num(block)
        c = encrypt_number(pub_key, m)
        enc_block = num_to_bytes(c)
        # 统一每块密文长度，便于解密时分块
        enc_block_len = (n.bit_length() + 7) // 8
        enc_block = enc_block.rjust(enc_block_len, b'\x00')
        encrypted_blocks.append(enc_block)
    return b''.join(encrypted_blocks)

def decrypt_byte_string(priv_key, encrypted_data):
    d, n = priv_key
    enc_block_len = (n.bit_length() + 7) // 8
    blocks = [encrypted_data[i:i+enc_block_len] for i in range(0, len(encrypted_data), enc_block_len)]
    decrypted_blocks = []
    for block in blocks:
        c = bytes_to_num(block)
        m = decrypt_number(priv_key, c)
        dec_block = num_to_bytes(m)
        # 所有块都去除前导零
        decrypted_blocks.append(dec_block.lstrip(b'\x00'))
    return b''.join(decrypted_blocks)

if __name__ == '__main__':
    # 测试128位密钥
    pub, priv = generate_rsa_keys(128)
    test_data = b'test RSA implementation'
    encrypted = encrypt_byte_string(pub, test_data)
    decrypted = decrypt_byte_string(priv, encrypted)
    
    if test_data != decrypted:
        raise AssertionError(f"Test failed: original {test_data}, decrypted {decrypted}")
    print(f"测试成功！原始数据: {test_data.decode()}, 解密后: {decrypted.decode()}")
    
    # 测试数字加密
    test_num = 42
    encrypted_num = encrypt_number(pub, test_num)
    decrypted_num = decrypt_number(priv, encrypted_num)
    assert test_num == decrypted_num, f"数字测试失败: 原始{test_num}, 解密后{decrypted_num}"
    print(f"数字测试成功: 原始{test_num}, 解密后{decrypted_num}")