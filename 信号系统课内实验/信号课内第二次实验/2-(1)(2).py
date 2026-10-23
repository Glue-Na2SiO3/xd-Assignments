from scipy.signal import lti, step, impulse
import matplotlib.pyplot as plt

sys = lti([2, 1], [1, 4, 3])  # 方程里的系数 由高次幂到低次幂
st, sy = step(sys)
it, iy = impulse(sys)
plt.plot(st, sy, label='step')
plt.plot(it, iy, label='impluse')
plt.legend()
plt.title('2-(1)(2)')
plt.grid()
plt.show()
