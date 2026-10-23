"""
实验1: PyTorch基础
内容: Tensors基础、DataLoaders、Autograd自动微分、神经网络基础、训练分类器（FashionMNIST）
参考: https://docs.pytorch.org/tutorials/beginner/basics/intro.html
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import matplotlib.pyplot as plt
import os

# ============================================================
# 0. 环境检查与设备配置
# ============================================================
print("=" * 60)
print("0. 环境检查与设备配置")
print("=" * 60)

print(f"PyTorch版本: {torch.__version__}")
print(f"CUDA是否可用: {torch.cuda.is_available()}")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"使用设备: {device}")
if torch.cuda.is_available():
    print(f"GPU名称: {torch.cuda.get_device_name(0)}")
print()

# ============================================================
# 1. Tensors基础
# ============================================================
print("=" * 60)
print("1. Tensors基础")
print("=" * 60)

# 1.1 创建Tensor
print("\n--- 1.1 创建Tensor ---")
# 从列表创建
x = torch.tensor([[1, 2], [3, 4], [5, 6]])
print(f"从列表创建的tensor:\n{x}")
print(f"形状: {x.shape}, 数据类型: {x.dtype}, 设备: {x.device}")

# 创建特殊Tensor
zeros = torch.zeros(2, 3)
ones = torch.ones(2, 3)
rand = torch.rand(2, 3)
print(f"\nzeros(2,3):\n{zeros}")
print(f"ones(2,3):\n{ones}")
print(f"rand(2,3):\n{rand}")

# 1.2 Tensor属性与运算
print("\n--- 1.2 Tensor属性与运算 ---")
x = torch.tensor([[1, 2], [3, 4]], dtype=torch.float32)
y = torch.tensor([[5, 6], [7, 8]], dtype=torch.float32)
print(f"x = \n{x}")
print(f"y = \n{y}")
print(f"x + y = \n{x + y}")
print(f"x * y (逐元素乘法) = \n{x * y}")
print(f"x @ y (矩阵乘法) = \n{x @ y}")
print(f"x转置 = \n{x.T}")
print(f"x求和: {x.sum()}")
print(f"x平均值: {x.mean()}")

# 1.3 Tensor与NumPy互转
print("\n--- 1.3 Tensor与NumPy互转 ---")
import numpy as np
np_array = np.array([[1, 2], [3, 4]])
tensor_from_np = torch.from_numpy(np_array)
print(f"NumPy数组:\n{np_array}")
print(f"转换后的Tensor:\n{tensor_from_np}")
np_from_tensor = tensor_from_np.numpy()
print(f"转回NumPy数组:\n{np_from_tensor}")

# 1.4 在GPU上创建Tensor
print("\n--- 1.4 GPU Tensor ---")
if torch.cuda.is_available():
    x_gpu = x.to(device)
    print(f"GPU上的Tensor: {x_gpu}")
    print(f"设备: {x_gpu.device}")
else:
    print("CUDA不可用，跳过GPU Tensor演示")
print()

# ============================================================
# 2. DataLoaders
# ============================================================
print("=" * 60)
print("2. DataLoaders")
print("=" * 60)

# 2.1 准备FashionMNIST数据集
print("\n--- 2.1 加载FashionMNIST数据集 ---")
transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

# 下载训练集和测试集
train_dataset = datasets.FashionMNIST(
    root='./data',
    train=True,
    download=True,
    transform=transform
)

test_dataset = datasets.FashionMNIST(
    root='./data',
    train=False,
    download=True,
    transform=transform
)

print(f"训练集大小: {len(train_dataset)}")
print(f"测试集大小: {len(test_dataset)}")
print(f"类别数: {len(train_dataset.classes)}")
print(f"类别名称: {train_dataset.classes}")

# 2.2 创建DataLoader
print("\n--- 2.2 创建DataLoader ---")
batch_size = 64
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

print(f"训练批次数量: {len(train_loader)}")
print(f"每批次大小: {batch_size}")

# 获取一个批次的数据
images, labels = next(iter(train_loader))
print(f"一个批次的图像形状: {images.shape}")  # [batch_size, 1, 28, 28]
print(f"一个批次的标签形状: {labels.shape}")
print(f"第一个图像的数据范围: [{images[0].min():.4f}, {images[0].max():.4f}]")

# 2.3 可视化部分数据
print("\n--- 2.3 可视化数据集样本 ---")
fig, axes = plt.subplots(2, 5, figsize=(12, 6))
for i, ax in enumerate(axes.flat):
    img = images[i].squeeze().numpy()
    ax.imshow(img, cmap='gray')
    ax.set_title(f"Label: {train_dataset.classes[labels[i]]}")
    ax.axis('off')
plt.suptitle("FashionMNIST Sample Visualization", fontsize=14)
plt.tight_layout()
plt.savefig("fashion_mnist_samples.png", dpi=150)
print("样本可视化已保存到 fashion_mnist_samples.png")
plt.close()
print()

# ============================================================
# 3. Autograd自动微分
# ============================================================
print("=" * 60)
print("3. Autograd自动微分")
print("=" * 60)

# 3.1 基本自动微分
print("\n--- 3.1 基本自动微分 ---")
x = torch.tensor(2.0, requires_grad=True)
y = torch.tensor(3.0, requires_grad=True)
z = x ** 2 + y ** 3
print(f"x = {x.item()}, y = {y.item()}")
print(f"z = x^2 + y^3 = {z.item()}")

z.backward()
print(f"dz/dx = {x.grad.item()} (期望: 2*x = 4)")
print(f"dz/dy = {y.grad.item()} (期望: 3*y^2 = 27)")

# 3.2 复杂函数的梯度
print("\n--- 3.2 复杂函数的梯度 ---")
x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
y = torch.sin(x)
loss = y.sum()
loss.backward()
print(f"x = {x.data}")
print(f"y = sin(x) = {y.data}")
print(f"loss = sum(y) = {loss.item()}")
print(f"d(loss)/dx = {x.grad} (期望: cos(x))")

# 3.3 关闭梯度跟踪
print("\n--- 3.3 关闭梯度跟踪 ---")
with torch.no_grad():
    y = x * 2
    print(f"no_grad模式下: y = {y}")
    print(f"requires_grad: {y.requires_grad}")
print()

# ============================================================
# 4. 神经网络基础
# ============================================================
print("=" * 60)
print("4. 神经网络基础")
print("=" * 60)

# 4.1 使用nn.Module定义网络
print("\n--- 4.1 定义神经网络 ---")

class NeuralNetwork(nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(28*28, 512),
            nn.ReLU(),
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 10),
        )

    def forward(self, x):
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits

model = NeuralNetwork().to(device)
print("网络结构:")
print(model)

# 统计参数数量
total_params = sum(p.numel() for p in model.parameters())
trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
print(f"\n总参数数量: {total_params}")
print(f"可训练参数数量: {trainable_params}")

# 4.2 前向传播测试
print("\n--- 4.2 前向传播测试 ---")
sample_input = torch.rand(1, 1, 28, 28).to(device)
output = model(sample_input)
print(f"输入形状: {sample_input.shape}")
print(f"输出形状: {output.shape}")
print(f"输出(未归一化logits): {output.squeeze()}")
print(f"预测类别: {output.argmax(dim=1).item()}")

# 4.3 损失函数和优化器
print("\n--- 4.3 损失函数和优化器 ---")
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.9)
print(f"损失函数: {criterion}")
print(f"优化器: {optimizer}")
print()

# ============================================================
# 5. 训练分类器（FashionMNIST）
# ============================================================
print("=" * 60)
print("5. 训练分类器（FashionMNIST）")
print("=" * 60)

def train_epoch(model, loader, criterion, optimizer, device):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    for batch_idx, (images, labels) in enumerate(loader):
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
        _, predicted = outputs.max(1)
        total += labels.size(0)
        correct += predicted.eq(labels).sum().item()
    return running_loss / len(loader), 100. * correct / total

def test_epoch(model, loader, criterion, device):
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)
            running_loss += loss.item()
            _, predicted = outputs.max(1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()
    return running_loss / len(loader), 100. * correct / total

# 训练参数
num_epochs = 5
print(f"\n训练参数: epochs={num_epochs}, batch_size={batch_size}, lr=0.01")
print("开始训练...\n")

train_losses = []
train_accs = []
test_losses = []
test_accs = []

for epoch in range(1, num_epochs + 1):
    train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer, device)
    test_loss, test_acc = test_epoch(model, test_loader, criterion, device)
    train_losses.append(train_loss)
    train_accs.append(train_acc)
    test_losses.append(test_loss)
    test_accs.append(test_acc)
    print(f"Epoch [{epoch}/{num_epochs}] "
          f"Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.2f}% | "
          f"Test Loss: {test_loss:.4f} | Test Acc: {test_acc:.2f}%")

print("\n训练完成!")

# 保存模型
model_path = "fashion_mnist_model.pth"
torch.save(model.state_dict(), model_path)
print(f"模型已保存到 {model_path}")

# 5.1 可视化训练过程
print("\n--- 5.1 可视化训练过程 ---")
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# 损失曲线
axes[0].plot(range(1, num_epochs + 1), train_losses, 'b-o', label='Train Loss')
axes[0].plot(range(1, num_epochs + 1), test_losses, 'r-s', label='Test Loss')
axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Loss')
axes[0].set_title('Training and Test Loss Curve')
axes[0].legend()
axes[0].grid(True)

# 准确率曲线
axes[1].plot(range(1, num_epochs + 1), train_accs, 'b-o', label='Train Accuracy')
axes[1].plot(range(1, num_epochs + 1), test_accs, 'r-s', label='Test Accuracy')
axes[1].set_xlabel('Epoch')
axes[1].set_ylabel('Accuracy (%)')
axes[1].set_title('Training and Test Accuracy Curve')
axes[1].legend()
axes[1].grid(True)

plt.tight_layout()
plt.savefig("training_curves.png", dpi=150)
print("训练曲线已保存到 training_curves.png")
plt.close()

# 5.2 可视化预测结果
print("\n--- 5.2 可视化预测结果 ---")
model.eval()
test_images, test_labels = next(iter(test_loader))
test_images = test_images.to(device)
with torch.no_grad():
    outputs = model(test_images)
    predictions = outputs.argmax(dim=1)

fig, axes = plt.subplots(2, 5, figsize=(14, 7))
for i, ax in enumerate(axes.flat):
    img = test_images[i].cpu().squeeze().numpy()
    pred = predictions[i].cpu().item()
    true = test_labels[i].item()
    color = 'green' if pred == true else 'red'
    ax.imshow(img, cmap='gray')
    ax.set_title(f"Pred: {train_dataset.classes[pred]}\nTrue: {train_dataset.classes[true]}", color=color)
    ax.axis('off')
plt.suptitle("FashionMNIST Prediction Visualization", fontsize=14)
plt.tight_layout()
plt.savefig("prediction_results.png", dpi=150)
print("预测结果可视化已保存到 prediction_results.png")
plt.close()

# 5.3 最终评估
print("\n--- 5.3 最终评估 ---")
final_test_loss, final_test_acc = test_epoch(model, test_loader, criterion, device)
print(f"最终测试损失: {final_test_loss:.4f}")
print(f"最终测试准确率: {final_test_acc:.2f}%")

# 各类别准确率
class_correct = [0.] * 10
class_total = [0.] * 10
model.eval()
with torch.no_grad():
    for images, labels in test_loader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        _, predicted = outputs.max(1)
        c = (predicted == labels).squeeze()
        for i in range(len(labels)):
            label = labels[i]
            class_correct[label] += c[i].item()
            class_total[label] += 1

print("\n各类别准确率:")
for i in range(10):
    acc = 100 * class_correct[i] / class_total[i]
    print(f"  {train_dataset.classes[i]:15s}: {acc:.2f}%")

print("\n" + "=" * 60)
print("实验1完成!")
print("=" * 60)
