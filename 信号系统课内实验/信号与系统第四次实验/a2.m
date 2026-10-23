clear;clc;

% 读取音频文件
[y, fs] = audioread('5.flac');
sound(y, fs); % 播放源文件

% 检查音频信号是否为多声道
if size(y, 2) > 1
    fprintf('多声道');
    y = mean(y, 2); % 如果是立体声，转换为单声道
end

% 获取音频信息
nbits = 16; % 假设位深度为16位
ts = 1 / fs;
t = (1/fs : 1/fs : length(y)/fs);

% 绘制原始信号波形及频谱
figure(1);
subplot(2,1,1);
plot(t, y);
title('原始信号波形');
xlabel('时间 t');
grid on;

subplot(2,1,2);
num = length(y);
plot((-num/2:num/2-1)/num*fs, abs(fftshift(fft(y))));
title('原始信号频谱');
xlabel('频率 (Hz)');
grid on;

% 频率减半 fs/2
fs1 = fs / 2.0;
y1 = resample(y, fs1 , fs);
audiowrite('51.flac', y1, fs1);
t1 = (1/fs1 : 1/fs1 : length(y1)/fs1);

figure(2);
subplot(2,1,1);
plot(t1, y1);
title('fs/2 采样信号波形');
xlabel('时间 t');
grid on;

subplot(2,1,2);
num1 = length(y1);
plot((-num1/2:num1/2-1)/num1*fs1, abs(fftshift(fft(y1))));
title('fs/2 采样信号频谱');
xlabel('频率 (Hz)');
grid on;

% 频率再减半 fs/4
fs2 = fs / 4;
y2 = resample(y, fs, fs2);
audiowrite('52.flac', y2, fs2);
t2 = (1/fs2 : 1/fs2 : length(y2)/fs2);

figure(3);
subplot(2,1,1);
plot(t2, y2);
title('fs/4 采样信号波形');
xlabel('时间 t');
grid on;

subplot(2,1,2);
num2 = length(y2);
plot((-num2/2:num2/2-1)/num2*fs2, abs(fftshift(fft(y2))));
title('fs/4 采样信号频谱');
xlabel('频率 (Hz)');
grid on;

% 频率再减半 fs/8
fs3 = round(fs / 8);
y3 = resample(y, fs, fs3);
audiowrite('53.flac', y3, fs3);
t3 = (1/fs3 : 1/fs3 : length(y3)/fs3);

figure(4);
subplot(2,1,1);
plot(t3, y3);
title('fs/8 采样信号波形');
xlabel('时间 t');
grid on;

subplot(2,1,2);
num3 = length(y3);
plot((-num3/2:num3/2-1)/num3*fs3, abs(fftshift(fft(y3))));
title('fs/8 采样信号频谱');
xlabel('频率 (Hz)');
grid on;

% 频率再减半 fs/16
fs4 = round(fs / 16);
y4 = resample(y, fs, fs4);
audiowrite('54.flac', y4, fs4);
t4 = (1/fs4 : 1/fs4 : length(y4)/fs4);

figure(5);
subplot(2,1,1);
plot(t4, y4);
title('fs/16 采样信号波形');
xlabel('时间 t');
grid on;

subplot(2,1,2);
num4 = length(y4);
plot((-num4/2:num4/2-1)/num4*fs4, abs(fftshift(fft(y4))));
title('fs/16 采样信号频谱');
xlabel('频率 (Hz)');
grid on;
