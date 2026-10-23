https://mysterytwister.org/challenges/level-2/cracking-sha1-hashed-passwords

Background: Password-based authentication means that a user sends a plaintext password to a server, and the server calculates the hash value of the received password and compares it with a stored hash value. Goal of this challenge is to reveal the plaintext password given its SHA1 hash value. There is some information known about the original password.

思路阐述：大概能看到有字母还有shift键，可能会有符号

大小写也不同可以直接暴力枚举