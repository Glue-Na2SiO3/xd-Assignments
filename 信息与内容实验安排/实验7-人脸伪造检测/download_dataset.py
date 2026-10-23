#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据集下载指引脚本
由于百度网盘需要手动下载，此脚本提供下载指引和数据集目录结构检查功能。
"""

import os
import sys


def print_guide():
    """打印数据集下载和准备指南"""
    guide = """
========================================================================
                    实验7 数据集下载指引
========================================================================

【下载地址】
  百度网盘: https://pan.baidu.com/s/1Zz6ZLQhv0_Eb4pGEtdqqbw
  提取码: 0gf4
  解压密码: xdce

【数据集信息】
  - 真实人脸 (Real): 1999 张
  - 伪造人脸 (Fake): 1999 张
  - 图像格式: JPG/PNG
  - 建议分辨率: 224x224 或更高

【目录结构要求】
  下载并解压后，请按以下结构组织数据集：

  face_dataset/
  ├── real/               <- 真实人脸图像 (1999张)
  │   ├── 00001.jpg
  │   ├── 00002.jpg
  │   └── ...
  └── fake/               <- 伪造人脸图像 (1999张)
      ├── 00001.jpg
      ├── 00002.jpg
      └── ...

  代码中默认的数据集路径为: ./face_dataset
  可通过 --data_root 参数修改路径。

【数据划分】
  训练集: 500张真实 + 500张虚假 = 1000张
  测试集: 其余 1499张真实 + 1499张虚假 = 2998张

【快速开始】
  1. 手动下载数据集并解压
  2. 将 real/ 和 fake/ 文件夹放入 face_dataset/ 目录
  3. 运行训练脚本:

     python exp7_face_forgery_detection.py --data_root ./face_dataset

【无数据集测试】
  如果暂时没有数据集，可以使用模拟数据模式测试代码:

     python exp7_face_forgery_detection.py --synthetic

  模拟数据模式会生成随机图像用于验证代码流程，
  但无法达到95%的准确率要求。

========================================================================
"""
    print(guide)


def check_dataset(data_root="./face_dataset"):
    """检查数据集目录结构"""
    print(f"\n[INFO] 检查数据集目录: {os.path.abspath(data_root)}")

    if not os.path.exists(data_root):
        print(f"[警告] 数据集目录不存在: {data_root}")
        print("[提示] 请按照上述指引下载并准备数据集。")
        return False

    real_dir = os.path.join(data_root, "real")
    fake_dir = os.path.join(data_root, "fake")

    real_count = 0
    fake_count = 0

    if os.path.exists(real_dir):
        real_count = len([f for f in os.listdir(real_dir)
                          if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.webp'))])
        print(f"[OK] 真实人脸目录存在: {real_dir} ({real_count} 张)")
    else:
        print(f"[错误] 真实人脸目录不存在: {real_dir}")

    if os.path.exists(fake_dir):
        fake_count = len([f for f in os.listdir(fake_dir)
                          if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.webp'))])
        print(f"[OK] 伪造人脸目录存在: {fake_dir} ({fake_count} 张)")
    else:
        print(f"[错误] 伪造人脸目录不存在: {fake_dir}")

    if real_count > 0 and fake_count > 0:
        print(f"\n[成功] 数据集检查通过！")
        print(f"  总计: {real_count + fake_count} 张图像")
        return True
    else:
        print(f"\n[失败] 数据集不完整，请检查目录结构。")
        return False


if __name__ == "__main__":
    print_guide()

    if len(sys.argv) > 1:
        data_path = sys.argv[1]
    else:
        data_path = "./face_dataset"

    check_dataset(data_path)
