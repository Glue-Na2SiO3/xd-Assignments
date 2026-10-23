clear;clc
syms t omega
f_origin=1/(1+omega^2);
f_change = ifourier(f_origin, omega, t);
disp('频域信号：');
disp(f_origin);
disp('傅里叶反变换后时域信号：')
disp(f_change)