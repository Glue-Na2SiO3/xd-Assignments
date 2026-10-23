"""
实验2: PyTorch进阶
内容: TorchVision目标检测（Faster R-CNN）、TorchText文本分类（AG_NEWS）
参考: https://docs.pytorch.org/tutorials/domains.html
"""

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
import numpy as np
import os
import time

print("=" * 70)
print("实验2: PyTorch进阶")
print("=" * 70)
print(f"PyTorch版本: {torch.__version__}")
print(f"CUDA是否可用: {torch.cuda.is_available()}")
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"使用设备: {device}")
if torch.cuda.is_available():
    print(f"GPU名称: {torch.cuda.get_device_name(0)}")
print()

# ============================================================
# 第一部分: TorchVision目标检测 (Faster R-CNN)
# ============================================================
print("=" * 70)
print("第一部分: TorchVision目标检测 (Faster R-CNN)")
print("=" * 70)

try:
    import torchvision
    from torchvision.models.detection import fasterrcnn_resnet50_fpn, FasterRCNN_ResNet50_FPN_Weights
    from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
    from torchvision import transforms
    from PIL import Image
    print("TorchVision版本:", torchvision.__version__)

    # 1.1 加载预训练的Faster R-CNN模型
    print("\n--- 1.1 加载预训练Faster R-CNN模型 ---")
    weights = FasterRCNN_ResNet50_FPN_Weights.DEFAULT
    model_det = fasterrcnn_resnet50_fpn(weights=weights).to(device)
    model_det.eval()
    print("模型加载完成")
    print(f"模型类别数(含背景): {model_det.roi_heads.box_predictor.cls_score.in_features}")

    # COCO数据集类别名称 (91类, 含背景)
    COCO_INSTANCE_CATEGORY_NAMES = [
        '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
        'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
        'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
        'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A',
        'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
        'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
        'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
        'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
        'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table',
        'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
        'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
        'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
    ]

    # 1.2 准备测试图像 (修改为加载本地真实图片)
    print("\n--- 1.2 准备测试图像 ---")
    # 请将此处替换为你的本地图片路径（支持jpg/png等格式）
    local_image_path = "test_image.png"  # 核心修改：指定本地图片路径
    if os.path.exists(local_image_path):
        test_image = Image.open(local_image_path).convert("RGB")  # 确保RGB格式
        print(f"成功加载本地图片: {local_image_path}")
    else:
        # 备用方案：如果本地图片不存在，生成简单随机图片（保留原有逻辑）
        print(f"本地图片 {local_image_path} 不存在，生成模拟测试图片")
        np.random.seed(42)
        img_array = np.ones((400, 600, 3), dtype=np.uint8) * 240  # 浅色背景
        # 添加几个彩色矩形块作为模拟目标
        rectangles = [
            (50, 50, 150, 200, [200, 50, 50]),    # 红色块
            (250, 80, 180, 150, [50, 150, 50]),   # 绿色块
            (450, 120, 100, 100, [50, 50, 200]),  # 蓝色块
            (100, 250, 200, 120, [200, 200, 50]), # 黄色块
            (350, 280, 150, 100, [150, 50, 150]), # 紫色块
        ]
        for x1, y1, w, h, color in rectangles:
            img_array[y1:y1+h, x1:x1+w] = color
        test_image = Image.fromarray(img_array)
        local_image_path = "detection_test_image.png"
        test_image.save(local_image_path)
    
    test_image_path = local_image_path  # 统一图片路径变量
    print(f"测试图像路径: {test_image_path}")
    print(f"图像尺寸: {test_image.size}")

    # 1.3 图像预处理与推理 (无修改)
    print("\n--- 1.3 图像预处理与推理 ---")
    preprocess = weights.transforms()
    img_tensor = preprocess(test_image).to(device)
    print(f"预处理后张量形状: {img_tensor.shape}")

    with torch.no_grad():
        predictions = model_det([img_tensor])

    pred = predictions[0]
    boxes = pred['boxes'].cpu().numpy()
    labels = pred['labels'].cpu().numpy()
    scores = pred['scores'].cpu().numpy()

    # 过滤低置信度结果
    score_threshold = 0.5
    keep = scores >= score_threshold
    boxes = boxes[keep]
    labels = labels[keep]
    scores = scores[keep]

    print(f"检测到 {len(boxes)} 个目标 (置信度>={score_threshold})")
    for i, (box, label, score) in enumerate(zip(boxes, labels, scores)):
        name = COCO_INSTANCE_CATEGORY_NAMES[label] if label < len(COCO_INSTANCE_CATEGORY_NAMES) else "unknown"
        print(f"  目标{i+1}: {name}, 置信度: {score:.4f}, 位置: [{box[0]:.1f}, {box[1]:.1f}, {box[2]:.1f}, {box[3]:.1f}]")

    # 1.4 可视化检测结果 (无修改)
    print("\n--- 1.4 可视化检测结果 ---")
    fig, ax = plt.subplots(1, figsize=(12, 8))
    ax.imshow(test_image)

    # 为不同类别生成颜色
    np.random.seed(0)
    colors = np.random.rand(91, 3)

    for box, label, score in zip(boxes, labels, scores):
        x1, y1, x2, y2 = box
        color = colors[label % 91]
        rect = plt.Rectangle((x1, y1), x2-x1, y2-y1, linewidth=2, edgecolor=color, facecolor='none')
        ax.add_patch(rect)
        name = COCO_INSTANCE_CATEGORY_NAMES[label] if label < len(COCO_INSTANCE_CATEGORY_NAMES) else "unknown"
        ax.text(x1, y1-5, f"{name}: {score:.2f}", color='white', fontsize=10,
                bbox=dict(facecolor=color, alpha=0.7, edgecolor='none', pad=2))

    ax.set_title("Faster R-CNN Object Detection Results", fontsize=14)
    ax.axis('off')
    plt.tight_layout()
    plt.savefig("detection_results.png", dpi=150, bbox_inches='tight')
    print("检测结果可视化已保存到 detection_results.png")
    plt.close()

    # 1.5 模型微调说明 (无修改)
    print("\n--- 1.5 模型微调 (Fine-tuning) 示例代码 ---")
    print("""
# 自定义数据集微调Faster R-CNN的示例代码:

def get_model_instance_segmentation(num_classes):
    # 加载预训练模型
    model = fasterrcnn_resnet50_fpn(weights=FasterRCNN_ResNet50_FPN_Weights.DEFAULT)
    
    # 获取分类器输入特征数
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    
    # 替换为新的预测头
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
    
    return model

# 假设有自定义数据集, 类别数为5 (含背景)
# num_classes = 5
# custom_model = get_model_instance_segmentization(num_classes).to(device)
# optimizer = optim.SGD(custom_model.parameters(), lr=0.005, momentum=0.9)
# 然后使用自定义数据进行训练...
    """)

except Exception as e:
    print(f"目标检测部分运行出错: {e}")
    print("请确保已安装torchvision: pip install torchvision")

print()

# ============================================================
# 第二部分: TorchText文本分类 (AG_NEWS)
# ============================================================
print("=" * 70)
print("第二部分: TorchText文本分类 (AG_NEWS)")
print("=" * 70)

try:
    import torchtext
    from torchtext.datasets import AG_NEWS
    from torchtext.data.utils import get_tokenizer
    from torchtext.vocab import build_vocab_from_iterator
    print("TorchText版本:", torchtext.__version__)

    # 2.1 加载AG_NEWS数据集
    print("\n--- 2.1 加载AG_NEWS数据集 ---")
    train_iter, test_iter = AG_NEWS(split=('train', 'test'))

    # 查看数据样本
    print("数据集样本示例:")
    labels_map = {1: "World", 2: "Sports", 3: "Business", 4: "Sci/Tech"}
    samples = []
    for i, (label, text) in enumerate(train_iter):
        if i < 3:
            print(f"  样本{i+1}: 类别={labels_map[label]}, 文本={text[:100]}...")
        samples.append((label, text))
    print(f"训练集样本总数: {len(samples)}")

    # 重新获取迭代器
    train_iter, test_iter = AG_NEWS(split=('train', 'test'))

    # 2.2 文本预处理: 分词与构建词表
    print("\n--- 2.2 文本预处理: 分词与构建词表 ---")
    tokenizer = get_tokenizer('basic_english')

    def yield_tokens(data_iter):
        for _, text in data_iter:
            yield tokenizer(text)

    # 构建词表 (限制词汇量)
    vocab = build_vocab_from_iterator(yield_tokens(train_iter), specials=["<unk>"])
    vocab.set_default_index(vocab["<unk>"])

    print(f"词表大小: {len(vocab)}")
    print(f"前10个词: {vocab.get_itos()[:10]}")

    # 2.3 文本编码与DataLoader
    print("\n--- 2.3 文本编码与DataLoader ---")

    def text_pipeline(x):
        return vocab(tokenizer(x))

    def label_pipeline(x):
        return int(x) - 1  # 将1-4映射到0-3

    # 重新加载数据
    train_iter, test_iter = AG_NEWS(split=('train', 'test'))

    def collate_batch(batch):
        label_list, text_list, offsets = [], [], [0]
        for (_label, _text) in batch:
            label_list.append(label_pipeline(_label))
            processed_text = torch.tensor(text_pipeline(_text), dtype=torch.int64)
            text_list.append(processed_text)
            offsets.append(processed_text.size(0))
        label_list = torch.tensor(label_list, dtype=torch.int64)
        offsets = torch.tensor(offsets[:-1]).cumsum(dim=0)
        text_list = torch.cat(text_list)
        return label_list.to(device), text_list.to(device), offsets.to(device)

    batch_size = 64
    train_loader = DataLoader(list(train_iter), batch_size=batch_size, shuffle=True, collate_fn=collate_batch)
    test_loader = DataLoader(list(test_iter), batch_size=batch_size, shuffle=False, collate_fn=collate_batch)

    print(f"批次大小: {batch_size}")
    print(f"训练批次数量: {len(train_loader)}")
    print(f"测试批次数量: {len(test_loader)}")

    # 查看一个批次的数据
    train_iter_check, _ = AG_NEWS(split=('train', 'test'))
    check_loader = DataLoader(list(train_iter_check), batch_size=2, shuffle=False, collate_fn=collate_batch)
    labels, texts, offsets = next(iter(check_loader))
    print(f"\n一个批次示例:")
    print(f"  标签形状: {labels.shape}, 值: {labels}")
    print(f"  文本编码形状: {texts.shape}")
    print(f"  偏移量: {offsets}")

    # 2.4 定义文本分类模型
    print("\n--- 2.4 定义文本分类模型 ---")

    class TextClassificationModel(nn.Module):
        def __init__(self, vocab_size, embed_dim, num_class):
            super(TextClassificationModel, self).__init__()
            self.embedding = nn.EmbeddingBag(vocab_size, embed_dim, sparse=False)
            self.fc = nn.Linear(embed_dim, num_class)
            self.init_weights()

        def init_weights(self):
            initrange = 0.5
            self.embedding.weight.data.uniform_(-initrange, initrange)
            self.fc.weight.data.uniform_(-initrange, initrange)
            self.fc.bias.data.zero_()

        def forward(self, text, offsets):
            embedded = self.embedding(text, offsets)
            return self.fc(embedded)

    vocab_size = len(vocab)
    embed_dim = 64
    num_classes = 4
    text_model = TextClassificationModel(vocab_size, embed_dim, num_classes).to(device)

    print(f"词表大小: {vocab_size}")
    print(f"嵌入维度: {embed_dim}")
    print(f"类别数: {num_classes}")
    print(f"模型结构:\n{text_model}")

    total_params = sum(p.numel() for p in text_model.parameters())
    print(f"总参数数量: {total_params}")

    # 2.5 训练文本分类模型
    print("\n--- 2.5 训练文本分类模型 ---")

    def train_text_model(model, loader, criterion, optimizer, device):
        model.train()
        total_acc, total_count = 0, 0
        total_loss = 0
        for idx, (label, text, offsets) in enumerate(loader):
            optimizer.zero_grad()
            output = model(text, offsets)
            loss = criterion(output, label)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
            total_acc += (output.argmax(1) == label).sum().item()
            total_count += label.size(0)
        return total_loss / len(loader), total_acc / total_count

    def evaluate_text_model(model, loader, criterion, device):
        model.eval()
        total_acc, total_count = 0, 0
        total_loss = 0
        with torch.no_grad():
            for idx, (label, text, offsets) in enumerate(loader):
                output = model(text, offsets)
                loss = criterion(output, label)
                total_loss += loss.item()
                total_acc += (output.argmax(1) == label).sum().item()
                total_count += label.size(0)
        return total_loss / len(loader), total_acc / total_count

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(text_model.parameters(), lr=4.0)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=1, gamma=0.9)

    num_epochs = 5
    print(f"训练参数: epochs={num_epochs}, lr=4.0, scheduler=StepLR(gamma=0.9)")
    print("开始训练...\n")

    train_losses, train_accs = [], []
    test_losses, test_accs = [], []

    for epoch in range(1, num_epochs + 1):
        epoch_start_time = time.time()
        train_loss, train_acc = train_text_model(text_model, train_loader, criterion, optimizer, device)
        test_loss, test_acc = evaluate_text_model(text_model, test_loader, criterion, device)
        scheduler.step()

        train_losses.append(train_loss)
        train_accs.append(train_acc)
        test_losses.append(test_loss)
        test_accs.append(test_acc)

        print(f"Epoch {epoch}/{num_epochs} | "
              f"Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.4f} | "
              f"Test Loss: {test_loss:.4f} | Test Acc: {test_acc:.4f} | "
              f"Time: {time.time() - epoch_start_time:.2f}s")

    print("\n文本分类模型训练完成!")

    # 2.6 可视化训练过程
    print("\n--- 2.6 可视化训练过程 ---")
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    axes[0].plot(range(1, num_epochs + 1), train_losses, 'b-o', label='Train Loss')
    axes[0].plot(range(1, num_epochs + 1), test_losses, 'r-s', label='Test Loss')
    axes[0].set_xlabel('Epoch')
    axes[0].set_ylabel('Loss')
    axes[0].set_title('AG_NEWS Text Classification Loss Curve')
    axes[0].legend()
    axes[0].grid(True)

    axes[1].plot(range(1, num_epochs + 1), train_accs, 'b-o', label='Train Accuracy')
    axes[1].plot(range(1, num_epochs + 1), test_accs, 'r-s', label='Test Accuracy')
    axes[1].set_xlabel('Epoch')
    axes[1].set_ylabel('Accuracy')
    axes[1].set_title('AG_NEWS Text Classification Accuracy Curve')
    axes[1].legend()
    axes[1].grid(True)

    plt.tight_layout()
    plt.savefig("text_classification_curves.png", dpi=150)
    print("训练曲线已保存到 text_classification_curves.png")
    plt.close()

    # 2.7 测试模型预测
    print("\n--- 2.7 模型预测示例 ---")
    text_model.eval()

    test_sentences = [
        "The stock market rallied today as investors welcomed the new economic policy.",
        "The football team won the championship after a thrilling final match.",
        "Scientists discovered a new species of dinosaur in Argentina.",
        "The United Nations held an important meeting on climate change.",
    ]

    print("预测结果:")
    for sentence in test_sentences:
        tokens = vocab(tokenizer(sentence))
        tokens_tensor = torch.tensor(tokens, dtype=torch.int64).to(device)
        offsets_tensor = torch.tensor([0], dtype=torch.int64).to(device)
        with torch.no_grad():
            output = text_model(tokens_tensor, offsets_tensor)
            pred_label = output.argmax(1).item()
        pred_class = labels_map[pred_label + 1]
        print(f"  文本: {sentence[:60]}...")
        print(f"  预测类别: {pred_class}\n")

    # 保存模型
    text_model_path = "ag_news_text_model.pth"
    torch.save(text_model.state_dict(), text_model_path)
    print(f"文本分类模型已保存到 {text_model_path}")

except Exception as e:
    print(f"文本分类部分运行出错: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("实验2完成!")
print("=" * 70)