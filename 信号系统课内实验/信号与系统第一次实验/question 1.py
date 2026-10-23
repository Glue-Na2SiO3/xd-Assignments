import numpy as np
import matplotlib.pyplot as plt

# question 1
t_value = np.linspace(-10, 10, 1000)


def fun_1(t):
    return np.where(t > 0, 1, 0)


y = []
for i in t_value:
    print(i)
    y.append(fun_1(2 * i))
plt.plot(t_value, y)
plt.xlabel('t')
plt.ylabel('F1')
plt.title('F1')
plt.grid()
plt.show()

# question 2
t = np.linspace(0, 10, 1000)
y = 4 * np.exp(-2 * t) * np.cos(np.pi * t)
plt.plot(t, y)
plt.xlabel('t')
plt.ylabel('F2')
plt.title('F2')
plt.grid()
plt.show()


# question 3

def fun_3(t):
    return np.where((t > -1) & (t < 1), 1, 0)


def fun_4(t):
    return np.where((t > -3) & (t < 3), 1, 0)


t = np.linspace(-10, 10, 1000)
f1 = fun_3(t)
f2 = fun_4(t)
y = f1 + f2
plt.plot(t, y)
plt.xlabel('t')
plt.ylabel('F3')
plt.title('F3')
plt.grid()
plt.show()

#question 4
t =range(-10,10)
def fun_5(t):
    return np.where(t > -3, 1, 0)
def fun_6(t):
    return np.where(t > 2, 1, 0)
y = []
for i in t:
    y.append(fun_5(i)-fun_6(i))
# 绘制散点图
plt.scatter(t, y)
# 添加垂直线
for i in range(len(t)):
    plt.vlines(t[i], 0, y[i], colors='gray', linestyles='dotted')
plt.xlabel('t')
plt.ylabel('F4')
plt.title('F4')
plt.grid()
plt.show()

#question 5
t = range(-10, 10)
y = []
for i in t:
    y.append(5.0*(0.4)**i*np.cos(1.2*np.pi*i))
# 绘制散点图
plt.scatter(t, y)
# 添加垂直线
for i in range(len(t)):
    plt.vlines(t[i], 0, y[i], colors='gray', linestyles='dotted')
plt.xlabel('t')
plt.ylabel('F5')
plt.title('F5')
plt.grid()
plt.show()

#question 6
t = np.linspace(-10, 10, 1000)
y = 2* np.sin(t/2)/t
plt.plot(t, y)
plt.xlabel('t')
plt.ylabel('F6')
plt.title('F6')
plt.grid()
plt.show()

#question 7
def fun_3(t):
    return np.where((t > -1) & (t < 1), 1, 0)


def fun_4(t):
    return np.where((t > -3) & (t < 3), 1, 0)
f3 = fun_3(0.5*t)
f4 = fun_4(0.5*t)
y1 = f3+f4
plt.plot(t, y1)
plt.xlabel('t')
plt.ylabel('y')
plt.title('2-(1)')
plt.grid()
plt.show()


def fun_3(t):
    return np.where((t > -1) & (t < 1), 1, 0)


def fun_4(t):
    return np.where((t > -3) & (t < 3), 1, 0)
f5 = fun_3(2-2*t)
f6 = fun_4(2-2*t)
y2 = f5+f6
plt.plot(t, y2)
plt.xlabel('t')
plt.ylabel('y')
plt.title('2-(2)')
plt.grid()
plt.show()

# 计算离散数据点的导数
dt = t[0] - t[1]  # 计算 x 的间距
dy = np.diff(y2) / dt  # 使用中心差分法计算 y 的导数

dy = np.append(dy, [dy[-1]])  # 补充末尾导数值，使长度与原始数据相同

plt.plot(t, dy)
plt.xlabel('t')
plt.ylabel('dy')
plt.title('2-(3)')
plt.grid()
plt.show()

t = np.linspace(0, np.pi*4, 1001)
y = []
for i in t:
    x = 0
    for j in range(1, 201):
        x += np.sin((2*j-1)*i) / (2*j-1)
    y.append(x)
plt.plot(t, y)
plt.xlabel('t')
plt.ylabel('y')
plt.title('3')
plt.grid()
plt.show()
