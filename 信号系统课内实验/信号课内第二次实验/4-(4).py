import numpy as np
import matplotlib.pyplot as plt

# 定义时间t的范围
t = np.linspace(0, np.pi * 4, 100)

# 设置子图的行数和列数
n_rows = 2
n_cols = 2

# 创建子图的网格
fig, axes = plt.subplots(n_rows, n_cols, figsize=(8, 8))

# 计算每个子图对应的N值
N_values = [50, 100, 200, 300]

# 遍历每个子图
for ax, N in zip(axes.flatten(), N_values):
    f2 = []
    for i in t:
        f1 = []
        for n in range(1, N+1):
            x = 0
            for j in range(1, n):
                x += np.sin(j * i) / j
            f1.append(x)
        f2.append(sum(f1) / N)
    # 在当前子图中绘制函数图像
    ax.plot(t, f2, label=f'N={N}')
    ax.legend()
    ax.set_title(f'N={N}')
    ax.grid(True)

# 设置子图之间的间距
plt.tight_layout()

# 显示图形
plt.show()