import numpy as np
import matplotlib.pyplot as plt

n = 1000
f1 = []
t = np.linspace(0, np.pi*4, 1000)
for i in t:
    x = 0
    for j in range(1, n):
        x += np.sin(j*i) / j
    f1.append(x)
plt.figure(figsize=(7, 7))
plt.plot(t, f1, label='jishu')
plt.legend()
plt.xlabel('t')
plt.ylabel('F')
plt.title('4-(1)')
plt.grid()
plt.show()