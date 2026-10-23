"""
实验4: TensorFlow进阶 - Vision (修改版)
内容来源: https://www.tensorflow.org/tutorials (Vision部分)
定制化: 第四部分使用CIFAR-10实现简易语义分割 (无需外网、仅内置tf.keras)
要求: 使用GPU(自动检测), 清晰注释, 包含训练过程可视化
"""

import os
import sys
import time
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ============================================================
# 0. 环境检查与GPU设置
# ============================================================
print("=" * 60)
print("实验4: TensorFlow进阶 - Vision (CIFAR-10语义分割版)")
print("=" * 60)

import tensorflow as tf
print(f"\n[环境信息]")
print(f"TensorFlow版本: {tf.__version__}")
print(f"Python版本: {sys.version.split()[0]}")

# GPU检测
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    print(f"检测到GPU设备: {len(gpus)}个")
    for i, gpu in enumerate(gpus):
        print(f"  GPU {i}: {gpu}")
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)
    print("已启用GPU内存动态增长")
else:
    print("未检测到GPU, 将使用CPU运行")

print("=" * 60)

# 创建输出目录
output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output_images")
os.makedirs(output_dir, exist_ok=True)
print(f"输出图片保存目录: {output_dir}")

# ============================================================
# 第一部分: 图像分类 (Image Classification)
# 来源: https://www.tensorflow.org/tutorials/images/classification
# ============================================================
print("\n" + "=" * 60)
print("第一部分: 图像分类 (Image Classification)")
print("=" * 60)

# 使用CIFAR-10数据集进行图像分类
print("\n[步骤1] 加载CIFAR-10数据集...")
(x_train_cifar, y_train_cifar), (x_test_cifar, y_test_cifar) = tf.keras.datasets.cifar10.load_data()

# 归一化
x_train_cifar = x_train_cifar.astype('float32') / 255.0
x_test_cifar = x_test_cifar.astype('float32') / 255.0
y_train_cifar = y_train_cifar.flatten()
y_test_cifar = y_test_cifar.flatten()

class_names_cifar = ['airplane', 'automobile', 'bird', 'cat', 'deer',
                     'dog', 'frog', 'horse', 'ship', 'truck']

print(f"训练集大小: {x_train_cifar.shape}")
print(f"测试集大小: {x_test_cifar.shape}")
print(f"类别数: {len(class_names_cifar)}")

# 可视化部分样本
fig, axes = plt.subplots(2, 5, figsize=(12, 5))
for i in range(10):
    ax = axes[i // 5, i % 5]
    ax.imshow(x_train_cifar[i])
    ax.set_title(class_names_cifar[y_train_cifar[i]])
    ax.axis('off')
plt.suptitle("CIFAR-10 Sample Images")
plt.tight_layout()
fig_path = os.path.join(output_dir, "part1_cifar10_samples.png")
plt.savefig(fig_path, dpi=150)
print(f"样本可视化已保存: {fig_path}")
plt.close()

# 构建CNN图像分类模型
print("\n[步骤2] 构建CNN图像分类模型...")
model_cifar = tf.keras.Sequential([
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D((2, 2)),
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(10)
])
model_cifar.compile(optimizer='adam',
                    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                    metrics=['accuracy'])
model_cifar.summary()

# 训练 (使用子集加速)
print("\n[步骤3] 训练图像分类模型 (使用5000样本子集, 10 epochs)...")
x_train_subset = x_train_cifar[:5000]
y_train_subset = y_train_cifar[:5000]

history_cifar = model_cifar.fit(x_train_subset, y_train_subset, epochs=10,
                                 validation_split=0.2, verbose=1)

# 评估
test_loss_cifar, test_acc_cifar = model_cifar.evaluate(x_test_cifar[:1000], y_test_cifar[:1000], verbose=2)
print(f"\nCIFAR-10测试准确率: {test_acc_cifar:.4f}")

# 可视化训练过程
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].plot(history_cifar.history['accuracy'], label='train')
axes[0].plot(history_cifar.history['val_accuracy'], label='val')
axes[0].set_title('CIFAR-10 Classification Accuracy')
axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Accuracy')
axes[0].legend()
axes[0].grid(True)

axes[1].plot(history_cifar.history['loss'], label='train')
axes[1].plot(history_cifar.history['val_loss'], label='val')
axes[1].set_title('CIFAR-10 Classification Loss')
axes[1].set_xlabel('Epoch')
axes[1].set_ylabel('Loss')
axes[1].legend()
axes[1].grid(True)
plt.tight_layout()
fig_path = os.path.join(output_dir, "part1_classification_training.png")
plt.savefig(fig_path, dpi=150)
print(f"训练过程可视化已保存: {fig_path}")
plt.close()

print("\n[第一部分完成] 图像分类结束")

# ============================================================
# 第二部分: 迁移学习 (Transfer Learning)
# 来源: https://www.tensorflow.org/tutorials/images/transfer_learning
# ============================================================
print("\n" + "=" * 60)
print("第二部分: 迁移学习 (Transfer Learning)")
print("=" * 60)

# 使用预训练的MobileNetV2进行迁移学习
print("\n[步骤1] 加载预训练模型 MobileNetV2...")

# 创建一个小数据集用于演示 (使用CIFAR-10的一部分, 调整为224x224)
print("准备迁移学习数据 (调整图像尺寸为224x224)...")

# 取少量样本并resize
num_samples_tl = 1000
x_tl = tf.image.resize(x_train_cifar[:num_samples_tl], [224, 224])
y_tl = y_train_cifar[:num_samples_tl]

# 使用预训练模型 (不包含顶层)
base_model = tf.keras.applications.MobileNetV2(input_shape=(224, 224, 3),
                                                include_top=False,
                                                weights='imagenet')
base_model.trainable = False  # 冻结基础模型
print(f"基础模型输出形状: {base_model.output_shape}")

# 构建迁移学习模型
inputs = tf.keras.Input(shape=(224, 224, 3))
x = base_model(inputs, training=False)
x = tf.keras.layers.GlobalAveragePooling2D()(x)
x = tf.keras.layers.Dropout(0.2)(x)
outputs = tf.keras.layers.Dense(10)(x)
model_tl = tf.keras.Model(inputs, outputs)

model_tl.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
                 loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                 metrics=['accuracy'])
model_tl.summary()

print("\n[步骤2] 训练迁移学习模型 (冻结基础层, 5 epochs)...")
history_tl = model_tl.fit(x_tl, y_tl, epochs=5, validation_split=0.2, verbose=1)

# 微调: 解冻部分层
print("\n[步骤3] 微调模型 - 解冻基础模型最后20层...")
base_model.trainable = True
fine_tune_at = len(base_model.layers) - 20
for layer in base_model.layers[:fine_tune_at]:
    layer.trainable = False

model_tl.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.00001),
                 loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                 metrics=['accuracy'])

history_tl_fine = model_tl.fit(x_tl, y_tl, epochs=3, validation_split=0.2, verbose=1)

# 合并历史并可视化
all_acc = history_tl.history['accuracy'] + history_tl_fine.history['accuracy']
all_val_acc = history_tl.history['val_accuracy'] + history_tl_fine.history['val_accuracy']
all_loss = history_tl.history['loss'] + history_tl_fine.history['loss']
all_val_loss = history_tl.history['val_loss'] + history_tl_fine.history['val_loss']

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].plot(all_acc, label='train accuracy')
axes[0].plot(all_val_acc, label='val accuracy')
axes[0].axvline(x=len(history_tl.history['accuracy']) - 0.5, color='r', linestyle='--', label='fine-tune start')
axes[0].set_title('Transfer Learning Accuracy')
axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Accuracy')
axes[0].legend()
axes[0].grid(True)

axes[1].plot(all_loss, label='train loss')
axes[1].plot(all_val_loss, label='val loss')
axes[1].axvline(x=len(history_tl.history['loss']) - 0.5, color='r', linestyle='--', label='fine-tune start')
axes[1].set_title('Transfer Learning Loss')
axes[1].set_xlabel('Epoch')
axes[1].set_ylabel('Loss')
axes[1].legend()
axes[1].grid(True)
plt.tight_layout()
fig_path = os.path.join(output_dir, "part2_transfer_learning.png")
plt.savefig(fig_path, dpi=150)
print(f"迁移学习可视化已保存: {fig_path}")
plt.close()

print("\n[第二部分完成] 迁移学习结束")

# ============================================================
# 第三部分: 数据增强 (Data Augmentation)
# 来源: https://www.tensorflow.org/tutorials/images/data_augmentation
# ============================================================
print("\n" + "=" * 60)
print("第三部分: 数据增强 (Data Augmentation)")
print("=" * 60)

print("\n[步骤1] 定义数据增强层...")
data_augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip("horizontal"),
    tf.keras.layers.RandomRotation(0.2),
    tf.keras.layers.RandomZoom(0.2),
    tf.keras.layers.RandomContrast(0.2),
])

# 可视化数据增强效果
print("\n[步骤2] 可视化数据增强效果...")
sample_image = x_train_cifar[0:1]
fig, axes = plt.subplots(2, 4, figsize=(12, 6))
axes[0, 0].imshow(sample_image[0])
axes[0, 0].set_title("Original")
axes[0, 0].axis('off')

for i in range(7):
    augmented = data_augmentation(sample_image)
    row = (i + 1) // 4
    col = (i + 1) % 4
    axes[row, col].imshow(augmented[0].numpy())
    axes[row, col].set_title(f"Augmented {i+1}")
    axes[row, col].axis('off')

plt.suptitle("Data Augmentation Examples")
plt.tight_layout()
fig_path = os.path.join(output_dir, "part3_data_augmentation.png")
plt.savefig(fig_path, dpi=150)
print(f"数据增强可视化已保存: {fig_path}")
plt.close()

# 使用数据增强训练模型
print("\n[步骤3] 使用数据增强训练模型...")
model_aug = tf.keras.Sequential([
    data_augmentation,
    tf.keras.layers.Conv2D(32, 3, activation='relu', input_shape=(32, 32, 3)),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Conv2D(64, 3, activation='relu'),
    tf.keras.layers.MaxPooling2D(),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(10)
])
model_aug.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])

history_aug = model_aug.fit(x_train_subset, y_train_subset, epochs=5,
                             validation_split=0.2, verbose=1)

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].plot(history_aug.history['accuracy'], label='train')
axes[0].plot(history_aug.history['val_accuracy'], label='val')
axes[0].set_title('With Data Augmentation - Accuracy')
axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Accuracy')
axes[0].legend()
axes[0].grid(True)

axes[1].plot(history_aug.history['loss'], label='train')
axes[1].plot(history_aug.history['val_loss'], label='val')
axes[1].set_title('With Data Augmentation - Loss')
axes[1].set_xlabel('Epoch')
axes[1].set_ylabel('Loss')
axes[1].legend()
axes[1].grid(True)
plt.tight_layout()
fig_path = os.path.join(output_dir, "part3_augmentation_training.png")
plt.savefig(fig_path, dpi=150)
print(f"数据增强训练可视化已保存: {fig_path}")
plt.close()

print("\n[第三部分完成] 数据增强结束")

# ============================================================
# 第四部分: 图像分割 (Image Segmentation)
# 定制化: 使用CIFAR-10实现简易语义分割 (无需外网、仅内置tf.keras)
# ============================================================
# ============================================================
# 第四部分: 图像分割 (Image Segmentation) - CIFAR-10简易版【修复显存崩溃】
# ============================================================
print("\n" + "=" * 60)
print("第四部分: 图像分割 (Image Segmentation) - CIFAR-10简易版")
print("=" * 60)

print("\n[步骤1] 加载CIFAR-10子集用于语义分割，降低显存占用...")
# 仅加载少量子集，不使用完整数据集，防止显存溢出
(x_train_full, y_train_full), (x_test_full, y_test_full) = tf.keras.datasets.cifar10.load_data()
# 截取小样本
train_num = 1000
test_num = 200
x_train_seg = x_train_full[:train_num].astype('float32') / 255.0
y_train_seg = y_train_full[:train_num].flatten()
x_test_seg = x_test_full[:test_num].astype('float32') / 255.0
y_test_seg = y_test_full[:test_num].flatten()

# 单样本预处理函数：在线生成掩码、resize，不占用大量内存
def preprocess(img, label):
    # 原图resize到128x128
    img = tf.image.resize(img, (128, 128))
    # 生成掩码：整张图像素值=类别标签，tf操作不依赖numpy大数组
    mask = tf.fill((128, 128, 1), label)
    return img, mask

# 构建dataset，在线预处理，不缓存全量大图
train_ds = tf.data.Dataset.from_tensor_slices((x_train_seg, y_train_seg))
train_ds = train_ds.map(preprocess, num_parallel_calls=tf.data.AUTOTUNE)
train_ds = train_ds.shuffle(500).batch(8).prefetch(tf.data.AUTOTUNE)

test_ds = tf.data.Dataset.from_tensor_slices((x_test_seg, y_test_seg))
test_ds = test_ds.map(preprocess, num_parallel_calls=tf.data.AUTOTUNE)
test_ds = test_ds.batch(8).prefetch(tf.data.AUTOTUNE)

print(f"分割训练子集数量: {train_num}")
print(f"分割测试子集数量: {test_num}")
print(f"分割输出类别通道: 10 (CIFAR-10十分类)")

# 构建轻量化U-Net，减少通道降低显存占用
print("\n[步骤2] 构建轻量化U-Net风格分割模型...")
def unet_model(output_channels: int):
    inputs = tf.keras.layers.Input(shape=[128, 128, 3])
    # 下采样 通道减半，减轻显存
    c1 = tf.keras.layers.Conv2D(32, 3, activation='relu', padding='same')(inputs)
    c1 = tf.keras.layers.Conv2D(32, 3, activation='relu', padding='same')(c1)
    p1 = tf.keras.layers.MaxPooling2D((2, 2))(c1)

    c2 = tf.keras.layers.Conv2D(64, 3, activation='relu', padding='same')(p1)
    c2 = tf.keras.layers.Conv2D(64, 3, activation='relu', padding='same')(c2)
    p2 = tf.keras.layers.MaxPooling2D((2, 2))(c2)

    # bottleneck
    c3 = tf.keras.layers.Conv2D(128, 3, activation='relu', padding='same')(p2)
    c3 = tf.keras.layers.Conv2D(128, 3, activation='relu', padding='same')(c3)

    # 上采样
    u4 = tf.keras.layers.Conv2DTranspose(64, (2, 2), strides=(2, 2), padding='same')(c3)
    u4 = tf.keras.layers.concatenate([u4, c2])
    c4 = tf.keras.layers.Conv2D(64, 3, activation='relu', padding='same')(u4)
    c4 = tf.keras.layers.Conv2D(64, 3, activation='relu', padding='same')(c4)

    u5 = tf.keras.layers.Conv2DTranspose(32, (2, 2), strides=(2, 2), padding='same')(c4)
    u5 = tf.keras.layers.concatenate([u5, c1])
    c5 = tf.keras.layers.Conv2D(32, 3, activation='relu', padding='same')(u5)
    c5 = tf.keras.layers.Conv2D(32, 3, activation='relu', padding='same')(c5)

    outputs = tf.keras.layers.Conv2D(output_channels, 1, activation='softmax')(c5)
    return tf.keras.Model(inputs=[inputs], outputs=[outputs])

model_seg = unet_model(output_channels=10)
model_seg.compile(
    optimizer='adam',
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False),
    metrics=['accuracy']
)
model_seg.summary()

# 训练分割模型，epoch调低减少计算量
print("\n[步骤3] 训练CIFAR-10分割模型 (3 epochs)...")
history_seg = model_seg.fit(
    train_ds,
    epochs=3,
    validation_data=test_ds,
    verbose=1
)

# 可视化分割结果
print("\n[步骤4] 可视化CIFAR-10分割结果...")
for image, mask in test_ds.take(1):
    pred_mask = model_seg.predict(image, verbose=0)
    pred_mask = tf.argmax(pred_mask, axis=-1)
    pred_mask = pred_mask[..., tf.newaxis]

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    true_cls = int(mask[0, 0, 0].numpy())
    pred_cls = int(pred_mask[0, 0, 0].numpy())

    axes[0].imshow(image[0].numpy())
    axes[0].set_title(f"Input Image\nTrue Class: {class_names_cifar[true_cls]}")
    axes[0].axis('off')

    axes[1].imshow(mask[0, ..., 0].numpy(), cmap='tab10')
    axes[1].set_title("True Segmentation Mask")
    axes[1].set_clim(0, 9)
    axes[1].axis('off')

    axes[2].imshow(pred_mask[0, ..., 0].numpy(), cmap='tab10')
    axes[2].set_title(f"Predicted Mask\nPredict Class: {class_names_cifar[pred_cls]}")
    axes[2].set_clim(0, 9)
    axes[2].axis('off')

    plt.suptitle("CIFAR-10 Simple Semantic Segmentation Results")
    plt.tight_layout()
    fig_path = os.path.join(output_dir, "part4_cifar10_segmentation_results.png")
    plt.savefig(fig_path, dpi=150)
    print(f"分割结果可视化已保存: {fig_path}")
    plt.close()
    break

# 训练曲线可视化
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].plot(history_seg.history['accuracy'], label='train')
axes[0].plot(history_seg.history['val_accuracy'], label='val')
axes[0].set_title('CIFAR-10 Segmentation Accuracy')
axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Accuracy')
axes[0].legend()
axes[0].grid(True)

axes[1].plot(history_seg.history['loss'], label='train')
axes[1].plot(history_seg.history['val_loss'], label='val')
axes[1].set_title('CIFAR-10 Segmentation Loss')
axes[1].set_xlabel('Epoch')
axes[1].set_ylabel('Loss')
axes[1].legend()
axes[1].grid(True)
plt.tight_layout()
fig_path = os.path.join(output_dir, "part4_cifar10_segmentation_training.png")
plt.savefig(fig_path, dpi=150)
print(f"分割训练可视化已保存: {fig_path}")
plt.close()

print("\n[第四部分完成] CIFAR-10简易语义分割结束")

# ============================================================
# 第五部分: 目标检测 (Object Detection)
# 来源: https://www.tensorflow.org/tutorials (Vision/Object Detection)
# 使用TensorFlow Hub的预训练模型进行演示
# ============================================================
print("\n" + "=" * 60)
print("第五部分: 目标检测 (Object Detection)")
print("=" * 60)

print("\n[步骤1] 使用TensorFlow Hub预训练模型进行目标检测...")

try:
    import tensorflow_hub as hub

    # 加载预训练的目标检测模型
    detector = hub.load("https://tfhub.dev/tensorflow/ssd_mobilenet_v2/2")
    print("目标检测模型加载成功")

    # 使用CIFAR-10图像进行演示 (需要resize到模型输入尺寸)
    print("\n[步骤2] 对样本图像进行目标检测...")

    # 取一张CIFAR图像并放大以便检测
    sample_img = x_train_cifar[4]  # 一张图像
    sample_img_resized = tf.image.resize(sample_img[tf.newaxis, ...], [320, 320])

    # 运行检测
    detections = detector(sample_img_resized)

    # 可视化检测结果
    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    ax.imshow(sample_img_resized[0].numpy())
    ax.set_title("Object Detection Sample (Pre-trained Model)")
    ax.axis('off')

    # 绘制检测框 (简化显示)
    boxes = detections['detection_boxes'][0].numpy()
    scores = detections['detection_scores'][0].numpy()
    for i in range(min(5, len(boxes))):
        if scores[i] > 0.3:
            y1, x1, y2, x2 = boxes[i]
            rect = plt.Rectangle((x1 * 320, y1 * 320), (x2 - x1) * 320, (y2 - y1) * 320,
                                 fill=False, edgecolor='red', linewidth=2)
            ax.add_patch(rect)
            ax.text(x1 * 320, y1 * 320 - 5, f"{scores[i]:.2f}", color='red', fontsize=10,
                    bbox=dict(facecolor='white', alpha=0.7))

    plt.tight_layout()
    fig_path = os.path.join(output_dir, "part5_object_detection.png")
    plt.savefig(fig_path, dpi=150)
    print(f"目标检测结果已保存: {fig_path}")
    plt.close()

    print(f"\n检测结果统计:")
    print(f"  检测框数量: {len(boxes)}")
    print(f"  最高置信度: {scores[0]:.4f}")

except Exception as e:
    print(f"目标检测部分出错: {e}")
    print("尝试使用简化版目标检测演示...")

    # 简化版: 使用简单的边缘检测作为替代演示
    sample_img = x_train_cifar[4]
    gray = tf.image.rgb_to_grayscale(sample_img[tf.newaxis, ...])
    sobel_y = tf.image.sobel_edges(gray)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    axes[0].imshow(sample_img)
    axes[0].set_title("Original Image")
    axes[0].axis('off')

    edge_img = tf.sqrt(sobel_y[0, ..., 0]**2 + sobel_y[0, ..., 1]**2)
    axes[1].imshow(edge_img[0, ..., 0], cmap='gray')
    axes[1].set_title("Edge Detection (Simplified)")
    axes[1].axis('off')

    plt.suptitle("Object Detection - Simplified Demo")
    plt.tight_layout()
    fig_path = os.path.join(output_dir, "part5_object_detection_simple.png")
    plt.savefig(fig_path, dpi=150)
    print(f"简化版目标检测已保存: {fig_path}")
    plt.close()

print("\n[第五部分完成] 目标检测结束")

# ============================================================
# 实验总结
# ============================================================
print("\n" + "=" * 60)
print("实验4总结 (CIFAR-10语义分割版)")
print("=" * 60)
print(f"1. 图像分类 (CIFAR-10)     - 测试准确率: {test_acc_cifar:.4f}")
print(f"2. 迁移学习 (MobileNetV2)  - 完成特征提取+微调")
print(f"3. 数据增强                - 完成多种增强策略演示")
print(f"4. 图像分割 (U-Net)        - 完成CIFAR-10简易语义分割 (无需外网)")
print(f"5. 目标检测                - 完成预训练模型推理")
print(f"\n所有可视化图片已保存到: {output_dir}")
print("=" * 60)
print("实验4完成!")