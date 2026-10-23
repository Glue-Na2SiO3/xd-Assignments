clear; clc;
syms t omega real

% 定义时域信号
f_origin_1 = 0.5 * exp(-2 * t) * heaviside(t);
f_origin_2 = 0.5 * exp(-2 * (t - 1)) * heaviside(t - 1);

% 计算傅里叶变换
f_change_1 = fourier(f_origin_1, t, omega);
f_change_2 = fourier(f_origin_2, t, omega);

% 转换符号表达式为数值函数
f_change_1_num = matlabFunction(f_change_1, 'Vars', omega);
f_change_2_num = matlabFunction(f_change_2, 'Vars', omega);

% 定义频率范围
omega_values = linspace(-10, 10, 100000); % 定义一个频率范围，例如从0到2

% 提取幅度和相位的数值函数
magnitude_1_num = abs(f_change_1_num(omega_values));
phase_1_num = angle(f_change_1_num(omega_values));
magnitude_2_num = abs(f_change_2_num(omega_values));
phase_2_num = angle(f_change_2_num(omega_values));

% 绘制幅度谱
figure;
subplot(2, 2, 1);
plot(omega_values, magnitude_1_num);
title('幅值 f_origin_1');
xlabel('Frequency (omega)');
ylabel('幅值');

% 绘制相位谱
subplot(2, 2, 2);
plot(omega_values, phase_1_num);
title('相位 f_origin_1');
xlabel('Frequency (omega)');
ylabel('相位');

% 绘制第二个信号的幅度谱
subplot(2, 2, 3);
plot(omega_values, magnitude_2_num);
title('幅值 f_origin_2');
xlabel('Frequency (omega)');
ylabel('幅值');

% 绘制第二个信号的相位谱
subplot(2, 2, 4);
plot(omega_values, phase_2_num);
title('相位 f_origin_2');
xlabel('Frequency (omega)');
ylabel('相位');
