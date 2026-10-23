import numpy as np
from scipy.signal import lti, lsim
import matplotlib.pyplot as plt


def step_function(x):
    if x < 0:
        return 0
    else:
        return 1


sys = lti([2, 1], [1, 4, 3])  # 方程里的系数 由高次幂到低次幂

t = np.linspace(0, 10, 1000)
f1 = np.array([4 * np.sin(2 * np.pi * i) * step_function(i) for i in t])
# 模拟系统对输入信号的响应
t, response, _ = lsim(sys, f1, t)

plt.plot(t, response, label='output')
plt.legend()
plt.title('2-(3)')
plt.grid()
plt.show()
