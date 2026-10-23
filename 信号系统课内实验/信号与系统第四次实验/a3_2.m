clear;clc;
% 读取带水印的图像
watermarked_image = imread('watermarked_image.jpg');

% 显示原始图像
figure;
subplot(1, 2, 1);
imshow(watermarked_image);
title('原始加水印的图像');

% 对带水印的图像进行傅里叶变换
fft_watermarked_image = fft2(double(watermarked_image));

% 创建已知的水印编码（这里假设水印是一个矩阵）
watermark = randi([0, 1], size(watermarked_image));
encoded_watermark = watermark * 255;

% 将水印从频域图像中去除
watermarked_fft_image_removed = fft_watermarked_image - encoded_watermark;

% 对修改后的频域图像进行傅里叶反变换
watermarked_image_removed = ifft2(watermarked_fft_image_removed);

% 取实部，得到图像
watermarked_image_removed = uint8(real(watermarked_image_removed));

% 显示去除水印后的图像
subplot(1, 2, 2);
imshow(watermarked_image_removed);
title('去除数字盲水印后的图像');

% 保存去除水印后的图像
imwrite(watermarked_image_removed, 'watermarked_image_removed.jpg');
