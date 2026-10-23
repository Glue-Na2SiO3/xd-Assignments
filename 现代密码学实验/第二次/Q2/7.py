#PKCS#7 padding validation
import random
from random import randint
import os
from Crypto.Cipher import AES
from math import ceil
from binascii import unhexlify, b2a_base64, a2b_base64, hexlify
import chardet

#Validate the padding
def PKCS_7_padding_validation(padded_message):
    return pkcs7_unpad(padded_message)

def pkcs7_unpad(padded_message):
    # 接受 bytes 或可编码为 bytes 的 str
    if isinstance(padded_message, str):
        padded_message = padded_message.encode()
    if not isinstance(padded_message, (bytes, bytearray)):
        raise TypeError("padded_message must be bytes or bytearray")
    if len(padded_message) == 0:
        raise ValueError('Padding is Invalid')

    last_byte = padded_message[-1]
    # last_byte 为 0 或 大于消息长度 都视为非法填充
    if last_byte == 0 or last_byte > len(padded_message):
        raise ValueError('Padding is Invalid')

    # 检查最后 last_byte 个字节是否都等于 last_byte
    if padded_message[-last_byte:] != bytes([last_byte]) * last_byte:
        raise ValueError('Padding is Invalid')

    return padded_message[:-last_byte]

if __name__== "__main__":
    test_byte_string=b'ICE ICE BABY\x04\x04\x04\x04'
    try:
        print(pkcs7_unpad(test_byte_string))
    except ValueError:
        print('Padding is Invalid')

    test_byte_string=b'ICE ICE BABY\x05\x05\x05\x05'
    try:
        print(pkcs7_unpad(test_byte_string))
    except ValueError:
        print('Padding is Invalid')

    test_byte_string=b'ICE ICE BABY\x01\x02\x03\x04'
    try:
        print(pkcs7_unpad(test_byte_string))
    except ValueError:
        print('Padding is Invalid')