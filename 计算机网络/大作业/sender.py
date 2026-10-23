import sys
import json
import socket
import random
import time
import crcmod
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QTextEdit, QTableWidget, QTableWidgetItem,
                             QHeaderView, QSpinBox, QSlider, QCheckBox, QLineEdit, QProgressBar)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QColor, QFont

# 全局配置
DEFAULT_RECV_IP = "127.0.0.1"
DEFAULT_RECV_PORT = 8888
DEFAULT_SEND_PORT = 9999
WINDOW_SIZE = 4
FRAME_CHAR_LEN = 3

# CRC计算函数 - 每次创建新的CRC对象
def calc_crc(data_str):
    """计算CRC-8校验值"""
    crc8 = crcmod.predefined.Crc('crc-8')
    crc8.update(data_str.encode('utf-8'))
    return format(crc8.crcValue, '02X').upper()

class FrameState:
    READY = "待发送"
    SENT = "已发送"
    ACKED = "已确认"
    LOST = "已丢失"
    CORRUPTED = "已损坏"
    MAX_RETRIES_EXCEEDED = "重传超限"

class SenderWindow(QMainWindow):
    log_signal = pyqtSignal(str, str)
    frame_update_signal = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("选择重发ARQ - 发送方（S）")
        self.setGeometry(100, 50, 1100, 700)
        self.setMaximumHeight(700)
        self.setStyleSheet("""
            QMainWindow { background-color: #f5f7fa; }
            QWidget { font-family: "Microsoft YaHei", sans-serif; font-size: 13px; }
            QPushButton { 
                background-color: #4285f4; color: white; border: none; border-radius: 4px; 
                padding: 6px 12px; font-size: 13px; 
            }
            QPushButton:hover { background-color: #3367d6; }
            QPushButton:disabled { background-color: #c9c9c9; }
            QTableWidget { 
                border: 1px solid #d0d0d0; border-radius: 4px; background-color: white;
                gridline-color: #e8eaed; min-height: 250px; max-height: 280px;
            }
            QHeaderView::section { 
                background-color: #e8eaed; border: none; padding: 6px; font-weight: bold; font-size: 12px;
            }
            QTextEdit, QLineEdit { 
                border: 1px solid #d0d0d0; border-radius: 4px; padding: 6px;
                background-color: white; font-size: 12px;
            }
            QSlider::groove:horizontal { height: 6px; background: #e8eaed; border-radius: 3px; }
            QSlider::handle:horizontal { width: 16px; background: #4285f4; border-radius: 8px; }
            QLabel { font-size: 13px; }
        """)

        self.recv_ip = DEFAULT_RECV_IP
        self.recv_port = DEFAULT_RECV_PORT
        self.send_port = DEFAULT_SEND_PORT
        self.upper_data = ""
        self.frame_list = []
        self.frame_cache = {}
        self.base_seq = 0
        self.next_seq = 0
        self.error_rate = 0.2
        self.sock = None
        self.is_running = False
        self.total_frames = 0
        self.ack_timer = None
        self.max_retries = 5  # 最大重传次数

        self.init_ui()
        self.log_signal.connect(self.add_log)
        self.frame_update_signal.connect(self.update_frame_table)

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # 顶部配置区
        config_layout = QHBoxLayout()
        config_layout.setSpacing(15)

        addr_layout = QVBoxLayout()
        addr_layout.setSpacing(8)
        addr_label = QLabel("接收方配置")
        addr_label.setFont(QFont("", 14, QFont.Weight.Bold))
        ip_port_layout = QHBoxLayout()
        ip_port_layout.addWidget(QLabel("IP:"))
        self.ip_edit = QLineEdit(DEFAULT_RECV_IP)
        self.ip_edit.setMaximumWidth(100)
        ip_port_layout.addWidget(self.ip_edit)
        ip_port_layout.addWidget(QLabel("端口:"))
        self.port_edit = QLineEdit(str(DEFAULT_RECV_PORT))
        self.port_edit.setMaximumWidth(70)
        ip_port_layout.addWidget(self.port_edit)
        addr_layout.addWidget(addr_label)
        addr_layout.addLayout(ip_port_layout)
        config_layout.addLayout(addr_layout)

        error_layout = QVBoxLayout()
        error_layout.setSpacing(8)
        error_label = QLabel("错误模拟")
        error_label.setFont(QFont("", 14, QFont.Weight.Bold))
        rate_layout = QHBoxLayout()
        rate_layout.addWidget(QLabel("错误率:"))
        self.error_slider = QSlider(Qt.Orientation.Horizontal)
        self.error_slider.setRange(0, 100)
        self.error_slider.setValue(int(self.error_rate * 100))
        self.error_slider.setMaximumWidth(100)
        self.error_label = QLabel(f"{int(self.error_rate * 100)}%")
        rate_layout.addWidget(self.error_slider)
        rate_layout.addWidget(self.error_label)
        error_type_layout = QHBoxLayout()
        error_type_layout.setSpacing(8)
        self.lost_check = QCheckBox("帧丢失")
        self.corrupt_check = QCheckBox("帧损坏")
        self.ack_lost_check = QCheckBox("ACK丢失")
        self.ack_corrupt_check = QCheckBox("ACK损坏")
        self.lost_check.setChecked(True)
        self.corrupt_check.setChecked(True)
        self.ack_lost_check.setChecked(True)
        self.ack_corrupt_check.setChecked(True)
        error_type_layout.addWidget(self.lost_check)
        error_type_layout.addWidget(self.corrupt_check)
        error_type_layout.addWidget(self.ack_lost_check)
        error_type_layout.addWidget(self.ack_corrupt_check)
        error_layout.addWidget(error_label)
        error_layout.addLayout(rate_layout)
        error_layout.addLayout(error_type_layout)
        config_layout.addLayout(error_layout)

        timeout_layout = QVBoxLayout()
        timeout_layout.setSpacing(8)
        timeout_label = QLabel("超时配置")
        timeout_label.setFont(QFont("", 14, QFont.Weight.Bold))
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(1, 10)
        self.timeout_spin.setValue(3)
        self.timeout_spin.setSuffix("s")
        self.timeout_spin.setMaximumWidth(60)
        timeout_layout.addWidget(timeout_label)
        timeout_layout.addWidget(self.timeout_spin)
        config_layout.addLayout(timeout_layout)

        main_layout.addLayout(config_layout)
        self.error_slider.valueChanged.connect(lambda x: self.error_label.setText(f"{x}%"))

        # 上层数据输入区
        upper_layout = QVBoxLayout()
        upper_layout.setSpacing(8)
        upper_label = QLabel("上层数据输入")
        upper_label.setFont(QFont("", 14, QFont.Weight.Bold))
        self.upper_edit = QTextEdit()
        self.upper_edit.setPlaceholderText("请输入要发送的上层数据（自动按字符分割为多帧）...")
        self.upper_edit.setMaximumHeight(80)
        self.confirm_upper_btn = QPushButton("确认上层数据")
        self.confirm_upper_btn.clicked.connect(self.confirm_upper_data)
        self.confirm_upper_btn.setMaximumWidth(120)
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.confirm_upper_btn)
        upper_layout.addWidget(upper_label)
        upper_layout.addWidget(self.upper_edit)
        upper_layout.addLayout(btn_layout)
        main_layout.addLayout(upper_layout)

        # 成帧动画区
        frame_anim_layout = QVBoxLayout()
        frame_anim_layout.setSpacing(8)
        frame_anim_label = QLabel("成帧过程可视化")
        frame_anim_label.setFont(QFont("", 14, QFont.Weight.Bold))
        step_progress_layout = QHBoxLayout()
        self.step_labels = [QLabel("分割"), QLabel("加序号"), QLabel("CRC校验"), QLabel("完成")]
        for label in self.step_labels:
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("font-size: 12px; color: #666;")
            step_progress_layout.addWidget(label)
        self.frame_progress = QProgressBar()
        self.frame_progress.setRange(0, 4)
        self.frame_progress.setValue(0)
        self.frame_progress.setMaximumHeight(12)
        self.frame_preview_label = QLabel("帧预览：无")
        self.frame_preview_label.setStyleSheet("background-color: white; padding: 6px; border-radius: 4px; font-size: 12px;")
        self.assemble_frame_btn = QPushButton("组装帧")
        self.assemble_frame_btn.clicked.connect(self.assemble_frame_anim)
        self.assemble_frame_btn.setEnabled(False)
        self.assemble_frame_btn.setMaximumWidth(100)
        assemble_btn_layout = QHBoxLayout()
        assemble_btn_layout.addStretch()
        assemble_btn_layout.addWidget(self.assemble_frame_btn)
        frame_anim_layout.addWidget(frame_anim_label)
        frame_anim_layout.addLayout(step_progress_layout)
        frame_anim_layout.addWidget(self.frame_progress)
        frame_anim_layout.addWidget(self.frame_preview_label)
        frame_anim_layout.addLayout(assemble_btn_layout)
        main_layout.addLayout(frame_anim_layout)

        # 帧缓存表格区
        cache_layout = QVBoxLayout()
        cache_layout.setSpacing(8)
        self.cache_label = QLabel(f"帧缓存（滑动窗口：[{self.base_seq}, {self.base_seq + WINDOW_SIZE - 1}]）")
        self.cache_label.setFont(QFont("", 14, QFont.Weight.Bold))
        self.frame_table = QTableWidget()
        self.frame_table.setColumnCount(6)
        self.frame_table.setHorizontalHeaderLabels(["序号", "数据", "状态", "定时器", "发送时间", "操作"])
        self.frame_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.frame_table.setMinimumHeight(250)
        self.frame_table.setMaximumHeight(280)
        cache_layout.addWidget(self.cache_label)
        cache_layout.addWidget(self.frame_table)
        main_layout.addLayout(cache_layout)

        # 控制按钮区
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        self.send_window_btn = QPushButton("发送窗口内帧")
        self.send_window_btn.clicked.connect(self.send_window_frames)
        self.send_window_btn.setEnabled(False)
        self.stop_timer_btn = QPushButton("停止选中帧定时器")
        self.stop_timer_btn.clicked.connect(self.stop_selected_timer)
        self.delete_acked_btn = QPushButton("删除已确认帧")
        self.delete_acked_btn.clicked.connect(self.delete_acked_frames)
        self.clear_cache_btn = QPushButton("清空缓存")
        self.clear_cache_btn.clicked.connect(self.clear_cache)
        self.exit_btn = QPushButton("退出")
        self.exit_btn.clicked.connect(self.close)
        for btn in [self.send_window_btn, self.stop_timer_btn, self.delete_acked_btn, self.clear_cache_btn, self.exit_btn]:
            btn.setMaximumHeight(30)
        btn_layout.addWidget(self.send_window_btn)
        btn_layout.addWidget(self.stop_timer_btn)
        btn_layout.addWidget(self.delete_acked_btn)
        btn_layout.addWidget(self.clear_cache_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.exit_btn)
        main_layout.addLayout(btn_layout)

        # 日志区
        log_layout = QVBoxLayout()
        log_layout.setSpacing(8)
        log_label = QLabel("运行日志")
        log_label.setFont(QFont("", 14, QFont.Weight.Bold))
        self.log_edit = QTextEdit()
        self.log_edit.setReadOnly(True)
        self.log_edit.setMaximumHeight(120)
        log_layout.addWidget(log_label)
        log_layout.addWidget(self.log_edit)
        main_layout.addLayout(log_layout)

    def add_log(self, content, log_type="info"):
        timestamp = time.strftime("%H:%M:%S", time.localtime())
        color_map = {
            "info": "#202124",
            "warn": "#f4b400",
            "error": "#d93025",
            "success": "#0f9d58"
        }
        self.log_edit.append(f'<span style="color:{color_map.get(log_type, "#202124")}">[{timestamp}] {content}</span>')
        self.log_edit.verticalScrollBar().setValue(self.log_edit.verticalScrollBar().maximum())

    def confirm_upper_data(self):
        self.upper_data = self.upper_edit.toPlainText().strip()
        if not self.upper_data:
            self.log_signal.emit("上层数据不能为空！", "error")
            return
        
        # 按字符分割
        self.frame_list = [self.upper_data[i:i+FRAME_CHAR_LEN] 
                          for i in range(0, len(self.upper_data), FRAME_CHAR_LEN)]
        self.total_frames = len(self.frame_list)
        
        self.log_signal.emit(f"上层数据确认成功，分割为{len(self.frame_list)}帧（每帧最大{FRAME_CHAR_LEN}个字符）", "success")
        self.assemble_frame_btn.setEnabled(True)
        self.send_window_btn.setEnabled(True)
        
        if not self.sock:
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                self.sock.bind(("", self.send_port))
                self.sock.setblocking(False)
                self.ack_timer = QTimer()
                self.ack_timer.timeout.connect(self.receive_ack)
                self.ack_timer.start(100)
                self.is_running = True
                self.log_signal.emit(f"UDP Socket启动成功，绑定端口{self.send_port}", "success")
            except Exception as e:
                self.log_signal.emit(f"Socket启动失败：{str(e)}", "error")

    def assemble_frame_anim(self):
        self.assemble_frame_btn.setEnabled(False)
        self.frame_progress.setValue(0)
        for label in self.step_labels:
            label.setStyleSheet("font-size: 12px; color: #666;")
        
        QTimer.singleShot(300, lambda: self.update_anim_step(0, "数据分割完成"))
        QTimer.singleShot(600, lambda: self.update_anim_step(1, "帧序号添加完成"))
        QTimer.singleShot(900, lambda: self.update_anim_step(2, "CRC校验计算完成"))
        QTimer.singleShot(1200, self.finish_assemble_frame)

    def update_anim_step(self, step_idx, msg):
        self.step_labels[step_idx].setStyleSheet("font-size: 12px; color: #4285f4; font-weight: bold;")
        self.frame_progress.setValue(step_idx + 1)
        self.log_signal.emit(msg, "info")

    def finish_assemble_frame(self):
        self.step_labels[3].setStyleSheet("font-size: 12px; color: #0f9d58; font-weight: bold;")
        self.frame_progress.setValue(4)
        
        for seq_no, data in enumerate(self.frame_list):
            # 计算CRC
            crc = calc_crc(f"{seq_no}|{data}")
            frame = {
                "seq_no": seq_no,
                "data": data,
                "crc": crc
            }
            self.frame_cache[seq_no] = {
                "frame": frame,
                "timer": None,
                "state": FrameState.READY,
                "send_time": "",
                "retry_count": 0
            }
        
        if self.frame_cache:
            first_frame = self.frame_cache[0]["frame"]
            self.frame_preview_label.setText(f"帧预览：seq={first_frame['seq_no']}, data={first_frame['data']}")
        
        self.log_signal.emit(f"所有{len(self.frame_cache)}帧组装完成，已添加到缓存", "success")
        self.assemble_frame_btn.setEnabled(True)
        self.frame_update_signal.emit()

    def send_window_frames(self):
        self.recv_ip = self.ip_edit.text().strip() or DEFAULT_RECV_IP
        try:
            self.recv_port = int(self.port_edit.text().strip())
        except ValueError:
            self.recv_port = DEFAULT_RECV_PORT
            self.log_signal.emit(f"端口无效，使用默认端口{DEFAULT_RECV_PORT}", "warn")
        
        window_end = self.base_seq + WINDOW_SIZE - 1
        self.log_signal.emit(f"开始发送窗口内帧（窗口：[{self.base_seq}, {window_end}]）", "info")
        
        # 发送窗口内状态为READY的帧
        sent_count = 0
        for seq_no in range(self.base_seq, min(window_end + 1, len(self.frame_cache))):
            frame_info = self.frame_cache.get(seq_no)
            if frame_info and frame_info["state"] == FrameState.READY:
                self.send_single_frame(seq_no)
                sent_count += 1
        
        if sent_count > 0:
            self.frame_update_signal.emit()
        else:
            self.log_signal.emit("窗口内没有可发送的帧", "info")

    def send_single_frame(self, seq_no):
        frame_info = self.frame_cache.get(seq_no)
        if not frame_info:
            return
        
        frame = frame_info["frame"].copy()  # 复制一份，避免修改原始数据
        original_data = frame["data"]
        
        # 更新错误率
        self.error_rate = self.error_slider.value() / 100
        
        # 检查是否模拟丢失
        if self.lost_check.isChecked() and random.random() < self.error_rate:
            frame_info["state"] = FrameState.LOST
            frame_info["retry_count"] += 1
            self.log_signal.emit(f"帧{seq_no}：模拟丢失（重传次数：{frame_info['retry_count']}）", "warn")
            self.start_frame_timer(seq_no)
            return
        
        # 检查是否模拟损坏
        if self.corrupt_check.isChecked() and random.random() < self.error_rate:
            # 创建损坏的帧：修改数据但保持CRC不变（这样接收方CRC校验会失败）
            corrupted_data = original_data + "X"  # 简单修改数据
            frame["data"] = corrupted_data  # 修改数据但不修改CRC
            frame_info["state"] = FrameState.CORRUPTED
            frame_info["retry_count"] += 1
            self.log_signal.emit(f"帧{seq_no}：模拟损坏（数据：{corrupted_data}）", "warn")
        else:
            frame_info["state"] = FrameState.SENT
            frame_info["send_time"] = time.strftime("%H:%M:%S", time.localtime())
        
        try:
            frame_str = json.dumps(frame, ensure_ascii=False)
            self.sock.sendto(frame_str.encode("utf-8"), (self.recv_ip, self.recv_port))
            
            if frame_info["state"] == FrameState.SENT:
                self.log_signal.emit(f"帧{seq_no}：发送成功（数据：{original_data}）", "success")
            elif frame_info["state"] == FrameState.CORRUPTED:
                self.log_signal.emit(f"帧{seq_no}：发送损坏帧（原始：{original_data}，发送：{corrupted_data}）", "warn")
                
            # 启动定时器
            self.start_frame_timer(seq_no)
            
        except Exception as e:
            self.log_signal.emit(f"帧{seq_no}：发送失败：{str(e)}", "error")
            frame_info["state"] = FrameState.READY

    def start_frame_timer(self, seq_no):
        frame_info = self.frame_cache.get(seq_no)
        if not frame_info:
            return
        
        # 停止现有的定时器
        if frame_info["timer"]:
            frame_info["timer"].stop()
        
        # 创建新定时器
        frame_info["timer"] = QTimer()
        frame_info["timer"].timeout.connect(lambda s=seq_no: self.frame_timeout(s))
        frame_info["timer"].start(self.timeout_spin.value() * 1000)

    def frame_timeout(self, seq_no):
        frame_info = self.frame_cache.get(seq_no)
        if not frame_info or frame_info["state"] == FrameState.ACKED:
            return
        
        # 检查重传次数
        if frame_info.get("retry_count", 0) >= self.max_retries:
            self.log_signal.emit(f"帧{seq_no}：重传次数超过{self.max_retries}次，停止重传", "error")
            frame_info["state"] = FrameState.MAX_RETRIES_EXCEEDED
            if frame_info["timer"]:
                frame_info["timer"].stop()
                frame_info["timer"] = None
            self.frame_update_signal.emit()
            return
        
        retry_count = frame_info.get("retry_count", 0) + 1
        self.log_signal.emit(f"帧{seq_no}：超时未收到ACK，第{retry_count}次重发", "warn")
        frame_info["state"] = FrameState.READY
        
        if frame_info["timer"]:
            frame_info["timer"].stop()
            frame_info["timer"] = None
        
        # 添加延迟避免网络拥塞（重传次数越多，延迟越长）
        delay = 100 * frame_info.get("retry_count", 0)
        QTimer.singleShot(delay, lambda s=seq_no: self.send_single_frame(s))

    def receive_ack(self):
        if not self.is_running or not self.sock:
            return
        
        try:
            data, addr = self.sock.recvfrom(1024)
            ack_str = data.decode("utf-8", errors='ignore')
            
            try:
                ack = json.loads(ack_str)
                if not isinstance(ack, dict) or "type" not in ack or "seq_no" not in ack or "crc" not in ack:
                    return
                
                ack_type = ack["type"]
                seq_no = ack["seq_no"]
                recv_crc = ack["crc"]
                
            except json.JSONDecodeError:
                # 可能是损坏的ACK，直接忽略
                return
            
            # 验证CRC
            crc_data = f"{ack_type}:{seq_no}"
            calc_crc_value = calc_crc(crc_data)
            
            if recv_crc != calc_crc_value:
                # CRC校验失败，可能是损坏的ACK
                self.log_signal.emit(f"收到损坏的{ack_type}：seq_no={seq_no}", "warn")
                return
            
            self.log_signal.emit(f"收到有效{ack_type}：seq_no={seq_no}", "success")
            
            if ack_type == "ACK":
                # 累积ACK：确认所有小于seq_no的帧
                acked_frames = 0
                for s in list(self.frame_cache.keys()):
                    if s < seq_no:
                        frame_info = self.frame_cache.get(s)
                        if frame_info and frame_info["state"] != FrameState.ACKED:
                            frame_info["state"] = FrameState.ACKED
                            if frame_info["timer"]:
                                frame_info["timer"].stop()
                                frame_info["timer"] = None
                            acked_frames += 1
                
                if seq_no > self.base_seq:
                    old_base = self.base_seq
                    self.base_seq = seq_no
                    window_end = self.base_seq + WINDOW_SIZE - 1
                    self.cache_label.setText(f"帧缓存（滑动窗口：[{self.base_seq}, {window_end}]）")
                    self.log_signal.emit(f"滑动窗口更新：{old_base} -> {self.base_seq}，确认了{acked_frames}帧", "info")
            
            elif ack_type == "NAK":
                # NAK：重传指定的帧
                frame_info = self.frame_cache.get(seq_no)
                if frame_info and frame_info["state"] != FrameState.ACKED:
                    frame_info["state"] = FrameState.READY
                    if frame_info["timer"]:
                        frame_info["timer"].stop()
                        frame_info["timer"] = None
                    self.log_signal.emit(f"收到NAK，准备重发帧{seq_no}", "warn")
                    self.send_single_frame(seq_no)
            
            self.frame_update_signal.emit()
            
        except BlockingIOError:
            pass
        except Exception as e:
            self.log_signal.emit(f"接收应答错误：{str(e)}", "error")

    def stop_selected_timer(self):
        selected_items = self.frame_table.selectedItems()
        if not selected_items:
            self.log_signal.emit("请选中要停止定时器的帧", "error")
            return
        
        row = selected_items[0].row()
        seq_no_item = self.frame_table.item(row, 0)
        if not seq_no_item or not seq_no_item.text().isdigit():
            self.log_signal.emit("选中行无有效帧序号", "error")
            return
        
        seq_no = int(seq_no_item.text())
        frame_info = self.frame_cache.get(seq_no)
        if not frame_info or not frame_info["timer"]:
            self.log_signal.emit(f"帧{seq_no}无运行中的定时器", "error")
            return
        
        frame_info["timer"].stop()
        frame_info["timer"] = None
        self.log_signal.emit(f"帧{seq_no}定时器已停止", "success")
        self.frame_update_signal.emit()

    def delete_acked_frames(self):
        acked_seqs = [s for s, info in self.frame_cache.items() if info["state"] == FrameState.ACKED]
        if not acked_seqs:
            self.log_signal.emit("无已确认的帧可删除", "info")
            return
        
        for seq_no in acked_seqs:
            frame_info = self.frame_cache[seq_no]
            if frame_info["timer"]:
                frame_info["timer"].stop()
            del self.frame_cache[seq_no]
        
        self.log_signal.emit(f"已删除{len(acked_seqs)}个已确认帧", "success")
        self.frame_update_signal.emit()

    def clear_cache(self):
        for info in self.frame_cache.values():
            if info["timer"]:
                info["timer"].stop()
        
        self.frame_cache.clear()
        self.frame_list = []
        self.base_seq = 0
        self.next_seq = 0
        self.total_frames = 0
        
        self.frame_progress.setValue(0)
        self.frame_preview_label.setText("帧预览：无")
        
        for label in self.step_labels:
            label.setStyleSheet("font-size: 12px; color: #666;")
        
        self.cache_label.setText(f"帧缓存（滑动窗口：[{self.base_seq}, {self.base_seq + WINDOW_SIZE - 1}]）")
        self.log_signal.emit("帧缓存已清空", "success")
        self.frame_update_signal.emit()

    def update_frame_table(self):
        self.frame_table.setRowCount(0)
        sorted_seqs = sorted(self.frame_cache.keys())
        
        for idx, seq_no in enumerate(sorted_seqs):
            info = self.frame_cache[seq_no]
            frame = info["frame"]
            row = self.frame_table.rowCount()
            self.frame_table.insertRow(row)
            
            self.frame_table.setItem(row, 0, QTableWidgetItem(str(seq_no)))
            self.frame_table.setItem(row, 1, QTableWidgetItem(frame["data"]))
            
            state_item = QTableWidgetItem(info["state"])
            color_map = {
                FrameState.READY: QColor(234, 234, 234),
                FrameState.SENT: QColor(251, 243, 219),
                FrameState.ACKED: QColor(219, 243, 219),
                FrameState.LOST: QColor(243, 219, 219),
                FrameState.CORRUPTED: QColor(243, 219, 234),
                FrameState.MAX_RETRIES_EXCEEDED: QColor(255, 100, 100)
            }
            state_item.setBackground(color_map.get(info["state"], QColor(255, 255, 255)))
            self.frame_table.setItem(row, 2, state_item)
            
            timer_state = "运行中" if info["timer"] and info["timer"].isActive() else "已停止"
            self.frame_table.setItem(row, 3, QTableWidgetItem(timer_state))
            
            self.frame_table.setItem(row, 4, QTableWidgetItem(info["send_time"]))
            
            stop_btn = QPushButton("停止")
            stop_btn.setMaximumWidth(50)
            stop_btn.clicked.connect(lambda _, s=seq_no: self.stop_timer_by_seq(s))
            self.frame_table.setCellWidget(row, 5, stop_btn)
        
        # 高亮窗口内的帧
        window_end = self.base_seq + WINDOW_SIZE - 1
        for row in range(self.frame_table.rowCount()):
            seq_no_item = self.frame_table.item(row, 0)
            if not seq_no_item:
                continue
            
            seq_no = int(seq_no_item.text())
            if self.base_seq <= seq_no <= window_end:
                for col in range(5):
                    item = self.frame_table.item(row, col)
                    if item:
                        item.setFont(QFont("", 13, QFont.Weight.Bold))

    def stop_timer_by_seq(self, seq_no):
        frame_info = self.frame_cache.get(seq_no)
        if not frame_info or not frame_info["timer"]:
            self.log_signal.emit(f"帧{seq_no}无运行中的定时器", "error")
            return
        
        frame_info["timer"].stop()
        frame_info["timer"] = None
        self.log_signal.emit(f"帧{seq_no}定时器已停止", "success")
        self.frame_update_signal.emit()

    def closeEvent(self, event):
        self.is_running = False
        
        if self.ack_timer:
            self.ack_timer.stop()
        
        for info in self.frame_cache.values():
            if info["timer"]:
                info["timer"].stop()
        
        if self.sock:
            self.sock.close()
        
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SenderWindow()
    window.show()
    sys.exit(app.exec())