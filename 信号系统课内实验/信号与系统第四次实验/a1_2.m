clear; clc;

% 读取合并后的图像
I_combined = imread('1-2.png');
g_combined = rgb2gray(I_combined);

% 对合并后的图像进行傅里叶变换
s_combined = fftshift(fft2(g_combined));
[M_combined, N_combined] = size(s_combined);
n1_combined = fix(M_combined / 2);
n2_combined = fix(N_combined / 2);

% 初始化低频和高频频谱
s_low_freq = zeros(size(s_combined));
s_high_freq = zeros(size(s_combined));

% 定义低通和高通滤波器的截止频率
d0 = 10; % 与合并时的d0相同
d02 = 10; % 与合并时的d02相同

for i = 1:M_combined
    for j = 1:N_combined
        d = sqrt((i - n1_combined)^2 + (j - n2_combined)^2);
        if d < d0
            s_low_freq(i, j) = s_combined(i, j);
        elseif d >= d02
            s_high_freq(i, j) = s_combined(i, j);
        end
    end
end

% 逆傅里叶变换得到低频和高频图像
s_low_freq = ifftshift(s_low_freq);
low_freq_img = uint8(real(ifft2(s_low_freq)));

s_high_freq = ifftshift(s_high_freq);
high_freq_img = uint8(real(ifft2(s_high_freq)));

% 显示分解出的低频和高频图像
figure(4);
imshow(low_freq_img);
title('Low Frequency Image');

figure(5);
imshow(high_freq_img);
title('High Frequency Image');
