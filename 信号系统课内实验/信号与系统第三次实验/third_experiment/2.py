from sympy import symbols, simplify, inverse_fourier_transform, exp, Heaviside

# 定义时间域、频域变量
t = symbols('t', real=True)
omega = symbols('omega', real=True)

f_t_1 = 0.5 * exp(-2 * t) * Heaviside(t)
f_t_2 = 0.5 * exp(-2 * (t-1)) * Heaviside(t-1)

f_change_1 = inverse_fourier_transform(f_t_1, omega, t)
f_change_2 = inverse_fourier_transform(f_t_2, omega, t)

#简化表达式
simple_f_1 = simplify(f_change_1)
simple_f_2 = simplify(f_change_2)

print(f'原始信号：{f_t_1, f_t_2}')
print(f'傅里叶反变换后的信号：{simple_f_1, simple_f_2}')

