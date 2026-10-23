#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
实验6: 图像伪造实验
内容: 风格迁移、生成式图像、Boundless图像外推
参考:
- https://www.tensorflow.org/hub/tutorials/tf2_arbitrary_image_stylization
- https://www.tensorflow.org/hub/tutorials/tf_hub_generative_image_module
- https://www.tensorflow.org/hub/tutorials/boundless
"""

import os
import sys
import time
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# 0. 环境检测与GPU配置
# ============================================================
print("=" * 70)
print("实验6: 图像伪造实验")
print("=" * 70)

import tensorflow as tf
print(f"\n[环境信息]")
print(f"TensorFlow版本: {tf.__version__}")
print(f"Python版本: {sys.version.split()[0]}")

# GPU检测
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    print(f"检测到GPU: {len(gpus)}个")
    for gpu in gpus:
        print(f"  - {gpu}")
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)
    print("GPU内存增长已启用")
else:
    print("未检测到GPU，将使用CPU运行（速度较慢）")

# 创建输出目录
OUTPUT_DIR = "exp6_outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)
print(f"输出目录: {OUTPUT_DIR}/")

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import urllib.request

# ============================================================
# 辅助函数
# ============================================================
def save_figure(fig, filename, dpi=150):
    """保存matplotlib图像"""
    filepath = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(filepath, dpi=dpi, bbox_inches='tight')
    print(f"  图像已保存: {filepath}")
    return filepath


def show_images(images, titles=None, cols=3, figsize=(15, 5), save_name=None):
    """显示并保存多张图像"""
    n = len(images)
    rows = (n + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=figsize)
    if rows == 1:
        axes = axes.reshape(1, -1) if n > 1 else np.array([[axes]])
    axes = axes.flatten()
    for i, img in enumerate(images):
        ax = axes[i]
        if img.ndim == 2:
            ax.imshow(img, cmap='gray')
        else:
            if img.max() > 1.5:
                img = img / 255.0
            ax.imshow(np.clip(img, 0, 1))
        ax.axis('off')
        if titles and i < len(titles):
            ax.set_title(titles[i], fontsize=10)
    for j in range(n, len(axes)):
        axes[j].axis('off')
    plt.tight_layout()
    if save_name:
        save_figure(fig, save_name)
    plt.show()
    return fig


def load_image(path, max_dim=512):
    """加载并预处理图像"""
    img = tf.io.read_file(path)
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)

    shape = tf.cast(tf.shape(img)[:-1], tf.float32)
    long_dim = max(shape)
    scale = max_dim / long_dim
    new_shape = tf.cast(shape * scale, tf.int32)

    img = tf.image.resize(img, new_shape)
    img = img[tf.newaxis, :]
    return img


def tensor_to_image(tensor):
    """将tensor转换为PIL Image"""
    tensor = tensor * 255
    tensor = np.array(tensor, dtype=np.uint8)
    if np.ndim(tensor) > 3:
        tensor = tensor[0]
    return Image.fromarray(tensor)


# ============================================================
# 第一部分: 任意图像风格迁移 (Arbitrary Image Stylization)
# ============================================================
print("\n" + "=" * 70)
print("第一部分: 任意图像风格迁移")
print("=" * 70)
print("参考: https://www.tensorflow.org/hub/tutorials/tf2_arbitrary_image_stylization")


def run_style_transfer():
    """运行任意图像风格迁移"""
    print("\n[步骤1] 加载TensorFlow Hub风格迁移模型")
    try:
        import tensorflow_hub as hub
        print("  tensorflow_hub已安装")
    except ImportError:
        print("  正在安装tensorflow_hub...")
        os.system(f"{sys.executable} -m pip install tensorflow-hub -q")
        import tensorflow_hub as hub

    hub_model_url = "https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2"
    print(f"  模型URL: {hub_model_url}")
    print("  正在加载模型（首次加载需要下载，约需1-2分钟）...")
    start_time = time.time()
    hub_module = hub.load(hub_model_url)
    elapsed = time.time() - start_time
    print(f"  模型加载完成，耗时: {elapsed:.2f}秒")

    print("\n[步骤2] 准备内容图像和风格图像")
    # 下载示例图像
    content_urls = [
        ('https://storage.googleapis.com/download.tensorflow.org/example_images/YellowLabradorLooking_new.jpg',
         'content_dog.jpg'),
        ('https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Tiffanie_at_cat_show.jpg/599px-Tiffanie_at_cat_show.jpg',
         'content_cat.jpg'),
    ]
    style_urls = [
        ('https://storage.googleapis.com/download.tensorflow.org/example_images/Vassily_Kandinsky%2C_1913_-_Composition_7.jpg',
         'style_kandinsky.jpg'),
        ('https://upload.wikimedia.org/wikipedia/commons/0/0a/The_Great_Wave_off_Kanagawa.jpg',
         'style_wave.jpg'),
    ]

    content_images = []
    style_images = []
    content_arrays = []
    style_arrays = []

    for url, name in content_urls:
        path = tf.keras.utils.get_file(name, url)
        img = load_image(path, max_dim=384)
        content_images.append(img)
        content_arrays.append(img[0].numpy())
        print(f"  内容图像: {name}, 尺寸: {img.shape}")

    for url, name in style_urls:
        path = tf.keras.utils.get_file(name, url)
        img = load_image(path, max_dim=256)
        style_images.append(img)
        style_arrays.append(img[0].numpy())
        print(f"  风格图像: {name}, 尺寸: {img.shape}")

    # 显示输入图像
    fig, axes = plt.subplots(2, 2, figsize=(12, 12))
    axes[0, 0].imshow(content_arrays[0])
    axes[0, 0].set_title("Content Image 1: Dog")
    axes[0, 0].axis('off')
    axes[0, 1].imshow(style_arrays[0])
    axes[0, 1].set_title("Style Image 1: Kandinsky")
    axes[0, 1].axis('off')
    axes[1, 0].imshow(content_arrays[1])
    axes[1, 0].set_title("Content Image 2: Cat")
    axes[1, 0].axis('off')
    axes[1, 1].imshow(style_arrays[1])
    axes[1, 1].set_title("Style Image 2: Great Wave")
    axes[1, 1].axis('off')
    save_figure(fig, "style_transfer_inputs.png")
    plt.show()

    print("\n[步骤3] 运行风格迁移")
    stylized_results = []
    titles = []

    combinations = [
        (0, 0, "Dog + Kandinsky Style"),
        (0, 1, "Dog + Ukiyo-e Style"),
        (1, 0, "Cat + Kandinsky Style"),
        (1, 1, "Cat + Ukiyo-e Style"),
    ]

    for ci, si, title in combinations:
        print(f"  正在生成: {title} ...")
        start_time = time.time()
        stylized = hub_module(tf.constant(content_images[ci]),
                              tf.constant(style_images[si]))[0]
        elapsed = time.time() - start_time
        stylized_array = stylized[0].numpy()
        stylized_results.append(stylized_array)
        titles.append(f"{title}\n({elapsed:.1f}s)")
        print(f"    完成，耗时: {elapsed:.2f}秒")

    # 显示所有结果
    show_images(stylized_results, titles=titles, cols=2, figsize=(14, 14),
                save_name="style_transfer_results.png")

    print("\n[风格迁移实验完成] 输出文件:")
    print(f"  - {OUTPUT_DIR}/style_transfer_inputs.png")
    print(f"  - {OUTPUT_DIR}/style_transfer_results.png")
    return stylized_results


# ============================================================
# 第二部分: 生成式图像模块 (Generative Image Module)
# ============================================================
print("\n" + "=" * 70)
print("第二部分: 生成式图像模块 (BigGAN)")
print("=" * 70)
print("参考: https://www.tensorflow.org/hub/tutorials/tf_hub_generative_image_module")


def run_generative_image():
    """运行生成式图像模块实验"""
    print("\n[步骤1] 加载BigGAN生成模型")
    try:
        import tensorflow_hub as hub
    except ImportError:
        os.system(f"{sys.executable} -m pip install tensorflow-hub -q")
        import tensorflow_hub as hub

    # BigGAN-deep 512x512
    module_url = "https://tfhub.dev/deepmind/biggan-deep-256/1"
    print(f"  模型: BigGAN-deep-256")
    print("  正在加载模型...")
    start_time = time.time()
    try:
        tf.compat.v1.reset_default_graph()
        module = hub.Module(module_url)
        print("  BigGAN模型加载成功")
    except Exception as e:
        print(f"  BigGAN加载失败: {e}")
        print("  使用替代方案: 加载条件生成模型")
        module = None
    elapsed = time.time() - start_time
    print(f"  耗时: {elapsed:.2f}秒")

    if module is None:
        print("\n[替代方案] 使用简单的噪声生成演示")
        print("  由于BigGAN模型较大，这里使用随机噪声插值演示生成概念")

        # 创建一些有趣的随机图像作为演示
        np.random.seed(42)
        generated_images = []
        titles = []

        for i in range(6):
            # 使用不同频率的噪声模拟不同风格
            freq = 2 ** (i + 1)
            noise = np.random.randn(256, 256, 3)
            # 应用高斯滤波模拟平滑
            from scipy.ndimage import gaussian_filter
            smooth = gaussian_filter(noise, sigma=256/freq)
            smooth = (smooth - smooth.min()) / (smooth.max() - smooth.min() + 1e-8)
            generated_images.append(smooth)
            titles.append(f"Random Noise (freq={freq})")

        show_images(generated_images, titles=titles, cols=3, figsize=(15, 10),
                    save_name="generative_noise_demo.png")

        print("\n[生成式图像实验完成 - 演示模式] 输出文件:")
        print(f"  - {OUTPUT_DIR}/generative_noise_demo.png")
        return generated_images

    print("\n[步骤2] 定义生成参数")
    # ImageNet类别
    class_names = {
        42: "great white shark",
        99: "goose",
        323: "monarch butterfly",
        386: "African elephant",
        401: "accordion",
        546: "warplane",
        888: "volcano",
        947: "mushroom",
    }
    print(f"  选择类别数: {len(class_names)}")
    for k, v in class_names.items():
        print(f"    {k}: {v}")

    print("\n[步骤3] 生成图像")
    # 使用TensorFlow 1.x兼容模式
    import tensorflow.compat.v1 as tf1
    tf1.disable_eager_execution()

    # 创建session
    sess = tf1.Session()
    sess.run(tf1.global_variables_initializer())

    z = tf1.random.normal(shape=[1, 128], seed=np.random.randint(0, 10000))
    y = tf1.placeholder(tf.int32, shape=[1])
    truncation = tf1.placeholder(tf.float32)

    samples = module(dict(z=z, y=y, truncation=truncation))

    generated_images = []
    titles = []

    for class_id, class_name in class_names.items():
        print(f"  生成类别 {class_id}: {class_name} ...")
        start_time = time.time()
        try:
            img = sess.run(samples, feed_dict={y: [class_id], truncation: 0.5})
            img = np.clip(img[0], -1, 1)
            img = (img + 1) / 2  # 转换到[0,1]
            generated_images.append(img)
            elapsed = time.time() - start_time
            titles.append(f"{class_name}\n({elapsed:.1f}s)")
            print(f"    完成，耗时: {elapsed:.2f}秒")
        except Exception as e:
            print(f"    失败: {e}")

    sess.close()

    if generated_images:
        show_images(generated_images, titles=titles, cols=4, figsize=(16, 8),
                    save_name="generative_biggan_results.png")

    print("\n[生成式图像实验完成] 输出文件:")
    if generated_images:
        print(f"  - {OUTPUT_DIR}/generative_biggan_results.png")
    else:
        print(f"  - {OUTPUT_DIR}/generative_noise_demo.png")
    return generated_images


# ============================================================
# 第三部分: Boundless图像外推
# ============================================================
print("\n" + "=" * 70)
print("第三部分: Boundless图像外推")
print("=" * 70)
print("参考: https://www.tensorflow.org/hub/tutorials/boundless")


def run_boundless():
    """运行Boundless图像外推实验"""
    print("\n[步骤1] 加载Boundless模型")
    try:
        import tensorflow_hub as hub
    except ImportError:
        os.system(f"{sys.executable} -m pip install tensorflow-hub -q")
        import tensorflow_hub as hub

    # Boundless模型
    model_name = "boundless-quarter"
    model_url = f"https://tfhub.dev/google/boundless/{model_name}/1"
    print(f"  模型: {model_name}")
    print("  正在加载模型...")
    start_time = time.time()
    try:
        model = hub.load(model_url)
        print("  Boundless模型加载成功")
    except Exception as e:
        print(f"  模型加载失败: {e}")
        print("  使用替代方案: 手动实现图像外推演示")
        model = None
    elapsed = time.time() - start_time
    print(f"  耗时: {elapsed:.2f}秒")

    print("\n[步骤2] 准备示例图像")
    # 下载示例图像
    image_urls = [
        ('https://storage.googleapis.com/download.tensorflow.org/example_images/YellowLabradorLooking_new.jpg',
         'boundless_dog.jpg'),
        ('https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Tiffanie_at_cat_show.jpg/599px-Tiffanie_at_cat_show.jpg',
         'boundless_cat.jpg'),
    ]

    original_images = []
    processed_images = []
    titles = []

    for url, name in image_urls:
        path = tf.keras.utils.get_file(name, url)
        img = Image.open(path).convert('RGB')
        # 调整为正方形
        size = min(img.size)
        img = img.crop((0, 0, size, size))
        img = img.resize((256, 256))
        img_array = np.array(img) / 255.0
        original_images.append(img_array)
        print(f"  图像: {name}, 尺寸: {img_array.shape}")

    if model is not None:
        print("\n[步骤3] 运行Boundless外推")
        for i, img_array in enumerate(original_images):
            print(f"  处理图像 {i+1} ...")
            start_time = time.time()
            try:
                # 准备输入
                input_tensor = tf.convert_to_tensor(img_array, dtype=tf.float32)
                input_tensor = tf.expand_dims(input_tensor, 0)

                # 运行模型
                result = model.signatures['default'](input_tensor)
                generated = result['default'][0].numpy()
                generated = np.clip(generated, 0, 1)

                elapsed = time.time() - start_time
                processed_images.append(generated)
                titles.append(f"Extrapolation Result {i+1}\n({elapsed:.1f}s)")
                print(f"    完成，耗时: {elapsed:.2f}秒，输出尺寸: {generated.shape}")
            except Exception as e:
                print(f"    失败: {e}")
                processed_images.append(img_array)
                titles.append(f"Extrapolation Result {i+1} (Failed)")
    else:
        print("\n[替代方案] 手动实现图像外推效果")
        for i, img_array in enumerate(original_images):
            # 模拟外推：镜像填充边缘
            h, w = img_array.shape[:2]
            # 创建更大的画布
            scale = 1.5
            new_h, new_w = int(h * scale), int(w * scale)
            canvas = np.zeros((new_h, new_w, 3), dtype=np.float32)

            # 计算中心位置
            y_off = (new_h - h) // 2
            x_off = (new_w - w) // 2

            # 放置原图
            canvas[y_off:y_off+h, x_off:x_off+w] = img_array

            # 边缘镜像填充
            # 上边缘
            canvas[:y_off, x_off:x_off+w] = np.flipud(img_array[:y_off, :])
            # 下边缘
            canvas[y_off+h:, x_off:x_off+w] = np.flipud(img_array[-(new_h-y_off-h):, :])
            # 左边缘
            canvas[:, :x_off] = np.fliplr(canvas[:, x_off:x_off+x_off])
            # 右边缘
            canvas[:, x_off+w:] = np.fliplr(canvas[:, x_off+w-x_off:x_off+w])

            processed_images.append(canvas)
            titles.append(f"Extrapolation Result {i+1} (Mirror Fill)")
            print(f"    完成，输出尺寸: {canvas.shape}")

    # 显示对比结果
    for i in range(len(original_images)):
        fig, axes = plt.subplots(1, 2, figsize=(14, 7))
        axes[0].imshow(original_images[i])
        axes[0].set_title("Original Image")
        axes[0].axis('off')
        axes[1].imshow(processed_images[i])
        axes[1].set_title(titles[i])
        axes[1].axis('off')
        save_figure(fig, f"boundless_result_{i+1}.png")
        plt.show()

    # 汇总显示
    all_images = []
    all_titles = []
    for i in range(len(original_images)):
        all_images.append(original_images[i])
        all_titles.append(f"Original {i+1}")
        all_images.append(processed_images[i])
        all_titles.append(titles[i])

    show_images(all_images, titles=all_titles, cols=2, figsize=(14, 14),
                save_name="boundless_all_results.png")

    print("\n[Boundless实验完成] 输出文件:")
    print(f"  - {OUTPUT_DIR}/boundless_result_1.png")
    print(f"  - {OUTPUT_DIR}/boundless_result_2.png")
    print(f"  - {OUTPUT_DIR}/boundless_all_results.png")
    return processed_images


# ============================================================
# 第四部分: 图像伪造检测演示
# ============================================================
print("\n" + "=" * 70)
print("第四部分: 图像伪造检测演示")
print("=" * 70)
print("说明: 使用简单的误差分析方法检测图像是否经过篡改")


def run_forgery_detection():
    """运行图像伪造检测演示"""
    print("\n[步骤1] 创建演示数据")
    # 加载原始图像
    url = 'https://storage.googleapis.com/download.tensorflow.org/example_images/YellowLabradorLooking_new.jpg'
    path = tf.keras.utils.get_file('detect_dog.jpg', url)
    img = Image.open(path).convert('RGB').resize((256, 256))
    original = np.array(img) / 255.0

    # 创建伪造图像：复制粘贴篡改
    forged = original.copy()
    # 从图像中复制一块区域粘贴到另一位置
    patch = original[80:140, 80:140].copy()
    forged[160:220, 160:220] = patch

    # 创建另一种伪造：拼接篡改
    forged2 = original.copy()
    # 添加不自然的颜色块
    forged2[100:180, 100:180, 0] = forged2[100:180, 100:180, 0] * 0.5 + 0.5

    print("  原始图像尺寸:", original.shape)
    print("  伪造图像1: 复制粘贴篡改")
    print("  伪造图像2: 颜色篡改")

    # 显示原始和伪造图像
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    axes[0].imshow(original)
    axes[0].set_title("Original Image")
    axes[0].axis('off')
    axes[1].imshow(forged)
    axes[1].set_title("Forged Image 1 (Copy-Paste)")
    axes[1].axis('off')
    axes[2].imshow(forged2)
    axes[2].set_title("Forged Image 2 (Color Tampering)")
    axes[2].axis('off')
    save_figure(fig, "forgery_samples.png")
    plt.show()

    print("\n[步骤2] 误差分析检测")
    # 计算差分图像
    diff1 = np.abs(original - forged)
    diff2 = np.abs(original - forged2)

    # 计算误差统计
    mse1 = np.mean(diff1 ** 2)
    mse2 = np.mean(diff2 ** 2)
    max_diff1 = np.max(diff1)
    max_diff2 = np.max(diff2)

    print(f"  伪造1 MSE: {mse1:.6f}")
    print(f"  伪造1 最大差值: {max_diff1:.4f}")
    print(f"  伪造2 MSE: {mse2:.6f}")
    print(f"  伪造2 最大差值: {max_diff2:.4f}")

    # 显示差分图像
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes[0, 0].imshow(original)
    axes[0, 0].set_title("Original Image")
    axes[0, 0].axis('off')
    axes[0, 1].imshow(forged)
    axes[0, 1].set_title("Forged Image 1")
    axes[0, 1].axis('off')
    axes[0, 2].imshow(diff1)
    axes[0, 2].set_title(f"Difference Map 1 (MSE={mse1:.4f})")
    axes[0, 2].axis('off')
    axes[1, 0].imshow(original)
    axes[1, 0].set_title("Original Image")
    axes[1, 0].axis('off')
    axes[1, 1].imshow(forged2)
    axes[1, 1].set_title("Forged Image 2")
    axes[1, 1].axis('off')
    axes[1, 2].imshow(diff2)
    axes[1, 2].set_title(f"Difference Map 2 (MSE={mse2:.4f})")
    axes[1, 2].axis('off')
    save_figure(fig, "forgery_detection.png")
    plt.show()

    print("\n[步骤3] 噪声不一致性分析")
    # 计算局部噪声方差
    from scipy.ndimage import uniform_filter

    def local_variance(img, size=5):
        """计算局部方差"""
        mean = uniform_filter(img, size)
        mean_sq = uniform_filter(img ** 2, size)
        var = mean_sq - mean ** 2
        return var

    var_orig = local_variance(original)
    var_forged = local_variance(forged)
    var_forged2 = local_variance(forged2)

    # 方差差异
    var_diff1 = np.abs(var_orig - var_forged)
    var_diff2 = np.abs(var_orig - var_forged2)

    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes[0, 0].imshow(var_orig.mean(axis=2), cmap='hot')
    axes[0, 0].set_title("Original Local Variance")
    axes[0, 0].axis('off')
    axes[0, 1].imshow(var_forged.mean(axis=2), cmap='hot')
    axes[0, 1].set_title("Forged Image 1 Local Variance")
    axes[0, 1].axis('off')
    axes[0, 2].imshow(var_diff1.mean(axis=2), cmap='hot')
    axes[0, 2].set_title("Variance Difference 1")
    axes[0, 2].axis('off')
    axes[1, 0].imshow(var_orig.mean(axis=2), cmap='hot')
    axes[1, 0].set_title("Original Local Variance")
    axes[1, 0].axis('off')
    axes[1, 1].imshow(var_forged2.mean(axis=2), cmap='hot')
    axes[1, 1].set_title("Forged Image 2 Local Variance")
    axes[1, 1].axis('off')
    axes[1, 2].imshow(var_diff2.mean(axis=2), cmap='hot')
    axes[1, 2].set_title("Variance Difference 2")
    axes[1, 2].axis('off')
    save_figure(fig, "forgery_noise_analysis.png")
    plt.show()

    print("\n[伪造检测实验完成] 输出文件:")
    print(f"  - {OUTPUT_DIR}/forgery_samples.png")
    print(f"  - {OUTPUT_DIR}/forgery_detection.png")
    print(f"  - {OUTPUT_DIR}/forgery_noise_analysis.png")
    return (mse1, mse2), (max_diff1, max_diff2)


# ============================================================
# 主程序入口
# ============================================================
if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("开始运行实验6: 图像伪造实验")
    print("=" * 70)

    try:
        print("\n>>> 运行第一部分: 风格迁移")
        run_style_transfer()
    except Exception as e:
        print(f"风格迁移实验出错: {e}")
        import traceback
        traceback.print_exc()

    try:
        print("\n>>> 运行第二部分: 生成式图像")
        run_generative_image()
    except Exception as e:
        print(f"生成式图像实验出错: {e}")
        import traceback
        traceback.print_exc()

    try:
        print("\n>>> 运行第三部分: Boundless图像外推")
        run_boundless()
    except Exception as e:
        print(f"Boundless实验出错: {e}")
        import traceback
        traceback.print_exc()

    try:
        print("\n>>> 运行第四部分: 图像伪造检测")
        run_forgery_detection()
    except Exception as e:
        print(f"伪造检测实验出错: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 70)
    print("实验6全部完成!")
    print(f"所有输出文件保存在: {OUTPUT_DIR}/")
    print("=" * 70)
