clear;clc
syms t omega
f_origin=exp(-2*abs(t));
f_change = fourier(f_origin, t, omega);
disp('时域信号：');
disp(f_origin);
disp('傅里叶变换后频域信号：')
disp(f_change)