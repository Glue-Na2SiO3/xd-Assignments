import numpy as np
import matplotlib.pyplot as plt


def step_function(x):
    if x < 0:
        return 0
    else:
        return 1


def g_5_function(x):
    if x > 2.5 or x < -2.5:
        return 0
    else:
        return 1


t = np.linspace(-10, 10, 1000)
f1 = np.array([np.cos(30 * i) * g_5_function(i) for i in t])
f2 = np.array([(step_function(i) - step_function(i - 4)) for i in t])
f2_flipped = np.flipud(f2)
conv_result = np.convolve(f1, f2_flipped, mode='same')

plt.figure(figsize=(10, 10))
plt.plot(t, conv_result, label='conv_result')
plt.legend()
plt.xlabel('t')
plt.ylabel('F')
plt.title('1-(2)')
plt.grid()
plt.show()
