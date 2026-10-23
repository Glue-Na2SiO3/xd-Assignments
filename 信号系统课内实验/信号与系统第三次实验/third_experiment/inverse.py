def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


def mod_inverse(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('Modular inverse does not exist')
    else:
        return x % m


# 示例使用
a = 5
m = 563
try:
    inverse = mod_inverse(a, m)
    print(f"{a} mod {m} 的逆是: {inverse}")
except Exception as e:
    print(e)
