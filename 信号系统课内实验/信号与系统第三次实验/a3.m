clear;clc;

%定义分式
B = conv([1 1], [1 4]);
A = conv([1 0], conv([1 2], [1 3]));

% 使用 residue 函数进行部分分式展开
[R, P, K] = residue(B, A);

% 打印部分分式展开结果
disp('零点:');
disp(R);
disp('极点:');
disp(P);
disp('直接项:');
disp(K);

% 反变换每个部分分式
syms t
h_t = 0; % 初始化 h(t)
for i = 1:length(R)
    h_t = h_t + R(i) * heaviside(t) * exp(P(i) * t);
end

% 如果有直流项，添加到 h(t)
if ~isempty(K)
    h_t = h_t + K(1) * heaviside(t);
end

% 显示反变换结果
disp('反变换结果:');
disp(h_t);