from sympy import symbols, simplify, exp, Abs, fourier_transform, pi

# 定义时间域、频域变量
t = symbols('t', real=True)
omega = symbols('omega', real=True)
w = omega / (2 * pi)

f_t = exp(-2 * Abs(t))

f_change = fourier_transform(f_t, t, w)

#简化表达式
simple_f = simplify(f_change)

print(f'原始信号：{f_t}')
print(f'傅里叶变换后的信号：{simple_f}')

