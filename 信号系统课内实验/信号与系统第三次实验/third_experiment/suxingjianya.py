def is_prime(num):
    # 如果输入的数小于2，则不是素数
    if num < 2:
        return False
    # 检查从2到num的平方根的所有数是否能整除num
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True


# 示例使用
number = 563
if is_prime(number):
    print(f"{number} 是素数。")
else:
    print(f"{number} 不是素数。")
