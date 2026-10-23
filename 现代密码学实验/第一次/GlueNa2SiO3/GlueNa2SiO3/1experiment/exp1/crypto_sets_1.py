import base64
import sys

# --- 1. 频率分析表 ---
# 英文单字母频率表，用于评分 (值来自 C 代码，已转换为 ASCII 码的整数作为字典键)
# score_plaintext 函数将使用此表来判断解密后的文本是否接近自然英文。
ENGLISH_SCORES = {
    ord(' '): 0.15, ord('e'): 0.127, ord('t'): 0.091, ord('a'): 0.082, ord('o'): 0.075,
    ord('i'): 0.070, ord('n'): 0.067, ord('s'): 0.063, ord('h'): 0.061, ord('r'): 0.060,
    ord('d'): 0.043, ord('l'): 0.040, ord('c'): 0.028, ord('u'): 0.028, ord('m'): 0.024,
    ord('w'): 0.024, ord('f'): 0.022, ord('g'): 0.020, ord('y'): 0.020, ord('p'): 0.019,
    ord('b'): 0.015, ord('v'): 0.0098, ord('k'): 0.0077, ord('j'): 0.0015, ord('x'): 0.0015,
    ord('q'): 0.00095, ord('z'): 0.00074
}

# --- 2. 核心功能函数 ---

def hamming_distance(b1: bytes, b2: bytes) -> int:
    """计算两个等长字节序列的汉明距离（不同位的数量）。"""
    if len(b1) != len(b2):
        raise ValueError("输入字节序列长度必须相等。")
    # 对每个字节进行异或，然后计算结果中设置的位数（1的个数）
    return sum(bin(x ^ y).count('1') for x, y in zip(b1, b2))

def score_plaintext(data: bytes) -> float:
    """根据英文字母频率为解密后的数据评分，得分越高越可能是可读英文。"""
    score = 0.0
    for byte in data:
        # 将大写字母转换为小写，以便使用小写字母频率表 (C代码的逻辑)
        if ord('A') <= byte <= ord('Z'):
            byte = byte + (ord('a') - ord('A'))
        
        # 查找得分，非目标字符默认为 0.0
        score += ENGLISH_SCORES.get(byte, 0.0) 
    return score

def break_single_xor(ciphertext_block: bytes) -> bytes:
    """对单个字节块进行单字节XOR攻击，返回得分最高的密钥字节。"""
    best_score = -1.0
    best_key = 0
    
    for key in range(256):
        # 尝试使用当前密钥字节解密块
        decrypted_data = bytes(byte ^ key for byte in ciphertext_block)
        
        # 评分
        current_score = score_plaintext(decrypted_data)
        
        if current_score > best_score:
            best_score = current_score
            best_key = key
            
    return bytes([best_key])

def guess_keysize(data: bytes) -> int:
    """
    通过计算标准化汉明距离，猜测重复密钥XOR的密钥长度 (KEYSZIZE)。
    KEYSZIZE 取值范围为 2 到 40。
    """
    best_keysize = -1
    best_score = float('inf')
    
    # 按照 C 语言代码的逻辑，检查 KEYSZIZE 从 2 到 40
    for keysize in range(2, 41):
        
        # 如果数据不足 4 个块，则跳过
        if keysize * 4 > len(data):
             continue

        # 选取前 4 个块进行两两比较 (共 6 组)
        blocks_to_compare = 4
        total_normalized_distance = 0.0
        comparison_count = 0
        
        for i in range(blocks_to_compare):
            block_i = data[i * keysize : (i + 1) * keysize]
            
            for j in range(i + 1, blocks_to_compare):
                block_j = data[j * keysize : (j + 1) * keysize]
                
                # 计算距离，并进行标准化: distance / keysize
                distance = hamming_distance(block_i, block_j)
                total_normalized_distance += distance / keysize
                comparison_count += 1
        
        if comparison_count == 0:
            continue
            
        # 平均标准化距离
        average_normalized_distance = total_normalized_distance / comparison_count
        
        if average_normalized_distance < best_score:
            best_score = average_normalized_distance
            best_keysize = keysize
            
    return best_keysize

def repeating_key_xor(data: bytes, key: bytes) -> bytes:
    """使用重复密钥对数据进行 XOR 操作。"""
    keylen = len(key)
    # 使用枚举和取模运算实现重复密钥异或
    return bytes(data_byte ^ key[i % keylen] for i, data_byte in enumerate(data))

# --- 3. 主程序逻辑 ---

def main():
    # 题目提供的 Base64 密文 (合并多行)
    b64_str = (
        "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"
    )
    
    print("--- 正在破解重复密钥 XOR 密文 (Python) ---")
    
    # 1. Base64 解码
    try:
        # Python 的 base64.b64decode() 相当于 C 中的 base64_decode
        ciphertext = base64.b64decode(b64_str)
    except base64.binascii.Error:
        print("错误: Base64 字符串无效。")
        return
        
    cipher_len = len(ciphertext)
    print(f"密文长度: {cipher_len} 字节")
    
    # 2. 猜测密钥长度 (KEYSZIZE)
    keysize = guess_keysize(ciphertext)
    
    if keysize <= 0:
        print("密钥长度猜测失败。")
        return
        
    print(f"猜测的密钥长度: {keysize}")
    
    # 3. 破解每个密钥字节
    key_bytes = []
    
    for k in range(keysize):
        # Python 的切片功能 [k::keysize] 相当于 C 语言中复杂的块提取循环
        block = ciphertext[k::keysize]
        
        # 破解单字节 XOR，得到第 k 个密钥字节
        key_byte = break_single_xor(block)
        key_bytes.append(key_byte[0])
        
    key = bytes(key_bytes)
    
    # 打印破解的密钥 (尝试解码为 ASCII)
    try:
        key_display = key.decode('ascii')
        print(f"破解的密钥 (ASCII): '{key_display}'")
    except UnicodeDecodeError:
        key_display = key.hex()
        print(f"破解的密钥 (Hex): {key_display}")

    # 4. 使用密钥解密
    plaintext = repeating_key_xor(ciphertext, key)
    
    print("\n解密后的明文:")
    print("========================================")
    
    # 尝试将明文解码为 ASCII 字符串进行打印
    try:
        # 使用 errors='replace' 来处理可能的非 ASCII 字符
        print(plaintext.decode('ascii', errors='replace'))
    except UnicodeDecodeError:
        print(f"无法安全解码为 ASCII，原始字节流（前200字节）：\n{plaintext[:200].hex()}...")
    
    print("========================================")
    print("\n解密完成！")


if __name__ == "__main__":
    main()
