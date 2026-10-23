import random

# 求最大公因数
def greatest_common_divisor(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Fermat素性检测函数
def fermat_primality_test(n):
    # 生成[2, n-2]之间的随机数
    rand_num = int(random.randrange(2, n-1))
    print(f"[!]生成的随机数为：{rand_num}")
    # 判断是否互素
    if greatest_common_divisor(rand_num, n) != 1:
        return False
    # 验证费马小定理
    if pow(rand_num, n-1, n) != 1:
        return False
    return True

# 读取测试文件并执行检测的函数
def test_from_file(file_path, k):
    try:
        with open(file_path, 'r') as f:
            n = int(f.read().strip())
            print(f"\n===== 测试文件 {file_path} =====")
            run_test(n, k)
    except Exception as e:
        print(f"读取文件 {file_path} 失败：{e} (路径：{file_path})")

# 执行检测的核心函数
def run_test(n, k):
    possible = (1 - 1 / (2 ** k)) * 100
    remaining = k
    while remaining > 0:
        if fermat_primality_test(n):
            remaining -= 1
        else:
            break
    if remaining == 0:
        print(f"[!]最终结果n={n} 可能是素数，为素数的概率为 {possible:.2f}%")
    else:
        print(f"[!]最终结果:n={n} 为合数")

if "__main__" == __name__:
    choice = input("请选择执行方式（1-手动输入，2-读取测试文件）：")
    if choice == '2':
        k = int(input("请输入检测次数k："))
        test_files = ["1.txt", "4.txt"]
        for file in test_files:
            test_from_file(file, k)
    else:
        n = int(input("请输入待检测的数n："))
        k = int(input("请输入检测次数k："))
        run_test(n, k)