###	Convert hex to base64
Input: 49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d

Output:
SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t

**resolution**:直接转换.hex(),再import base64 as b64, 再 b64.encode()即可

###	Fixed XOR
Write a function that takes two equal-length buffers and produces their XOR combination.

If your function works properly, then when you feed it the string:
`1c0111001f010100061a024b53535009181c`
... after hex decoding, and when XOR'd against:
`686974207468652062756c6c277320657965`
... should produce:
`746865206b696420646f6e277420706c6179`

**resolution**:转化成01再去诸位异或，或者字节（8位二进制）直接异或，binascii.unhexlify()

###	Single-byte XOR cipher


###	Detect single-character XOR

###	Implement repeating-key XOR

###	Break repeating-key XOR

