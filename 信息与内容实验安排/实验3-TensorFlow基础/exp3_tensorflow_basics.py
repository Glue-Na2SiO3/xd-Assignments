"""
实验3: TensorFlow基础
内容来源: https://www.tensorflow.org/tutorials
包含: Quickstart for beginners, Quickstart for experts, ML basics with Keras
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
print("实验3: TensorFlow基础")
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
    # 启用内存增长
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
# 第一部分: Quickstart for Beginners
# ============================================================
print("\n" + "=" * 60)
print("第一部分: Quickstart for Beginners")
print("=" * 60)

# 1.1 加载MNIST数据集
print("\n[步骤1] 加载MNIST数据集...")
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0
print(f"训练集大小: {x_train.shape}, 标签: {y_train.shape}")
print(f"测试集大小: {x_test.shape}, 标签: {y_test.shape}")

# 1.2 构建Sequential模型
print("\n[步骤2] 构建Sequential模型...")
model_beginner = tf.keras.models.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(10)
])
model_beginner.summary()

# 1.3 编译模型
print("\n[步骤3] 编译模型...")
loss_fn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
model_beginner.compile(optimizer='adam',
                       loss=loss_fn,
                       metrics=['accuracy'])

# 1.4 训练模型
print("\n[步骤4] 训练模型 (5 epochs)...")
history_beginner = model_beginner.fit(x_train, y_train, epochs=5,
                                       validation_split=0.1,
                                       verbose=1)

# 1.5 评估模型
print("\n[步骤5] 评估模型...")
test_loss, test_acc = model_beginner.evaluate(x_test, y_test, verbose=2)
print(f"\n测试集损失: {test_loss:.4f}")
print(f"测试集准确率: {test_acc:.4f}")

# 1.6 预测示例
print("\n[步骤6] 预测前5个测试样本...")
probability_model = tf.keras.Sequential([
    model_beginner,
    tf.keras.layers.Softmax()
])
predictions = probability_model(x_test[:5])
print(f"预测结果 (前5个):\n{np.argmax(predictions, axis=1)}")
print(f"真实标签 (前5个): {y_test[:5]}")

# 1.7 可视化训练过程
print("\n[步骤7] 保存训练过程可视化图片...")
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].plot(history_beginner.history['accuracy'], label='train accuracy')
axes[0].plot(history_beginner.history['val_accuracy'], label='val accuracy')
axes[0].set_title('Beginner Model Accuracy')
axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Accuracy')
axes[0].legend()
axes[0].grid(True)

axes[1].plot(history_beginner.history['loss'], label='train loss')
axes[1].plot(history_beginner.history['val_loss'], label='val loss')
axes[1].set_title('Beginner Model Loss')
axes[1].set_xlabel('Epoch')
axes[1].set_ylabel('Loss')
axes[1].legend()
axes[1].grid(True)

plt.tight_layout()
fig_path = os.path.join(output_dir, "part1_beginner_training.png")
plt.savefig(fig_path, dpi=150)
print(f"图片已保存: {fig_path}")
plt.close()

# 1.8 可视化预测结果
print("\n[步骤8] 保存预测结果可视化图片...")
fig, axes = plt.subplots(2, 5, figsize=(12, 5))
for i in range(10):
    ax = axes[i // 5, i % 5]
    ax.imshow(x_test[i], cmap='gray')
    pred_label = np.argmax(probability_model(x_test[i:i+1]))
    true_label = y_test[i]
    color = 'green' if pred_label == true_label else 'red'
    ax.set_title(f"Pred: {pred_label}\nTrue: {true_label}", color=color)
    ax.axis('off')
plt.suptitle("Beginner Model Predictions (First 10 Samples)")
plt.tight_layout()
fig_path = os.path.join(output_dir, "part1_beginner_predictions.png")
plt.savefig(fig_path, dpi=150)
print(f"图片已保存: {fig_path}")
plt.close()

print("\n[第一部分完成] Quickstart for Beginners 结束")

# ============================================================
# 第二部分: Quickstart for Experts
# ============================================================
print("\n" + "=" * 60)
print("第二部分: Quickstart for Experts")
print("=" * 60)

# 2.1 加载MNIST数据集并转换为tf.data.Dataset
print("\n[步骤1] 使用tf.data加载和预处理数据...")
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train = x_train.reshape(-1, 28, 28, 1).astype('float32') / 255.0
x_test = x_test.reshape(-1, 28, 28, 1).astype('float32') / 255.0
y_train = y_train.astype('int64')
y_test = y_test.astype('int64')

# 使用tf.data进行数据管道优化
train_ds = tf.data.Dataset.from_tensor_slices((x_train, y_train))
train_ds = train_ds.shuffle(10000).batch(32).prefetch(tf.data.AUTOTUNE)
test_ds = tf.data.Dataset.from_tensor_slices((x_test, y_test)).batch(32).prefetch(tf.data.AUTOTUNE)
print("数据管道构建完成 (shuffle + batch + prefetch)")

# 2.2 使用Keras Functional API构建模型
print("\n[步骤2] 使用Functional API构建CNN模型...")
inputs = tf.keras.Input(shape=(28, 28, 1), name="input_layer")
x = tf.keras.layers.Conv2D(32, 3, activation='relu', name="conv1")(inputs)
x = tf.keras.layers.MaxPooling2D(name="pool1")(x)
x = tf.keras.layers.Conv2D(64, 3, activation='relu', name="conv2")(x)
x = tf.keras.layers.MaxPooling2D(name="pool2")(x)
x = tf.keras.layers.Flatten(name="flatten")(x)
x = tf.keras.layers.Dense(128, activation='relu', name="dense1")(x)
x = tf.keras.layers.Dropout(0.5, name="dropout")(x)
outputs = tf.keras.layers.Dense(10, name="output")(x)

model_expert = tf.keras.Model(inputs=inputs, outputs=outputs, name="expert_mnist_cnn")
model_expert.summary()

# 2.3 自定义训练循环 (Experts风格)
print("\n[步骤3] 使用自定义训练循环训练模型...")

# 损失函数和优化器
loss_object = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
optimizer = tf.keras.optimizers.Adam()

train_loss = tf.keras.metrics.Mean(name='train_loss')
train_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(name='train_accuracy')
test_loss = tf.keras.metrics.Mean(name='test_loss')
test_accuracy = tf.keras.metrics.SparseCategoricalAccuracy(name='test_accuracy')

@tf.function
def train_step(images, labels):
    with tf.GradientTape() as tape:
        predictions = model_expert(images, training=True)
        loss = loss_object(labels, predictions)
    gradients = tape.gradient(loss, model_expert.trainable_variables)
    optimizer.apply_gradients(zip(gradients, model_expert.trainable_variables))
    train_loss(loss)
    train_accuracy(labels, predictions)

@tf.function
def test_step(images, labels):
    predictions = model_expert(images, training=False)
    t_loss = loss_object(labels, predictions)
    test_loss(t_loss)
    test_accuracy(labels, predictions)

EPOCHS = 5
history_expert = {'loss': [], 'accuracy': [], 'val_loss': [], 'val_accuracy': []}

for epoch in range(EPOCHS):
    train_loss.reset_states()
    train_accuracy.reset_states()
    test_loss.reset_states()
    test_accuracy.reset_states()

    start_time = time.time()
    for images, labels in train_ds:
        train_step(images, labels)

    for test_images, test_labels in test_ds:
        test_step(test_images, test_labels)

    elapsed = time.time() - start_time
    history_expert['loss'].append(float(train_loss.result()))
    history_expert['accuracy'].append(float(train_accuracy.result()))
    history_expert['val_loss'].append(float(test_loss.result()))
    history_expert['val_accuracy'].append(float(test_accuracy.result()))

    print(f"Epoch {epoch+1}/{EPOCHS}, "
          f"Loss: {train_loss.result():.4f}, "
          f"Accuracy: {train_accuracy.result():.4f}, "
          f"Val Loss: {test_loss.result():.4f}, "
          f"Val Accuracy: {test_accuracy.result():.4f}, "
          f"Time: {elapsed:.2f}s")

print(f"\n最终测试准确率: {test_accuracy.result():.4f}")

# 2.4 可视化训练过程
print("\n[步骤4] 保存专家模式训练过程可视化图片...")
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].plot(history_expert['accuracy'], label='train accuracy', marker='o')
axes[0].plot(history_expert['val_accuracy'], label='val accuracy', marker='s')
axes[0].set_title('Expert Model Accuracy (Custom Loop)')
axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Accuracy')
axes[0].legend()
axes[0].grid(True)

axes[1].plot(history_expert['loss'], label='train loss', marker='o')
axes[1].plot(history_expert['val_loss'], label='val loss', marker='s')
axes[1].set_title('Expert Model Loss (Custom Loop)')
axes[1].set_xlabel('Epoch')
axes[1].set_ylabel('Loss')
axes[1].legend()
axes[1].grid(True)

plt.tight_layout()
fig_path = os.path.join(output_dir, "part2_expert_training.png")
plt.savefig(fig_path, dpi=150)
print(f"图片已保存: {fig_path}")
plt.close()

print("\n[第二部分完成] Quickstart for Experts 结束")

# ============================================================
# 第三部分: ML Basics with Keras
# ============================================================
print("\n" + "=" * 60)
print("第三部分: ML Basics with Keras")
print("=" * 60)

# 3.1 基本图像分类 (Fashion MNIST)
print("\n[3.1 基本图像分类 - Fashion MNIST]")
print("-" * 40)

fashion_mnist = tf.keras.datasets.fashion_mnist
(x_train_f, y_train_f), (x_test_f, y_test_f) = fashion_mnist.load_data()
x_train_f = x_train_f / 255.0
x_test_f = x_test_f / 255.0

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
print(f"Fashion MNIST 训练集: {x_train_f.shape}")
print(f"类别名称: {class_names}")

# 构建模型
model_fashion = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10)
])
model_fashion.compile(optimizer='adam',
                      loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                      metrics=['accuracy'])

print("\n训练Fashion MNIST分类器 (5 epochs)...")
history_fashion = model_fashion.fit(x_train_f, y_train_f, epochs=5,
                                     validation_split=0.1, verbose=1)

test_loss_f, test_acc_f = model_fashion.evaluate(x_test_f, y_test_f, verbose=2)
print(f"Fashion MNIST 测试准确率: {test_acc_f:.4f}")

# 可视化Fashion MNIST训练过程
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].plot(history_fashion.history['accuracy'], label='train')
axes[0].plot(history_fashion.history['val_accuracy'], label='val')
axes[0].set_title('Fashion MNIST Accuracy')
axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Accuracy')
axes[0].legend()
axes[0].grid(True)

axes[1].plot(history_fashion.history['loss'], label='train')
axes[1].plot(history_fashion.history['val_loss'], label='val')
axes[1].set_title('Fashion MNIST Loss')
axes[1].set_xlabel('Epoch')
axes[1].set_ylabel('Loss')
axes[1].legend()
axes[1].grid(True)
plt.tight_layout()
fig_path = os.path.join(output_dir, "part3_fashion_mnist.png")
plt.savefig(fig_path, dpi=150)
print(f"图片已保存: {fig_path}")
plt.close()

# 3.2 文本分类 (IMDB影评情感分析)
print("\n[3.2 文本分类 - IMDB影评情感分析]")
print("-" * 40)

imdb = tf.keras.datasets.imdb
# 仅保留前10000个最常出现的词
(x_train_t, y_train_t), (x_test_t, y_test_t) = imdb.load_data(num_words=10000)
print(f"IMDB训练集样本数: {len(x_train_t)}")
print(f"IMDB测试集样本数: {len(x_test_t)}")
print(f"第一条影评长度: {len(x_train_t[0])} 词")

# 填充序列到固定长度
x_train_t = tf.keras.preprocessing.sequence.pad_sequences(x_train_t, maxlen=256)
x_test_t = tf.keras.preprocessing.sequence.pad_sequences(x_test_t, maxlen=256)

# 构建Embedding模型
model_text = tf.keras.Sequential([
    tf.keras.layers.Embedding(10000, 16),
    tf.keras.layers.GlobalAveragePooling1D(),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(1, activation='sigmoid')
])
model_text.compile(optimizer='adam',
                   loss='binary_crossentropy',
                   metrics=['accuracy'])
model_text.summary()

print("\n训练文本分类模型 (5 epochs)...")
history_text = model_text.fit(x_train_t, y_train_t, epochs=5,
                               batch_size=512, validation_split=0.1, verbose=1)

test_loss_t, test_acc_t = model_text.evaluate(x_test_t, y_test_t, verbose=2)
print(f"IMDB文本分类测试准确率: {test_acc_t:.4f}")

# 可视化文本分类训练过程
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].plot(history_text.history['accuracy'], label='train')
axes[0].plot(history_text.history['val_accuracy'], label='val')
axes[0].set_title('IMDB Text Classification Accuracy')
axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Accuracy')
axes[0].legend()
axes[0].grid(True)

axes[1].plot(history_text.history['loss'], label='train')
axes[1].plot(history_text.history['val_loss'], label='val')
axes[1].set_title('IMDB Text Classification Loss')
axes[1].set_xlabel('Epoch')
axes[1].set_ylabel('Loss')
axes[1].legend()
axes[1].grid(True)
plt.tight_layout()
fig_path = os.path.join(output_dir, "part3_text_classification.png")
plt.savefig(fig_path, dpi=150)
print(f"图片已保存: {fig_path}")
plt.close()

# 3.3 回归预测 (Auto MPG)
print("\n[3.3 回归预测 - Auto MPG油耗预测]")
print("-" * 40)

# 下载数据集
url = 'http://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data'
column_names = ['MPG', 'Cylinders', 'Displacement', 'Horsepower', 'Weight',
                'Acceleration', 'Model Year', 'Origin']

try:
    import pandas as pd
    raw_dataset = pd.read_csv(url, names=column_names,
                              na_values='?', comment='\t',
                              sep=' ', skipinitialspace=True)
    dataset = raw_dataset.copy()
    print(f"Auto MPG数据集大小: {dataset.shape}")

    # 处理缺失值
    dataset = dataset.dropna()
    print(f"清理后数据集大小: {dataset.shape}")

    # One-hot编码Origin
    dataset['Origin'] = dataset['Origin'].map({1: 'USA', 2: 'Europe', 3: 'Japan'})
    dataset = pd.get_dummies(dataset, columns=['Origin'], prefix='', prefix_sep='')
    print(f"特征列: {list(dataset.columns)}")

    # 划分训练集和测试集
    train_dataset = dataset.sample(frac=0.8, random_state=0)
    test_dataset = dataset.drop(train_dataset.index)

    # 分离标签
    train_features = train_dataset.copy()
    test_features = test_dataset.copy()
    train_labels = train_features.pop('MPG')
    test_labels = test_features.pop('MPG')

    # 标准化
    normalizer = tf.keras.layers.Normalization(axis=-1)
    normalizer.adapt(np.array(train_features))
    print(f"标准化层已适配训练数据")

    # 构建回归模型
    model_regression = tf.keras.Sequential([
        normalizer,
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(1)
    ])
    model_regression.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
                             loss='mean_absolute_error')
    model_regression.summary()

    print("\n训练回归模型 (100 epochs, 显示最后结果)...")
    history_regression = model_regression.fit(
        train_features, train_labels,
        epochs=100, verbose=0,
        validation_split=0.2)

    # 评估
    test_results = model_regression.evaluate(test_features, test_labels, verbose=2)
    print(f"测试集MAE: {test_results:.4f}")

    # 可视化回归训练过程
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(history_regression.history['loss'], label='train loss')
    ax.plot(history_regression.history['val_loss'], label='val loss')
    ax.set_title('Auto MPG Regression Loss')
    ax.set_xlabel('Epoch')
    ax.set_ylabel('MAE (MPG)')
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    fig_path = os.path.join(output_dir, "part3_regression.png")
    plt.savefig(fig_path, dpi=150)
    print(f"图片已保存: {fig_path}")
    plt.close()

    # 预测 vs 真实值
    test_predictions = model_regression.predict(test_features, verbose=0).flatten()
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(test_labels, test_predictions, alpha=0.6)
    ax.plot([test_labels.min(), test_labels.max()],
            [test_labels.min(), test_labels.max()], 'r--', lw=2)
    ax.set_xlabel('True Values [MPG]')
    ax.set_ylabel('Predictions [MPG]')
    ax.set_title('Regression: True vs Predicted')
    ax.grid(True)
    plt.tight_layout()
    fig_path = os.path.join(output_dir, "part3_regression_scatter.png")
    plt.savefig(fig_path, dpi=150)
    print(f"图片已保存: {fig_path}")
    plt.close()

except Exception as e:
    print(f"Auto MPG数据集加载失败: {e}")
    print("跳过回归预测部分")

# 3.4 过拟合与正则化
print("\n[3.4 过拟合与正则化]")
print("-" * 40)

# 使用一个小数据集来演示过拟合
(x_train_s, y_train_s), (x_test_s, y_test_s) = fashion_mnist.load_data()
x_train_s = x_train_s / 255.0
x_test_s = x_test_s / 255.0

# 只使用少量数据来制造过拟合
num_samples = 1000
x_small = x_train_s[:num_samples]
y_small = y_train_s[:num_samples]

# 无正则化模型 (容易过拟合)
model_overfit = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(512, activation='relu'),
    tf.keras.layers.Dense(10)
])
model_overfit.compile(optimizer='adam',
                      loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                      metrics=['accuracy'])

print("训练无正则化模型 (演示过拟合)...")
history_overfit = model_overfit.fit(x_small, y_small, epochs=20,
                                     validation_split=0.2, verbose=0)

# 带正则化的模型
model_regularized = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    tf.keras.layers.Dense(512, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.001)),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(512, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.001)),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(10)
])
model_regularized.compile(optimizer='adam',
                          loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                          metrics=['accuracy'])

print("训练带正则化模型 (L2 + Dropout)...")
history_regularized = model_regularized.fit(x_small, y_small, epochs=20,
                                             validation_split=0.2, verbose=0)

# 可视化过拟合对比
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
axes[0].plot(history_overfit.history['accuracy'], label='train (no reg)')
axes[0].plot(history_overfit.history['val_accuracy'], label='val (no reg)')
axes[0].plot(history_regularized.history['accuracy'], label='train (regularized)')
axes[0].plot(history_regularized.history['val_accuracy'], label='val (regularized)')
axes[0].set_title('Overfitting vs Regularization (Accuracy)')
axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Accuracy')
axes[0].legend()
axes[0].grid(True)

axes[1].plot(history_overfit.history['loss'], label='train (no reg)')
axes[1].plot(history_overfit.history['val_loss'], label='val (no reg)')
axes[1].plot(history_regularized.history['loss'], label='train (regularized)')
axes[1].plot(history_regularized.history['val_loss'], label='val (regularized)')
axes[1].set_title('Overfitting vs Regularization (Loss)')
axes[1].set_xlabel('Epoch')
axes[1].set_ylabel('Loss')
axes[1].legend()
axes[1].grid(True)
plt.tight_layout()
fig_path = os.path.join(output_dir, "part3_overfitting.png")
plt.savefig(fig_path, dpi=150)
print(f"图片已保存: {fig_path}")
plt.close()

print("\n[第三部分完成] ML Basics with Keras 结束")

# ============================================================
# 实验总结
# ============================================================
print("\n" + "=" * 60)
print("实验3总结")
print("=" * 60)
print(f"1. Beginner Quickstart - 测试准确率: {test_acc:.4f}")
print(f"2. Expert Quickstart   - 测试准确率: {test_accuracy.result():.4f}")
print(f"3. Fashion MNIST       - 测试准确率: {test_acc_f:.4f}")
print(f"4. IMDB文本分类        - 测试准确率: {test_acc_t:.4f}")
print(f"\n所有可视化图片已保存到: {output_dir}")
print("=" * 60)
print("实验3完成!")
