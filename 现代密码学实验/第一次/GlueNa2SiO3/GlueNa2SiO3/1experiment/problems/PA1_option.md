Write a program that allows you to "crack" ciphertexts generated using a Vigenere-like cipher, where byte-wise XOR is used instead of addition modulo 26.

# Vigenère-like Cipher
一种多表代换密码，其思想源于经典的维吉尼亚密码。

核心思想：它使用一个关键词来加密信息，而不是像凯撒密码那样只用一个固定的偏移量。关键词中的每个字母决定了明文中对应字母的偏移量。

工作方式：
将明文和关键词对齐。如果关键词比明文短，就重复关键词。
明文中的每个字母，根据其对应的关键词字母进行移位。
例如，如果关键词是 KEY，明文是 HELLO：
H 用 K 来加密
E 用 E 来加密
L 用 Y 来加密
L 用 K (关键词重复) 来加密
O 用 E (关键词重复) 来加密
