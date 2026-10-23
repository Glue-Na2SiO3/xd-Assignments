clear;clc;

%定义分式
B = [1 0 1];
A = [3 5 4 6];

% 使用 roots 函数求解分子和分母的零点和极点
zeros = roots(B); % 分子的零点
poles = roots(A); % 分母的极点

% 创建传递函数
sys = tf(B, A);

% 绘制零极点图
figure;
pzmap(sys);
title('Pole-Zero Map of the System H(s)');
xlabel('Real Part');
ylabel('Imaginary Part');
grid on;

% 打印零点和极点
disp('Zeros of the system:');
disp(zeros);
disp('Poles of the system:');
disp(poles);

% 检查极点的位置以判断系统稳定性
if all(real(poles) < 0)
    disp('系统是稳定的，因为所有极点都位于左半平面。');
else
    disp('系统是不稳定的，因为存在极点不在左半平面。');
end