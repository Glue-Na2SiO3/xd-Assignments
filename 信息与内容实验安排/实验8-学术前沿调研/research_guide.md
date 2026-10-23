# 实验8: 学术前沿调研指南

## 一、调研目标

调研信息与内容安全相关的前沿科技进展，选择一个具体方向进行深入研究，制作PPT汇报并撰写调研报告。

## 二、推荐调研方向

### 方向1: 深度伪造检测（Deepfake Detection）

**研究背景**：随着GAN和扩散模型的发展，合成视频/图像的质量越来越高，深度伪造检测成为多媒体安全的核心问题。

**推荐论文**：
1. Rossler A, et al. "FaceForensics++: Learning to Detect Manipulated Facial Images". ICCV 2019.
   - 代码：https://github.com/ondyari/FaceForensics
2. Dolhansky B, et al. "The DeepFake Detection Challenge (DFDC) Dataset". arXiv 2020.
   - 代码：https://github.com/facebookresearch/deepfake-detection-challenge
3. Zhao H, et al. "Multi-attentional Deepfake Detection". CVPR 2021.
   - 代码：https://github.com/yoctta/multiple-attention

**核心技术**：时空不一致性分析、频域特征、生物信号（心跳/眨眼）检测、多注意力机制

---

### 方向2: 可解释人工智能（XAI / Explainable AI）

**研究背景**：深度学习模型被视为"黑箱"，在安全关键领域（如内容审核、恶意软件检测）中，可解释性至关重要。

**推荐论文**：
1. Selvaraju R R, et al. "Grad-CAM: Visual Explanations from Deep Networks via Gradient-based Localization". ICCV 2017.
   - 代码：https://github.com/ramprs/grad-cam
2. Ribeiro M T, et al. "\"Why Should I Trust You?\": Explaining the Predictions of Any Classifier". KDD 2016.
   - 代码：https://github.com/marcotcr/lime
3. Lundberg S M, Lee S I. "A Unified Approach to Interpreting Model Predictions". NeurIPS 2017.
   - 代码：https://github.com/shap/shap

**核心技术**：梯度类方法（Grad-CAM）、基于扰动的方法（LIME）、Shapley值（SHAP）、概念激活向量（CAV）

---

### 方向3: 联邦学习安全（Federated Learning Security）

**研究背景**：联邦学习允许多方在不共享原始数据的前提下协作训练模型，但面临投毒攻击、梯度泄露、后门攻击等安全威胁。

**推荐论文**：
1. McMahan B, et al. "Communication-Efficient Learning of Deep Networks from Decentralized Data". AISTATS 2017.
   - 代码：https://github.com/google-research/federated
2. Bagdasaryan E, et al. "How To Backdoor Federated Learning". AISTATS 2020.
   - 代码：https://github.com/ebagdasa/backdoor_federated_learning
3. Nasr M, et al. "Comprehensive Privacy Analysis of Deep Learning". S&P 2019.

**核心技术**：安全聚合、差分隐私、拜占庭容错、梯度压缩、成员推理攻击防御

---

### 方向4: 视觉Transformer（Vision Transformer, ViT）

**研究背景**：Transformer架构在NLP领域取得巨大成功后，被引入计算机视觉领域，ViT及其变体在图像分类、检测等任务上展现出强大能力。

**推荐论文**：
1. Dosovitskiy A, et al. "An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale". ICLR 2021.
   - 代码：https://github.com/google-research/vision_transformer
2. Liu Z, et al. "Swin Transformer: Hierarchical Vision Transformer using Shifted Windows". ICCV 2021.
   - 代码：https://github.com/microsoft/Swin-Transformer
3. Touvron H, et al. "Training data-efficient image transformers & distillation through attention". ICML 2021.
   - 代码：https://github.com/facebookresearch/deit

**核心技术**：自注意力机制、补丁嵌入、位置编码、层次化特征、知识蒸馏

---

### 方向5: 扩散模型（Diffusion Models）

**研究背景**：扩散模型（如DDPM、Stable Diffusion）在图像生成领域超越了GAN，成为当前最热门的生成模型，同时也带来了新的内容安全挑战。

**推荐论文**：
1. Ho J, et al. "Denoising Diffusion Probabilistic Models". NeurIPS 2020.
   - 代码：https://github.com/hojonathanho/diffusion
2. Rombach R, et al. "High-Resolution Image Synthesis with Latent Diffusion Models". CVPR 2022.
   - 代码：https://github.com/CompVis/stable-diffusion
3. Saharia C, et al. "Photorealistic Text-to-Image Diffusion Models with Deep Language Understanding". NeurIPS 2022.
   - 代码：https://github.com/google-research/text-to-image-diffusion

**核心技术**：前向/反向扩散过程、U-Net噪声预测、条件生成、潜在空间扩散、文本引导生成

---

## 三、PPT制作指南

### 3.1 内容结构（8个部分）

| 页码 | 内容 | 建议页数 | 要点 |
|------|------|---------|------|
| 1 | 封面 | 1 | 标题、姓名、学号、日期 |
| 2 | 基本信息 | 1 | 调研方向、关键词、涉及领域 |
| 3 | 研究背景 | 1-2 | 问题来源、现实需求、技术发展历程 |
| 4 | 研究意义 | 1 | 学术价值、应用价值、社会影响 |
| 5 | 研究现状 | 2-3 | 时间线/分类梳理代表性工作 |
| 6 | 创新思路 | 1-2 | 核心创新点、与传统方法对比 |
| 7 | 核心技术 | 2-3 | 模型架构图、算法流程图、公式 |
| 8 | 实验效果 | 1-2 | 对比表格、性能曲线、可视化结果 |
| 9 | 总结展望 | 1 | 主要结论、局限、未来方向 |

### 3.2 设计规范

**文字要求**：
- 不得出现完整句子，以关键词、短语、 bullet points 为主
- 每页不超过6行文字
- 字号：标题32-40pt，正文24-28pt

**视觉要求**：
- 以图片、图表、架构图展示为主（占比70%以上）
- 使用高质量论文插图或自行绘制
- 配色简洁，避免超过3种主色

**推荐工具**：
- 绘图：draw.io, PowerPoint, Keynote
- 公式：LaTeX + MathType
- 配色：Color Hunt, Adobe Color

### 3.3 汇报技巧

- 准备讲稿，不是念PPT
- 重点讲解"为什么"和"怎么做"
- 控制时间：10-15分钟

---

## 四、调研报告模板

### 报告结构

```
1. 调研方向概述
   - 方向名称
   - 核心问题定义
   - 与信息与内容安全的关联

2. 研究背景与意义
   - 技术背景
   - 现实应用场景
   - 安全威胁分析

3. 研究现状综述
   - 按时间线或技术路线梳理
   - 代表性方法对比表格
   - 数据集与评价指标

4. 核心技术详解
   - 选择1-2篇代表性论文深入分析
   - 模型架构
   - 算法流程
   - 关键公式

5. 实验效果分析
   - 定量结果（表格）
   - 定性结果（可视化）
   - 优缺点分析

6. 总结与展望
   - 当前挑战
   - 未来研究方向
   - 个人思考

7. 参考文献
   - 至少10篇，包含近3年的顶会/顶刊论文
```

---

## 五、评分标准参考

| 评分项 | 占比 | 说明 |
|--------|------|------|
| 内容深度 | 30% | 对技术原理的理解是否准确深入 |
| 前沿性 | 20% | 选题是否紧跟学术前沿 |
| PPT质量 | 25% | 视觉效果、信息密度、无完整句子 |
| 汇报表达 | 15% | 逻辑清晰、时间控制、回答问题 |
| 报告规范 | 10% | 格式规范、参考文献完整 |
