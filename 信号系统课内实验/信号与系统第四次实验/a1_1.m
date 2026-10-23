clear; clc;

% 读取并处理图片（低通滤波）
I1 = imread('1.png'); 
g1 = rgb2gray(I1);
s = fftshift(fft2(g1));
[M, N] = size(s);
n1 = fix(M / 2);
n2 = fix(N / 2);

% 理想低通滤波器取d0=10（可调节）
d0 = 10;
for i = 1:M
    for j = 1:N
        d = sqrt((i - n1)^2 + (j - n2)^2);
        if d < d0
            h = 1;
        else
            h = 0;
        end
        s(i, j) = h * s(i, j);
    end
end
s = ifftshift(s);
s_low = uint8(real(ifft2(s)));
figure(1);
imshow(s_low);
title('Low-pass filtered image (Monroe)');

% 读取并处理图片（高通滤波）
I2 = imread('2.png'); 
g2 = rgb2gray(I2);
s2 = fftshift(fft2(g2));
[M2, N2] = size(s2);
n12 = fix(M2 / 2);
n22 = fix(N2 / 2);

% 理想高通滤波器取d02=10（可调节）
d02 = 10;
for i = 1:M2
    for j = 1:N2
        d = sqrt((i - n12)^2 + (j - n22)^2);
        if d < d02
            h = 0;
        else
            h = 1;
        end
        s2(i, j) = h * s2(i, j);
    end
end
s2 = ifftshift(s2);
s_high = uint8(real(ifft2(s2)));
figure(2);
imshow(s_high);
title('High-pass filtered image (Einstein)');

% 确保两幅图像大小一致（如果不同则裁剪或填充）
[height1, width1] = size(s_low);
[height2, width2] = size(s_high);

if height1 ~= height2 || width1 ~= width2
    minHeight = min(height1, height2);
    minWidth = min(width1, width2);
    s_low = imresize(s_low, [minHeight, minWidth]);
    s_high = imresize(s_high, [minHeight, minWidth]);
end

% 图片合并
s_combined = imadd(s_low, s_high);
figure(3);
imshow(s_combined);
title('Combined Image');
imwrite(s_combined, 'combined.jpg', 'JPG');
