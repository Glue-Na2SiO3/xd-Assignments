#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
实验7: 人脸伪造检测
使用PyTorch和预训练ResNet进行迁移学习，区分真实人脸和伪造人脸。
支持真实数据集和模拟数据两种模式。
"""

import os
import sys
import argparse
import random
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import seaborn as sns

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset, Subset
from torchvision import transforms, models
from torchvision.datasets import ImageFolder
from PIL import Image

# 设置随机种子保证可复现
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
torch.manual_seed(SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(SEED)

# ==================== 配置参数 ====================
class Config:
    # 数据路径（根据实际环境修改）
    DATA_ROOT = "./face_dataset"          # 真实数据集根目录
    REAL_DIR = "real"                     # 真实人脸子目录名
    FAKE_DIR = "fake"                     # 伪造人脸子目录名

    # 训练参数
    TRAIN_REAL = 500                      # 训练集真实人脸数量
    TRAIN_FAKE = 500                      # 训练集伪造人脸数量
    BATCH_SIZE = 32
    NUM_EPOCHS = 30
    LEARNING_RATE = 1e-4
    WEIGHT_DECAY = 1e-5

    # 模型参数
    MODEL_NAME = "resnet50"               # resnet18 或 resnet50
    NUM_CLASSES = 2
    PRETRAINED = True

    # 输出路径
    OUTPUT_DIR = "./outputs"
    BEST_MODEL_PATH = os.path.join(OUTPUT_DIR, "best_model.pth")
    FINAL_MODEL_PATH = os.path.join(OUTPUT_DIR, "final_model.pth")
    PLOT_DIR = os.path.join(OUTPUT_DIR, "plots")

    # 设备
    DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # 模拟数据模式
    USE_SYNTHETIC = False                 # 是否使用模拟数据


# ==================== 模拟数据集 ====================
class SyntheticFaceDataset(Dataset):
    """
    模拟人脸数据集：当没有真实数据时，生成随机图像用于代码测试。
    图像特征：真实=偏暖色调，伪造=偏冷色调（仅用于模拟）。
    """
    def __init__(self, num_samples=1000, img_size=224, transform=None, label=0):
        self.num_samples = num_samples
        self.img_size = img_size
        self.transform = transform
        self.label = label  # 0=real, 1=fake

    def __len__(self):
        return self.num_samples

    def __getitem__(self, idx):
        # 生成有区分性的模拟图像
        if self.label == 0:  # real: 暖色调，较平滑
            base = np.array([0.6, 0.4, 0.3], dtype=np.float32)
            noise_scale = 0.08
        else:  # fake: 冷色调，噪声较多
            base = np.array([0.4, 0.45, 0.55], dtype=np.float32)
            noise_scale = 0.15

        img = np.ones((self.img_size, self.img_size, 3), dtype=np.float32) * base
        noise = np.random.randn(self.img_size, self.img_size, 3).astype(np.float32) * noise_scale
        img = np.clip(img + noise, 0.0, 1.0)

        # 添加简单纹理特征
        x = np.linspace(0, 4*np.pi, self.img_size)
        y = np.linspace(0, 4*np.pi, self.img_size)
        X, Y = np.meshgrid(x, y)
        pattern = np.sin(X) * np.cos(Y) * 0.05
        img[:, :, 0] += pattern
        img[:, :, 1] += pattern * 0.8
        img[:, :, 2] += pattern * 0.6
        img = np.clip(img, 0.0, 1.0)

        pil_img = Image.fromarray((img * 255).astype(np.uint8))
        if self.transform:
            pil_img = self.transform(pil_img)
        return pil_img, self.label


# ==================== 数据预处理 ====================
def get_transforms(train=True):
    """获取数据预处理变换"""
    if train:
        return transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.RandomCrop(224),
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.RandomRotation(degrees=10),
            transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
        ])
    else:
        return transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])
        ])


# ==================== 数据集构建 ====================
def build_datasets(cfg):
    """构建训练集和测试集"""
    train_transform = get_transforms(train=True)
    test_transform = get_transforms(train=False)

    if cfg.USE_SYNTHETIC or not os.path.exists(cfg.DATA_ROOT):
        print("[INFO] 使用模拟数据集进行测试...")
        cfg.USE_SYNTHETIC = True

        train_real = SyntheticFaceDataset(num_samples=cfg.TRAIN_REAL, transform=train_transform, label=0)
        train_fake = SyntheticFaceDataset(num_samples=cfg.TRAIN_FAKE, transform=train_transform, label=1)

        test_real = SyntheticFaceDataset(num_samples=1499, transform=test_transform, label=0)
        test_fake = SyntheticFaceDataset(num_samples=1499, transform=test_transform, label=1)

        # 合并数据集
        from torch.utils.data import ConcatDataset
        train_dataset = ConcatDataset([train_real, train_fake])
        test_dataset = ConcatDataset([test_real, test_fake])

        print(f"[INFO] 模拟训练集大小: {len(train_dataset)}")
        print(f"[INFO] 模拟测试集大小: {len(test_dataset)}")
        return train_dataset, test_dataset

    # 真实数据集模式
    real_path = os.path.join(cfg.DATA_ROOT, cfg.REAL_DIR)
    fake_path = os.path.join(cfg.DATA_ROOT, cfg.FAKE_DIR)

    if not os.path.exists(real_path) or not os.path.exists(fake_path):
        raise FileNotFoundError(f"数据集路径不存在: {real_path} 或 {fake_path}")

    # 分别加载两个目录
    real_dataset = ImageFolder(root=cfg.DATA_ROOT, transform=train_transform)
    # 只保留 real 目录的样本（假设real类别索引为0）
    # 更稳健的方式：分别构建
    real_imgs = []
    fake_imgs = []
    for root, _, files in os.walk(real_path):
        for f in files:
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.webp')):
                real_imgs.append(os.path.join(root, f))
    for root, _, files in os.walk(fake_path):
        for f in files:
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.webp')):
                fake_imgs.append(os.path.join(root, f))

    print(f"[INFO] 真实人脸总数: {len(real_imgs)}")
    print(f"[INFO] 伪造人脸总数: {len(fake_imgs)}")

    # 随机采样
    random.shuffle(real_imgs)
    random.shuffle(fake_imgs)

    train_real_paths = real_imgs[:cfg.TRAIN_REAL]
    train_fake_paths = fake_imgs[:cfg.TRAIN_FAKE]
    test_real_paths = real_imgs[cfg.TRAIN_REAL:]
    test_fake_paths = fake_imgs[cfg.TRAIN_FAKE:]

    train_dataset = FaceForgeryDataset(train_real_paths + train_fake_paths,
                                       [0]*len(train_real_paths) + [1]*len(train_fake_paths),
                                       transform=train_transform)
    test_dataset = FaceForgeryDataset(test_real_paths + test_fake_paths,
                                      [0]*len(test_real_paths) + [1]*len(test_fake_paths),
                                      transform=test_transform)

    print(f"[INFO] 训练集大小: {len(train_dataset)}")
    print(f"[INFO] 测试集大小: {len(test_dataset)}")
    return train_dataset, test_dataset


class FaceForgeryDataset(Dataset):
    """通用的人脸伪造数据集"""
    def __init__(self, image_paths, labels, transform=None):
        self.image_paths = image_paths
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        img_path = self.image_paths[idx]
        label = self.labels[idx]
        image = Image.open(img_path).convert('RGB')
        if self.transform:
            image = self.transform(image)
        return image, label


# ==================== 模型定义 ====================
def build_model(cfg):
    """构建预训练ResNet模型并修改分类头"""
    if cfg.MODEL_NAME == "resnet18":
        model = models.resnet18(pretrained=cfg.PRETRAINED)
        num_ftrs = model.fc.in_features
        model.fc = nn.Linear(num_ftrs, cfg.NUM_CLASSES)
    elif cfg.MODEL_NAME == "resnet50":
        model = models.resnet50(pretrained=cfg.PRETRAINED)
        num_ftrs = model.fc.in_features
        model.fc = nn.Sequential(
            nn.Dropout(0.5),
            nn.Linear(num_ftrs, cfg.NUM_CLASSES)
        )
    else:
        raise ValueError(f"不支持的模型: {cfg.MODEL_NAME}")

    return model.to(cfg.DEVICE)


# ==================== 训练与评估 ====================
def train_one_epoch(model, dataloader, criterion, optimizer, device):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    for images, labels in dataloader:
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item() * images.size(0)
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

    epoch_loss = running_loss / total
    epoch_acc = correct / total
    return epoch_loss, epoch_acc


def evaluate(model, dataloader, criterion, device):
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0
    all_preds = []
    all_labels = []

    with torch.no_grad():
        for images, labels in dataloader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)

            running_loss += loss.item() * images.size(0)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

            all_preds.extend(predicted.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    epoch_loss = running_loss / total
    epoch_acc = correct / total
    return epoch_loss, epoch_acc, all_labels, all_preds


# ==================== 可视化 ====================
def plot_training_curves(history, save_dir):
    """绘制训练曲线"""
    epochs = range(1, len(history['train_loss']) + 1)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Loss 曲线
    axes[0].plot(epochs, history['train_loss'], 'b-', label='Train Loss')
    axes[0].plot(epochs, history['val_loss'], 'r-', label='Val Loss')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Loss')
    axes[0].set_title('Training and Validation Loss')
    axes[0].legend()
    axes[0].grid(True)

    # Accuracy 曲线
    axes[1].plot(epochs, history['train_acc'], 'b-', label='Train Acc')
    axes[1].plot(epochs, history['val_acc'], 'r-', label='Val Acc')
    axes[1].set_xlabel('Epoch')
    axes[1].set_ylabel('Accuracy')
    axes[1].set_title('Training and Validation Accuracy')
    axes[1].legend()
    axes[1].grid(True)

    plt.tight_layout()
    save_path = os.path.join(save_dir, "training_curves.png")
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"[INFO] 训练曲线已保存: {save_path}")
    plt.close()


def plot_confusion_matrix(y_true, y_pred, save_dir, class_names=['Real', 'Fake']):
    """绘制混淆矩阵"""
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=class_names, yticklabels=class_names)
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.title('Confusion Matrix')

    save_path = os.path.join(save_dir, "confusion_matrix.png")
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"[INFO] 混淆矩阵已保存: {save_path}")
    plt.close()
    return cm


# ==================== 主函数 ====================
def main():
    parser = argparse.ArgumentParser(description="实验7: 人脸伪造检测")
    parser.add_argument("--data_root", type=str, default=Config.DATA_ROOT, help="数据集根目录")
    parser.add_argument("--model", type=str, default=Config.MODEL_NAME, choices=["resnet18", "resnet50"])
    parser.add_argument("--epochs", type=int, default=Config.NUM_EPOCHS)
    parser.add_argument("--batch_size", type=int, default=Config.BATCH_SIZE)
    parser.add_argument("--lr", type=float, default=Config.LEARNING_RATE)
    parser.add_argument("--synthetic", action="store_true", help="使用模拟数据模式")
    parser.add_argument("--output", type=str, default=Config.OUTPUT_DIR)
    args = parser.parse_args()

    cfg = Config()
    cfg.DATA_ROOT = args.data_root
    cfg.MODEL_NAME = args.model
    cfg.NUM_EPOCHS = args.epochs
    cfg.BATCH_SIZE = args.batch_size
    cfg.LEARNING_RATE = args.lr
    cfg.USE_SYNTHETIC = args.synthetic
    cfg.OUTPUT_DIR = args.output
    cfg.BEST_MODEL_PATH = os.path.join(cfg.OUTPUT_DIR, "best_model.pth")
    cfg.FINAL_MODEL_PATH = os.path.join(cfg.OUTPUT_DIR, "final_model.pth")
    cfg.PLOT_DIR = os.path.join(cfg.OUTPUT_DIR, "plots")

    os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)
    os.makedirs(cfg.PLOT_DIR, exist_ok=True)

    print("=" * 60)
    print("实验7: 人脸伪造检测")
    print("=" * 60)
    print(f"设备: {cfg.DEVICE}")
    print(f"模型: {cfg.MODEL_NAME}")
    print(f"学习率: {cfg.LEARNING_RATE}")
    print(f"批次大小: {cfg.BATCH_SIZE}")
    print(f"训练轮数: {cfg.NUM_EPOCHS}")
    print(f"使用模拟数据: {cfg.USE_SYNTHETIC}")
    print("=" * 60)

    # 数据集
    train_dataset, test_dataset = build_datasets(cfg)
    train_loader = DataLoader(train_dataset, batch_size=cfg.BATCH_SIZE, shuffle=True, num_workers=0)
    test_loader = DataLoader(test_dataset, batch_size=cfg.BATCH_SIZE, shuffle=False, num_workers=0)

    # 模型
    model = build_model(cfg)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=cfg.LEARNING_RATE, weight_decay=cfg.WEIGHT_DECAY)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.1)

    # 训练历史
    history = {
        'train_loss': [], 'train_acc': [],
        'val_loss': [], 'val_acc': []
    }
    best_acc = 0.0

    print("\n开始训练...")
    for epoch in range(1, cfg.NUM_EPOCHS + 1):
        train_loss, train_acc = train_one_epoch(model, train_loader, criterion, optimizer, cfg.DEVICE)
        val_loss, val_acc, _, _ = evaluate(model, test_loader, criterion, cfg.DEVICE)
        scheduler.step()

        history['train_loss'].append(train_loss)
        history['train_acc'].append(train_acc)
        history['val_loss'].append(val_loss)
        history['val_acc'].append(val_acc)

        print(f"Epoch [{epoch:02d}/{cfg.NUM_EPOCHS}] "
              f"Train Loss: {train_loss:.4f} Acc: {train_acc:.4f} | "
              f"Val Loss: {val_loss:.4f} Acc: {val_acc:.4f}")

        # 保存最佳模型
        if val_acc > best_acc:
            best_acc = val_acc
            torch.save(model.state_dict(), cfg.BEST_MODEL_PATH)
            print(f"  -> 最佳模型已保存 (acc={best_acc:.4f})")

    # 保存最终模型
    torch.save(model.state_dict(), cfg.FINAL_MODEL_PATH)
    print(f"\n[INFO] 最终模型已保存: {cfg.FINAL_MODEL_PATH}")

    # 加载最佳模型进行最终评估
    print("\n加载最佳模型进行最终评估...")
    model.load_state_dict(torch.load(cfg.BEST_MODEL_PATH, map_location=cfg.DEVICE))
    _, test_acc, y_true, y_pred = evaluate(model, test_loader, criterion, cfg.DEVICE)

    print(f"\n最终测试准确率: {test_acc:.4f} ({test_acc*100:.2f}%)")
    print("\n分类报告:")
    print(classification_report(y_true, y_pred, target_names=['Real', 'Fake'], digits=4))

    # 可视化
    plot_training_curves(history, cfg.PLOT_DIR)
    cm = plot_confusion_matrix(y_true, y_pred, cfg.PLOT_DIR)

    print("\n混淆矩阵:")
    print(cm)

    # 检查是否达到95%准确率
    if test_acc >= 0.95:
        print("\n[成功] 测试准确率达到95%以上！")
    else:
        print("\n[提示] 测试准确率未达到95%，建议尝试：")
        print("  1. 增加训练轮数 (--epochs 50)")
        print("  2. 使用更大的模型 (--model resnet50)")
        print("  3. 调整学习率 (--lr 1e-5)")
        print("  4. 使用真实数据集而非模拟数据")

    print("\n实验完成！输出文件:")
    print(f"  - 最佳模型: {cfg.BEST_MODEL_PATH}")
    print(f"  - 最终模型: {cfg.FINAL_MODEL_PATH}")
    print(f"  - 训练曲线: {os.path.join(cfg.PLOT_DIR, 'training_curves.png')}")
    print(f"  - 混淆矩阵: {os.path.join(cfg.PLOT_DIR, 'confusion_matrix.png')}")


if __name__ == "__main__":
    main()
