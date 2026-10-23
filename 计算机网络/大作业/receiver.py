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

DEFAULT_RECV_PORT = 8888
DEFAULT_SEND_IP = "127.0.0.1"
DEFAULT_SEND_PORT = 9999
WINDOW_SIZE = 4

# CRC计算函数 - 每次创建新的CRC对象
def calc_crc(data_str):
    """计算CRC-8校验值"""
    crc8 = crcmod.predefined.Crc('crc-8')
    crc8.update(data_str.encode('utf-8'))
    return format(crc8.crcValue, '02X').upper()

class FrameState:
    RECEIVED = "已接收"
    CRC_PASS = "CRC通过"
    CRC_FAIL = "CRC失败"
    OUT_OF_ORDER = "失序"
    DELIVERED = "已交付"

class ReceiverWindow(QMainWindow):
    log_signal = pyqtSignal(str, str)
    frame_update_signal = pyqtSignal()
    deliver_signal = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("选择重发ARQ - 接收方（R）")
        self.setGeometry(200, 50, 1100, 700)
        self.setMaximumHeight(700)
        self.setStyleSheet("""
            QMainWindow { background-color: #f5f7fa; }
            QWidget { font-family: "Microsoft YaHei", sans-serif; font-size: 13px; }
            QPushButton { 
                background-color: #0f9d58; color: white; border: none; border-radius: 4px; 
                padding: 6px 12px; font-size: 13px; 
            }
            QPushButton:hover { background-color: #0b7d4b; }
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
            QSlider::handle:horizontal { width: 16px; background: #0f9d58; border-radius: 8px; }
            QLabel { font-size: 13px; }
        """)

        self.recv_port = DEFAULT_RECV_PORT
        self.send_ip = DEFAULT_SEND_IP
        self.send_port = DEFAULT_SEND_PORT
        self.exp_seq = 0
        self.received_frames = {}
        self.error_rate = 0.2
        self.sock = None
        self.is_listening = False
        self.delivered_count = 0
        self.recv_timer = None
        self.nak_requests = {}  # 记录NAK请求时间，避免频繁发送

        self.init_ui()
        self.log_signal.connect(self.add_log)
        self.frame_update_signal.connect(self.update_frame_table)
        self.deliver_signal.connect(self.auto_deliver_to_upper)
        
        # 清理旧的NAK请求记录
        self.nak_cleanup_timer = QTimer()
        self.nak_cleanup_timer.timeout.connect(self.cleanup_old_nak_requests)
        self.nak_cleanup_timer.start(30000)  # 30秒清理一次

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(20, 20, 20, 20)

        config_layout = QHBoxLayout()
        config_layout.setSpacing(15)

        listen_layout = QVBoxLayout()
        listen_layout.setSpacing(8)
        listen_label = QLabel("监听配置")
        listen_label.setFont(QFont("", 14, QFont.Weight.Bold))
        port_layout = QHBoxLayout()
        port_layout.addWidget(QLabel("端口:"))
        self.port_edit = QLineEdit(str(DEFAULT_RECV_PORT))
        self.port_edit.setMaximumWidth(70)
        port_layout.addWidget(self.port_edit)
        listen_layout.addWidget(listen_label)
        listen_layout.addLayout(port_layout)
        config_layout.addLayout(listen_layout)

        send_addr_layout = QVBoxLayout()
        send_addr_layout.setSpacing(8)
        send_addr_label = QLabel("发送方配置")
        send_addr_label.setFont(QFont("", 14, QFont.Weight.Bold))
        ip_port_layout = QHBoxLayout()
        ip_port_layout.addWidget(QLabel("IP:"))
        self.ip_edit = QLineEdit(DEFAULT_SEND_IP)
        self.ip_edit.setMaximumWidth(100)
        ip_port_layout.addWidget(self.ip_edit)
        ip_port_layout.addWidget(QLabel("端口:"))
        self.send_port_edit = QLineEdit(str(DEFAULT_SEND_PORT))
        self.send_port_edit.setMaximumWidth(70)
        ip_port_layout.addWidget(self.send_port_edit)
        send_addr_layout.addWidget(send_addr_label)
        send_addr_layout.addLayout(ip_port_layout)
        config_layout.addLayout(send_addr_layout)

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
        self.ack_lost_check = QCheckBox("ACK丢失")
        self.ack_corrupt_check = QCheckBox("ACK损坏")
        self.ack_lost_check.setChecked(True)
        self.ack_corrupt_check.setChecked(True)
        error_type_layout.addWidget(self.ack_lost_check)
        error_type_layout.addWidget(self.ack_corrupt_check)
        error_layout.addWidget(error_label)
        error_layout.addLayout(rate_layout)
        error_layout.addLayout(error_type_layout)
        config_layout.addLayout(error_layout)

        main_layout.addLayout(config_layout)
        self.error_slider.valueChanged.connect(lambda x: self.error_label.setText(f"{x}%"))

        # 状态显示区
        status_layout = QHBoxLayout()
        status_layout.setSpacing(15)
        self.exp_seq_label = QLabel(f"期望接收序号：<span style='color:#d93025; font-size:14px; font-weight:bold'>{self.exp_seq}</span>")
        self.recv_count_label = QLabel(f"已接收帧数：0")
        self.delivered_count_label = QLabel(f"已交付帧数：0")
        status_layout.addWidget(self.exp_seq_label)
        status_layout.addWidget(self.recv_count_label)
        status_layout.addWidget(self.delivered_count_label)
        status_layout.addStretch()
        main_layout.addLayout(status_layout)

        # ACK控制区
        ack_layout = QHBoxLayout()
        ack_layout.setSpacing(15)
        self.send_ack_btn = QPushButton("发送ACK")
        self.send_ack_btn.clicked.connect(lambda: self.send_ack_nak("ACK", self.exp_seq))
        self.send_nak_btn = QPushButton("发送NAK")
        self.send_nak_btn.clicked.connect(lambda: self.send_ack_nak("NAK", self.exp_seq))
        self.send_ack_btn.setEnabled(False)
        self.send_nak_btn.setEnabled(False)
        self.send_ack_btn.setMaximumWidth(80)
        self.send_nak_btn.setMaximumWidth(80)
        ack_layout.addStretch()
        ack_layout.addWidget(self.send_ack_btn)
        ack_layout.addWidget(self.send_nak_btn)
        main_layout.addLayout(ack_layout)

        # 接收帧表格
        frame_layout = QVBoxLayout()
        frame_layout.setSpacing(8)
        frame_label = QLabel("接收帧记录")
        frame_label.setFont(QFont("", 14, QFont.Weight.Bold))
        self.frame_table = QTableWidget()
        self.frame_table.setColumnCount(7)
        self.frame_table.setHorizontalHeaderLabels(["序号", "数据", "CRC状态", "接收时间", "处理状态", "重传次数", "操作"])
        self.frame_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.frame_table.setMinimumHeight(250)
        self.frame_table.setMaximumHeight(280)
        frame_layout.addWidget(frame_label)
        frame_layout.addWidget(self.frame_table)
        main_layout.addLayout(frame_layout)

        # 交付数据区
        deliver_layout = QVBoxLayout()
        deliver_layout.setSpacing(8)
        deliver_label = QLabel("上层交付数据")
        deliver_label.setFont(QFont("", 14, QFont.Weight.Bold))
        self.deliver_edit = QTextEdit()
        self.deliver_edit.setReadOnly(True)
        self.deliver_edit.setPlaceholderText("已交付上层的数据将显示在这里...")
        self.deliver_edit.setMaximumHeight(80)
        self.batch_deliver_btn = QPushButton("手动交付上层")
        self.batch_deliver_btn.clicked.connect(self.manual_batch_deliver)
        self.batch_deliver_btn.setEnabled(False)
        self.batch_deliver_btn.setMaximumWidth(120)
        deliver_btn_layout = QHBoxLayout()
        deliver_btn_layout.addStretch()
        deliver_btn_layout.addWidget(self.batch_deliver_btn)
        deliver_layout.addWidget(deliver_label)
        deliver_layout.addWidget(self.deliver_edit)
        deliver_layout.addLayout(deliver_btn_layout)
        main_layout.addLayout(deliver_layout)

        # 控制按钮区
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        self.start_listen_btn = QPushButton("开始监听")
        self.start_listen_btn.clicked.connect(self.start_listen)
        self.stop_listen_btn = QPushButton("停止监听")
        self.stop_listen_btn.clicked.connect(self.stop_listen)
        self.stop_listen_btn.setEnabled(False)
        self.clear_frame_btn = QPushButton("清空接收记录")
        self.clear_frame_btn.clicked.connect(self.clear_frame_records)
        self.exit_btn = QPushButton("退出")
        self.exit_btn.clicked.connect(self.close)
        for btn in [self.start_listen_btn, self.stop_listen_btn, self.clear_frame_btn, self.exit_btn]:
            btn.setMaximumHeight(30)
        btn_layout.addWidget(self.start_listen_btn)
        btn_layout.addWidget(self.stop_listen_btn)
        btn_layout.addWidget(self.clear_frame_btn)
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

    def cleanup_old_nak_requests(self):
        """清理过时的NAK请求记录"""
        current_time = time.time()
        old_keys = [k for k, v in self.nak_requests.items() if current_time - v > 30]
        for key in old_keys:
            del self.nak_requests[key]
        if old_keys:
            self.log_signal.emit(f"清理了{len(old_keys)}个旧NAK请求记录", "info")

    def start_listen(self):
        try:
            self.recv_port = int(self.port_edit.text().strip())
        except ValueError:
            self.recv_port = DEFAULT_RECV_PORT
            self.log_signal.emit(f"端口无效，使用默认端口{DEFAULT_RECV_PORT}", "warn")
        
        self.send_ip = self.ip_edit.text().strip() or DEFAULT_SEND_IP
        
        try:
            self.send_port = int(self.send_port_edit.text().strip())
        except ValueError:
            self.send_port = DEFAULT_SEND_PORT
            self.log_signal.emit(f"发送端口无效，使用默认端口{DEFAULT_SEND_PORT}", "warn")

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.bind(("", self.recv_port))
            self.sock.setblocking(False)
            self.is_listening = True
            self.recv_timer = QTimer()
            self.recv_timer.timeout.connect(self.receive_frame)
            self.recv_timer.start(100)
            self.log_signal.emit(f"监听启动成功，绑定端口{self.recv_port}", "success")
            self.start_listen_btn.setEnabled(False)
            self.stop_listen_btn.setEnabled(True)
            self.send_ack_btn.setEnabled(True)
            self.send_nak_btn.setEnabled(True)
            self.batch_deliver_btn.setEnabled(True)
        except Exception as e:
            self.log_signal.emit(f"监听启动失败：{str(e)}", "error")

    def stop_listen(self):
        self.is_listening = False
        if self.sock:
            self.sock.close()
            self.sock = None
        if self.recv_timer:
            self.recv_timer.stop()
            self.recv_timer = None
        self.log_signal.emit("监听已停止", "info")
        self.start_listen_btn.setEnabled(True)
        self.stop_listen_btn.setEnabled(False)
        self.send_ack_btn.setEnabled(False)
        self.send_nak_btn.setEnabled(False)
        self.batch_deliver_btn.setEnabled(False)

    def receive_frame(self):
        if not self.is_listening or not self.sock:
            return
        
        try:
            data, addr = self.sock.recvfrom(1024)
            frame_str = data.decode("utf-8", errors='ignore')
            
            try:
                frame = json.loads(frame_str)
                if not isinstance(frame, dict) or "seq_no" not in frame or "data" not in frame or "crc" not in frame:
                    self.log_signal.emit(f"无效帧格式", "error")
                    return
                
                seq_no = frame["seq_no"]
                frame_data = frame["data"]
                recv_crc = frame["crc"]
                
            except json.JSONDecodeError:
                self.log_signal.emit(f"帧解析失败，可能是损坏的帧", "error")
                return

            # 计算CRC进行验证
            crc_data = f"{seq_no}|{frame_data}"
            calc_crc_value = calc_crc(crc_data)
            crc_state = FrameState.CRC_PASS if recv_crc == calc_crc_value else FrameState.CRC_FAIL

            recv_time = time.strftime("%H:%M:%S", time.localtime())
            
            # 检查是否已经收到过此帧
            existing_info = self.received_frames.get(seq_no)
            retry_count = existing_info.get("retry_count", 0) + 1 if existing_info else 1
            
            if crc_state == FrameState.CRC_PASS:
                if seq_no == self.exp_seq:
                    # 正确接收到期望的帧
                    state = FrameState.RECEIVED
                    self.log_signal.emit(f"帧{seq_no}：有序接收（数据：{frame_data}，CRC：通过）", "success")
                    
                    # 存储帧信息
                    self.received_frames[seq_no] = {
                        "frame": frame,
                        "crc_state": crc_state,
                        "recv_time": recv_time,
                        "state": state,
                        "retry_count": retry_count
                    }
                    
                    # 更新期望序号
                    self.exp_seq += 1
                    self.exp_seq_label.setText(f"期望接收序号：<span style='color:#d93025; font-size:14px; font-weight:bold'>{self.exp_seq}</span>")
                    
                    # 检查是否有缓存的连续帧可以处理
                    self.check_buffered_frames()
                    
                    # 发送ACK
                    self.send_ack_nak("ACK", self.exp_seq)
                    
                    # 尝试交付
                    self.deliver_signal.emit([seq_no])
                    
                else:
                    # 失序帧处理
                    if seq_no < self.exp_seq:
                        # 重复帧（已经接收过的帧）
                        state = FrameState.RECEIVED
                        self.log_signal.emit(f"帧{seq_no}：重复接收，已丢弃", "warn")
                        
                        # 发送ACK确认
                        self.send_ack_nak("ACK", self.exp_seq)
                    else:
                        # 未来的帧（失序），缓存起来
                        state = FrameState.OUT_OF_ORDER
                        self.log_signal.emit(f"帧{seq_no}：失序接收（期望{self.exp_seq}，数据：{frame_data}）", "warn")
                        
                        # 存储帧信息
                        self.received_frames[seq_no] = {
                            "frame": frame,
                            "crc_state": crc_state,
                            "recv_time": recv_time,
                            "state": state,
                            "retry_count": retry_count
                        }
                        
                        # 发送NAK，请求期望的帧
                        self.send_ack_nak("NAK", self.exp_seq)
            else:
                # CRC失败
                state = FrameState.RECEIVED
                self.log_signal.emit(f"帧{seq_no}：CRC校验失败（数据：{frame_data}）", "error")
                
                # 存储帧信息
                self.received_frames[seq_no] = {
                    "frame": frame,
                    "crc_state": crc_state,
                    "recv_time": recv_time,
                    "state": state,
                    "retry_count": retry_count
                }
                
                # 发送NAK，请求重传
                self.send_ack_nak("NAK", seq_no)

            # 更新接收计数
            self.recv_count_label.setText(f"已接收帧数：{len(self.received_frames)}")
            self.frame_update_signal.emit()

        except BlockingIOError:
            # 没有数据可读，正常情况
            pass
        except Exception as e:
            self.log_signal.emit(f"接收帧错误：{str(e)}", "error")

    def check_buffered_frames(self):
        """检查缓存的帧是否可以按顺序处理"""
        # 持续检查，直到没有连续的帧为止
        while True:
            frame_info = self.received_frames.get(self.exp_seq)
            if not frame_info:
                break
                
            if (frame_info["crc_state"] == FrameState.CRC_PASS and 
                frame_info["state"] != FrameState.DELIVERED):
                # 可以处理这个缓存的帧
                self.exp_seq += 1
                self.log_signal.emit(f"处理缓存帧{self.exp_seq-1}，期望序号更新为{self.exp_seq}", "success")
                
                # 发送ACK
                self.send_ack_nak("ACK", self.exp_seq)
                
                # 尝试交付
                self.deliver_signal.emit([self.exp_seq - 1])
            else:
                # CRC失败或已交付，跳出循环
                break
        
        self.exp_seq_label.setText(
            f"期望接收序号：<span style='color:#d93025; font-size:14px; font-weight:bold'>{self.exp_seq}</span>"
        )

    def send_ack_nak(self, ack_type, seq_no):
        self.error_rate = self.error_slider.value() / 100
        
        # 对于NAK，检查是否最近已经请求过，避免频繁发送
        if ack_type == "NAK":
            current_time = time.time()
            last_request_time = self.nak_requests.get(seq_no, 0)
            if current_time - last_request_time < 0.5:  # 500ms内不重复发送相同NAK
                self.log_signal.emit(f"NAK：最近已请求过重传seq_no={seq_no}，跳过", "info")
                return
            self.nak_requests[seq_no] = current_time
        
        # 计算CRC
        crc_data = f"{ack_type}:{seq_no}"
        crc = calc_crc(crc_data)
        
        ack = {
            "type": ack_type,
            "seq_no": seq_no,
            "crc": crc
        }
        
        # 错误模拟
        send_ack = True
        
        # 检查是否模拟丢失
        if self.ack_lost_check.isChecked() and random.random() < self.error_rate:
            self.log_signal.emit(f"{ack_type}：模拟丢失（seq_no={seq_no}）", "warn")
            send_ack = False
        
        # 检查是否模拟损坏
        elif self.ack_corrupt_check.isChecked() and random.random() < self.error_rate:
            # 损坏ACK：修改CRC
            ack["crc"] = "XX"  # 无效的CRC
            self.log_signal.emit(f"{ack_type}：模拟损坏（seq_no={seq_no}）", "warn")
        
        if send_ack:
            try:
                ack_str = json.dumps(ack, ensure_ascii=False)
                self.sock.sendto(ack_str.encode("utf-8"), (self.send_ip, self.send_port))
                if ack_type == "ACK":
                    self.log_signal.emit(f"{ack_type}发送成功：期望下一个序号={seq_no}", "success")
                else:
                    self.log_signal.emit(f"{ack_type}发送成功：请求重传序号={seq_no}", "success")
            except Exception as e:
                self.log_signal.emit(f"{ack_type}发送失败：{str(e)}", "error")

    def auto_deliver_to_upper(self, start_seqs):
        # 找到所有CRC通过且未交付的连续帧
        delivered_frames = []
        delivered_data = []
        
        # 从期望序号-1开始检查（因为exp_seq是下一个期望的序号）
        current_seq = self.exp_seq - 1
        
        while True:
            frame_info = self.received_frames.get(current_seq)
            if not frame_info:
                break
            
            if frame_info["crc_state"] == FrameState.CRC_PASS and frame_info["state"] != FrameState.DELIVERED:
                delivered_frames.append(current_seq)
                delivered_data.append(frame_info["frame"]["data"])
                frame_info["state"] = FrameState.DELIVERED
                current_seq += 1
            else:
                break
        
        if delivered_data:
            deliver_text = "".join(delivered_data)
            timestamp = time.strftime("%H:%M:%S", time.localtime())
            self.deliver_edit.append(f"[{timestamp}] 交付数据：{deliver_text}（{len(delivered_frames)}帧）")
            
            self.delivered_count += len(delivered_frames)
            self.delivered_count_label.setText(f"已交付帧数：{self.delivered_count}")
            
            self.log_signal.emit(f"成功交付{len(delivered_frames)}帧到上层，累计交付{self.delivered_count}帧", "success")
            self.frame_update_signal.emit()

    def manual_batch_deliver(self):
        # 手动交付所有可交付的帧
        delivered_frames = []
        delivered_data = []
        
        for seq_no in sorted(self.received_frames.keys()):
            frame_info = self.received_frames[seq_no]
            if frame_info["crc_state"] == FrameState.CRC_PASS and frame_info["state"] != FrameState.DELIVERED:
                delivered_frames.append(seq_no)
                delivered_data.append(frame_info["frame"]["data"])
                frame_info["state"] = FrameState.DELIVERED
        
        if delivered_data:
            deliver_text = "".join(delivered_data)
            timestamp = time.strftime("%H:%M:%S", time.localtime())
            self.deliver_edit.append(f"[{timestamp}] 手动交付数据：{deliver_text}（{len(delivered_frames)}帧）")
            
            self.delivered_count += len(delivered_frames)
            self.delivered_count_label.setText(f"已交付帧数：{self.delivered_count}")
            
            self.log_signal.emit(f"手动交付{len(delivered_frames)}帧到上层，累计交付{self.delivered_count}帧", "success")
            self.frame_update_signal.emit()
        else:
            self.log_signal.emit("没有可交付的帧", "info")

    def clear_frame_records(self):
        self.received_frames.clear()
        self.exp_seq = 0
        self.delivered_count = 0
        
        self.exp_seq_label.setText(f"期望接收序号：<span style='color:#d93025; font-size:14px; font-weight:bold'>{self.exp_seq}</span>")
        self.recv_count_label.setText(f"已接收帧数：0")
        self.delivered_count_label.setText(f"已交付帧数：0")
        self.deliver_edit.clear()
        
        self.log_signal.emit("接收记录已清空", "info")
        self.frame_update_signal.emit()

    def update_frame_table(self):
        self.frame_table.setRowCount(0)
        sorted_seqs = sorted(self.received_frames.keys())
        
        for idx, seq_no in enumerate(sorted_seqs):
            info = self.received_frames[seq_no]
            frame = info["frame"]
            row = self.frame_table.rowCount()
            self.frame_table.insertRow(row)
            
            # 添加序号颜色标记
            seq_item = QTableWidgetItem(str(seq_no))
            if seq_no == self.exp_seq:
                # 当前期望的帧（可能已丢失）
                seq_item.setBackground(QColor(255, 200, 200))
                seq_item.setToolTip("当前期望接收的帧")
            elif seq_no < self.exp_seq:
                # 已接收的帧
                seq_item.setBackground(QColor(200, 255, 200))
                seq_item.setToolTip("已正确接收的帧")
            else:
                # 未来的帧
                seq_item.setBackground(QColor(255, 255, 200))
                seq_item.setToolTip("提前接收的帧")
            
            self.frame_table.setItem(row, 0, seq_item)
            
            self.frame_table.setItem(row, 1, QTableWidgetItem(frame["data"]))
            
            crc_item = QTableWidgetItem(info["crc_state"])
            crc_item.setBackground(QColor(219, 243, 219) if info["crc_state"] == FrameState.CRC_PASS else QColor(243, 219, 219))
            self.frame_table.setItem(row, 2, crc_item)
            
            self.frame_table.setItem(row, 3, QTableWidgetItem(info["recv_time"]))
            
            state_item = QTableWidgetItem(info["state"])
            color_map = {
                FrameState.RECEIVED: QColor(251, 243, 219),
                FrameState.OUT_OF_ORDER: QColor(255, 235, 205),
                FrameState.DELIVERED: QColor(219, 243, 219)
            }
            state_item.setBackground(color_map.get(info["state"], QColor(255, 255, 255)))
            self.frame_table.setItem(row, 4, state_item)
            
            self.frame_table.setItem(row, 5, QTableWidgetItem(str(info.get("retry_count", 0))))
            
            deliver_btn = QPushButton("标记交付")
            deliver_btn.setMaximumWidth(70)
            deliver_btn.clicked.connect(lambda _, s=seq_no: self.mark_delivered(s))
            self.frame_table.setCellWidget(row, 6, deliver_btn)
        
        # 高亮期望序号
        for row in range(self.frame_table.rowCount()):
            seq_no_item = self.frame_table.item(row, 0)
            if not seq_no_item:
                continue
            
            seq_no = int(seq_no_item.text())
            if seq_no == self.exp_seq - 1:  # 期望的帧应该是exp_seq-1
                for col in range(6):
                    item = self.frame_table.item(row, col)
                    if item:
                        item.setFont(QFont("", 13, QFont.Weight.Bold))
                        item.setForeground(QColor("#d93025"))

    def mark_delivered(self, seq_no):
        info = self.received_frames.get(seq_no)
        if not info:
            self.log_signal.emit(f"帧{seq_no}不存在", "error")
            return
        
        if info["state"] == FrameState.DELIVERED:
            self.log_signal.emit(f"帧{seq_no}已交付", "error")
            return
        
        if info["crc_state"] != FrameState.CRC_PASS:
            self.log_signal.emit(f"帧{seq_no}CRC失败，无法交付", "error")
            return
        
        info["state"] = FrameState.DELIVERED
        self.delivered_count += 1
        self.delivered_count_label.setText(f"已交付帧数：{self.delivered_count}")
        
        deliver_text = info["frame"]["data"]
        timestamp = time.strftime("%H:%M:%S", time.localtime())
        self.deliver_edit.append(f"[{timestamp}] 手动标记交付：{deliver_text}（帧{seq_no}）")
        
        self.log_signal.emit(f"帧{seq_no}已标记为已交付", "success")
        self.frame_update_signal.emit()

    def closeEvent(self, event):
        self.is_listening = False
        if self.sock:
            self.sock.close()
        if self.recv_timer:
            self.recv_timer.stop()
        if self.nak_cleanup_timer:
            self.nak_cleanup_timer.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ReceiverWindow()
    window.show()
    sys.exit(app.exec())