import gmpy2
#中国剩余定理
def read_base_from_txt(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
        items = [int(x.strip()) for x in content.replace('\n', ',').split(',') if x.strip()]
        return items

def chinese_remainder_verbose(data):
    # 判断是否互质
    for i in range(len(data)):
        for j in range(i+1, len(data)):
            if gmpy2.gcd(data[i][1], data[j][1]) != 1:
                print("not coprime")
                return

    mods = [m for _, m in data]
    N = 1
    for m in mods:
        N *= m
    Ni = [N // m for m in mods]
    Ni_inv = [gmpy2.invert(Ni[i], mods[i]) for i in range(len(mods))]
    xj = [data[i][0] * Ni[i] * Ni_inv[i] for i in range(len(data))]
    x0 = sum(xj) % N

    print("m:", mods)
    print("Mj:", Ni)
    print("Mj^-1:", Ni_inv)
    print("xj:", xj)
    print("x0:", x0)
    print(f"结果: x ≡ {x0} (mod {N})")

def prepare_data(base):
    n = len(base) // 2
    return [(base[i], base[n + i]) for i in range(n)]

if __name__ == '__main__':
    for idx in range(1, 5):
        print(f"base{idx}:")
        base = read_base_from_txt(f"{idx}.txt")
        data = prepare_data(base)
        chinese_remainder_verbose(data)
