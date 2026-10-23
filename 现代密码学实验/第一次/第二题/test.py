def find_possible_keys(sub_array):
    """
    筛选可能的密钥：对给定子数组，找到所有能使解密结果仅包含允许字符的密钥
    sub_array：按密钥长度分组后的子密文数组（整数形式）
    返回：符合条件的密钥列表
    """
    # 定义允许的明文字符集（常见可打印字符）
    # 包含：空格(32)、!、"(33-34)，逗号(44)、减号(45)、句号(46)、冒号(58)、问号(63)、下划线(95)
    # 大写字母(65-90)、小写字母(97-122)
    allowed_chars = (
        [chr(x) for x in range(32, 35)]  # 32(空格),33(!),34(")
        + [chr(44), chr(45), chr(46), chr(58), chr(63), chr(95)]  # 标点符号
        + [chr(x) for x in range(65, 91)]  # 大写字母A-Z
        + [chr(x) for x in range(97, 123)]  # 小写字母a-z
    )
    
    all_possible_keys = range(0x00, 0x100)  # 所有可能的密钥（0-255）
    valid_keys = []
    
    # 筛选密钥：若用该密钥解密子数组后所有字符都在允许集内，则为有效密钥
    for key in all_possible_keys:
        # 检查子数组中每个元素用key解密后的字符是否合法
        if all(chr(byte ^ key) in allowed_chars for byte in sub_array):
            valid_keys.append(key)
    
    return valid_keys


# 密文（十六进制字符串）
ciphertext_hex = (
    "F96DE8C227A259C87EE1DA2AED57C93FE5DA36ED4EC87EF2C63AAE5B9A7EFFD673BE4ACF7BE8923C"
    "AB1ECE7AF2DA3DA44FCF7AE29235A24C963FF0DF3CA3599A70E5DA36BF1ECE77F8DC34BE129A6CF4D126BF"
    "5B9A7CFEDF3EB850D37CF0C63AA2509A76FF9227A55B9A6FE3D720A850D97AB1DD35ED5FCE6BF0D138A84C"
    "C931B1F121B44ECE70F6C032BD56C33FF9D320ED5CDF7AFF9226BE5BDE3FF7DD21ED56CF71F5C036A94D96"
    "3FF8D473A351CE3FE5DA3CB84DDB71F5C17FED51DC3FE8D732BF4D963FF3C727ED4AC87EF5DB27A451D47E"
    "FD9230BF47CA6BFEC12ABE4ADF72E29224A84CDF3FF5D720A459D47AF59232A35A9A7AE7D33FB85FCE7AF5"
    "923AA31EDB3FF7D33ABF52C33FF0D673A551D93FFCD33DA35BC831B1F43CBF1EDF67F0DF23A15B963FE5DA"
    "36ED68D378F4DC36BF5B9A7AFFD121B44ECE76FEDC73BE5DD27AFCD773BA5FC93FE5DA3CB859D26BB1C63C"
    "ED5CDF3FE2D730B84CDF3FF7DD21ED5ADF7CF0D636BE1EDB79E5D721ED57CE3FE6D320ED57D469F4DC27A8"
    "5A963FF3C727ED49DF3FFFDD24ED55D470E69E73AC50DE3FE5DA3ABE1EDF67F4C030A44DDF3FF5D73EA250"
    "C96BE3D327A84D963FE5DA32B91ED36BB1D132A31ED87AB1D021A255DF71B1C436BF479A7AF0C13AA14794"
)

# 将十六进制密文转换为字节数组（每个元素为十六进制对应的整数）
cipher_bytes = [int(ciphertext_hex[i:i+2], 16) for i in range(0, len(ciphertext_hex), 2)]


# 步骤1：尝试不同的密钥长度（1到13），筛选可能的密钥
for key_length in range(1, 14):
    print(f"\n===== 测试密钥长度: {key_length} =====")
    # 按密钥长度分组：第class_number组包含下标为class_number, class_number+key_length, ...的元素
    for class_num in range(key_length):
        sub_array = cipher_bytes[class_num::key_length]  # 提取当前分组的子密文
        possible_keys = find_possible_keys(sub_array)   # 筛选该分组的可能密钥
        
        print(f"分组 {class_num} 的可能密钥: {possible_keys}")
        
        # 若有多个可能的密钥，打印每个密钥对应的解密片段
        if len(possible_keys) > 0:
            for key in possible_keys:
                decrypted_fragment = ''.join([chr(byte ^ key) for byte in sub_array])
                print(f"  密钥 {key} 对应的解密片段: {decrypted_fragment[:50]}...")  # 只显示前50字符


# 步骤2：使用确定的密钥解密完整明文（假设通过上述分析确定密钥）
confirmed_key = [186, 31, 145, 178, 83, 205, 62]  # 确定的密钥
plaintext = ''.join([
    chr(cipher_bytes[i] ^ confirmed_key[i % len(confirmed_key)]) 
    for i in range(len(cipher_bytes))
])

print("\n===== 完整解密结果 =====")
print(plaintext)