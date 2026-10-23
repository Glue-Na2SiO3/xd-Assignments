clear; clc;
syms s t

% 定义传递函数的分子和分母多项式
num = [1 0];        % s
den = [1 3 2];      % s^2 + 3s + 2

% 创建传递函数
sys = tf(num, den);

% 计算冲激响应的拉普拉斯反变换
H_s = poly2sym(num, s) / poly2sym(den, s);
h_t = ilaplace(H_s, s, t);
disp('Impulse response h(t):');
disp(h_t);

% 计算阶跃响应的拉普拉斯反变换
U_s = 1 / s;  % 拉普拉斯变换后的单位阶跃函数
Y_s = H_s * U_s;  % 传递函数乘以单位阶跃函数的拉普拉斯变换
y_t = ilaplace(Y_s, s, t);
disp('Step response y(t):');
disp(y_t);

% 冲激响应图
figure;
impulse(sys);
title('Impulse Response');
grid on;

% 阶跃响应图
figure;
step(sys);
title('Step Response');
grid on;

% 给定激励下的零状态响应
% 定义激励信号
t = 0:0.01:10;
u = cos(20*t).*heaviside(t);  % 例如一个正弦激励信号

% 计算零状态响应
[y, t_out] = lsim(sys, u, t);

% 绘制零状态响应图
figure;
plot(t_out, y);
title('Zero State Response to sin(t) Input');
xlabel('Time (s)');
ylabel('Response');
grid on;
