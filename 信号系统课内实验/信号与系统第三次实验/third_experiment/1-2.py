from sympy import symbols, simplify, inverse_fourier_transform, pi

# 定义时间域、频域变量
t = symbols('t', real=True)
omega = symbols('omega', real=True)
w = omega / (2 * pi)

f_w = 1 / (1 + w**2)

f_change = inverse_fourier_transform(f_w, omega, t)

#简化表达式
simple_f = simplify(f_change)

print(f'原始信号：{f_w}')
print(f'傅里叶反变换后的信号：{simple_f}')

