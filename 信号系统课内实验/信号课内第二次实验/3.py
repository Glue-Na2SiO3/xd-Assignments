import numpy as np
import matplotlib.pyplot as plt

# 定义参数
num_samples = 1000
mean = 0
std_dev = 1

# 生成高斯白噪声
white_noise = np.random.randn(num_samples) * std_dev

# 计算自相关函数
autocorr = np.correlate(white_noise, white_noise, mode='full')

# 绘制结果
plt.figure(figsize=(7, 7))
plt.plot(white_noise)
plt.figure(figsize=(7, 7))
plt.plot(autocorr, color='r')
plt.xlabel('T')
plt.ylabel('y')
plt.title('Gaussian White Noise')
plt.grid(True)
plt.show()