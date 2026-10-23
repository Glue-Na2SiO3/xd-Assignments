clear;clc;
% 读取原始图像
original_image = imread(['1.png']);

% 将原始图像转换为灰度图像
gray_image = rgb2gray(original_image);

% 显示原始图像
figure;
subplot(1, 2, 1);
imshow(gray_image);
title('原始灰度图像');

% 对灰度图像进行傅里叶变换
fft_image = fft2(double(gray_image));

% 创建数字水印（这里假设水印是一个矩阵，大小与图像相同）
watermark = randi([0, 1], size(gray_image));

% 编码水印（这里假设编码过程是简单的直接加法）
encoded_watermark = watermark * 255;

% 将水印添加到频域图像中
watermarked_fft_image = fft_image + encoded_watermark;

% 对添加水印后的频域图像进行傅里叶反变换
watermarked_image = ifft2(watermarked_fft_image);

% 取水印图像的实部（因为傅里叶反变换得到的是复数，取实部可以得到图像）
watermarked_image = uint8(real(watermarked_image));

% 显示添加水印后的图像
subplot(1, 2, 2);
imshow(watermarked_image);
title('添加数字盲水印后的图像');

% 保存添加水印后的图像
imwrite(watermarked_image, 'watermarked_image.jpg');
