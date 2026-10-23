# 信息与内容安全实验

本目录包含西安电子科技大学网络与信息安全学院《信息与内容安全》课程的8次实验内容。

## 实验列表

| 实验 | 名称 | 框架 | 内容 |
|------|------|------|------|
| 实验1 | PyTorch基础 | PyTorch | 张量、数据加载、自动微分、神经网络 |
| 实验2 | PyTorch进阶 | PyTorch | 目标检测、文本分类 |
| 实验3 | TensorFlow基础 | TensorFlow | Keras快速入门、自定义训练 |
| 实验4 | TensorFlow进阶-Vision | TensorFlow | 图像分类、迁移学习、数据增强 |
| 实验5 | TensorFlow进阶-Generative | TensorFlow | CycleGAN、DeepDream、扩散模型 |
| 实验6 | 图像伪造实验 | TensorFlow | 风格迁移、图像生成、图像外推 |
| 实验7 | 人脸伪造检测 | PyTorch | 二分类器训练（准确率95%+） |
| 实验8 | 学术前沿调研 | - | 前沿技术调研与PPT汇报 |

## 环境要求

- Python 3.8+
- 无NVIDIA显卡也可运行（所有代码已设置为CPU模式）
- 部分实验需要网络连接下载预训练模型和数据集

## 快速开始

### 1. 激活Conda环境（推荐）
```bash
conda activate py311ml
```

### 2. 安装依赖
进入任意实验目录，安装所需依赖：
```bash
cd 实验1-PyTorch基础
pip install -r requirements.txt
```

### 3. 运行实验
```bash
python pytorch_basics.py
```

### 4. 查看报告
打开对应目录下的 `实验X报告.docx`，填写个人信息后提交。

## 目录结构

```
信息与内容实验安排/
├── 实验1-PyTorch基础/
│   ├── pytorch_basics.py
│   ├── requirements.txt
│   ├── README.md
│   └── 实验1报告.docx
├── 实验2-PyTorch进阶/
│   ├── pytorch_advanced.py
│   ├── requirements.txt
│   ├── README.md
│   └── 实验2报告.docx
├── 实验3-TensorFlow基础/
│   ├── tensorflow_basics.py
│   ├── requirements.txt
│   ├── README.md
│   └── 实验3报告.docx
├── 实验4-TensorFlow进阶-Vision/
│   ├── tensorflow_vision.py
│   ├── requirements.txt
│   ├── README.md
│   └── 实验4报告.docx
├── 实验5-TensorFlow进阶-Generative/
│   ├── tensorflow_generative.py
│   ├── requirements.txt
│   ├── README.md
│   └── 实验5报告.docx
├── 实验6-图像伪造实验/
│   ├── image_forgery.py
│   ├── requirements.txt
│   ├── README.md
│   └── 实验6报告.docx
├── 实验7-人脸伪造检测/
│   ├── face_forgery_detection.py
│   ├── download_dataset.py
│   ├── requirements.txt
│   ├── README.md
│   └── 实验7报告.docx
├── 实验8-学术前沿调研/
│   ├── research_survey.md
│   ├── requirements.txt
│   ├── README.md
│   └── 实验8报告.docx
├── 1. 实验安排-8次-2026.pptx
├── 信息与内容安全实验报告模板-2026.docx
└── README.md
```

## 注意事项

1. **数据集下载**
   - 实验7需要从百度网盘下载数据集
   - 部分实验首次运行会自动下载数据集（MNIST、CIFAR-10、FashionMNIST等）

2. **模型下载**
   - 实验2、4、5、6需要下载预训练模型
   - 确保网络连接畅通

3. **运行时间**
   - 实验1-6单次运行约5-15分钟
   - 实验7训练约30-60分钟
   - 实验8为调研任务，无代码运行

4. **报告提交**
   - 电子版（PDF格式）命名：姓名+学号+信息与内容安全实验X
   - 提交至学在西电作业中

## 参考资料

- PyTorch官方教程：https://docs.pytorch.org/tutorials/
- TensorFlow官方教程：https://www.tensorflow.org/tutorials
- 实验安排PPT：`1. 实验安排-8次-2026.pptx`
- 报告模板：`信息与内容安全实验报告模板-2026.docx`

## 联系方式

- 指导教师：彭春蕾
- 邮箱：clpeng@xidian.edu.cn
- 学院：网络与信息安全学院
