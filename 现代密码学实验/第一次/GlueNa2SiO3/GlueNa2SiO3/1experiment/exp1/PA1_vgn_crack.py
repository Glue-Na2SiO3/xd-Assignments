"""
假设给一个循环加密的关键词是"KEY"，明文是"plaintext"。模拟一下加密和解密，并展示结果。
"""
def vgn_encode(plaintext: bytes, key: bytes) -> bytes:
    """使用循环密钥对明文进行加密"""
    encrypted = bytearray()
    key_length = len(key)
    
    for i in range(len(plaintext)):
        encrypted_byte = plaintext[i] ^ key[i % key_length]
        encrypted.append(encrypted_byte)
    
    return bytes(encrypted)


def vgn_decode(ciphertext: bytes, key: bytes) -> bytes:
    """使用循环密钥对密文进行解密"""
    decrypted = bytearray()
    key_length = len(key)
    
    for i in range(len(ciphertext)):
        decrypted_byte = ciphertext[i] ^ key[i % key_length]
        decrypted.append(decrypted_byte)
    
    return bytes(decrypted)

if __name__ == "__main__":
    key = b"KEY"
    plaintext = b"plaintext"
    
    ciphertext = vgn_encode(plaintext, key)
    print(f"Ciphertext (hex): {ciphertext.hex()}")
    
    decrypted_text = vgn_decode(ciphertext, key)
    print(f"Decrypted Text: {decrypted_text.decode()}")
    
    assert decrypted_text == plaintext 