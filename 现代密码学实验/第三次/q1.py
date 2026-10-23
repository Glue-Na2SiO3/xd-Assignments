import math

def calculate():
    p = 1009
    q = 3643
    phi = (p - 1) * (q - 1)
    
    # 计算p对应的未隐藏消息数列表（仅保留与p-1互素的e）
    p_counts = get_unhidden_counts(p)
    min_p = min(p_counts)
    
    # 计算q对应的未隐藏消息数列表（仅保留与q-1互素的e）
    q_counts = get_unhidden_counts(q)
    min_q = min(q_counts)
    
    # 求和所有满足条件的e（1 < e < phi，且对应解数为最小值）
    total = 0
    for e in range(2, phi):
        if math.gcd(e, phi) != 1:
            continue
        if p_counts[e % (p - 1)] == min_p and q_counts[e % (q - 1)] == min_q:
            total += e
    return str(total)

def get_unhidden_counts(prime):
    mod = prime - 1
    counts = []
    for e in range(mod):
        if math.gcd(e, mod) != 1:
            counts.append(float('inf'))  # 非互素的e排除
        else:
            counts.append(count_unhidden(prime, e))
    return counts

def count_unhidden(modulus, exponent):
    count = 0
    for m in range(modulus):
        if pow(m, exponent, modulus) == m:
            count += 1
    return count

if __name__ == "__main__":
    print(calculate())