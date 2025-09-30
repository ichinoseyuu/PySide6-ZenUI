import sys
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QComboBox,
                               QCheckBox, QPushButton, QSpinBox, QLabel,
                               QApplication, QGroupBox, QGridLayout)
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QCursor

# 假设 tooltip.py 和 tooldipdemo.py 在同一目录下
from .tooltip import ZToolTip
from ZenUI.component.base import ZPosition

class ZToolTipDemo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # --- 创建 ZToolTip 实例 ---
        self._tooltip = ZToolTip()
        # --- 创建主布局 ---
        self.main_layout = QVBoxLayout(self)
        # --- 创建控制面板 ---
        self.control_group = QGroupBox("ZToolTip Controls", self)
        self.control_layout = QGridLayout()
        self.control_group.setLayout(self.control_layout)
        self.main_layout.addWidget(self.control_group)

        # --- 创建目标区域 ---
        self.target_group = QGroupBox("Hover over this area to see the tooltip", self)
        self.target_group.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.target_group.setFixedHeight(60)
        self.target_group.setStyleSheet("background-color: lightgray;")
        self.main_layout.addWidget(self.target_group)

        # --- 初始化控制控件 ---
        self._init_controls()

        # --- 设置目标区域的事件 ---
        self.target_group.setMouseTracking(True)
        self.target_group.enterEvent = self._on_target_enter
        self.target_group.leaveEvent = self._on_target_leave

    def _init_controls(self):
        # Position ComboBox
        self.pos_label = QLabel("Position:")
        self.pos_combo = QComboBox()
        self.pos_combo.setStyleSheet("background-color: white; border: 1px solid gray;")
        for pos in ZPosition:
            self.pos_combo.addItem(pos.name, pos)
        self.pos_combo.setCurrentText(ZPosition.TopRight.name)
        self.control_layout.addWidget(self.pos_label, 0, 0)
        self.control_layout.addWidget(self.pos_combo, 0, 1)

        # Mode ComboBox
        self.mode_label = QLabel("TrackMode:")
        self.mode_combo = QComboBox()
        self.mode_combo.setStyleSheet("background-color: white; border: 1px solid gray;")
        for mode in ZToolTip.Mode:
            self.mode_combo.addItem(mode.name, mode)
        self.mode_combo.setCurrentText(ZToolTip.Mode.TrackMouse.name)
        self.control_layout.addWidget(self.mode_label, 1, 0)
        self.control_layout.addWidget(self.mode_combo, 1, 1)

        # Show Delay SpinBox
        self.delay_label = QLabel("Show Delay (ms):")
        self.delay_spin = QSpinBox()
        self.delay_spin.setRange(0, 5000)
        self.delay_spin.setValue(0)
        self.delay_spin.setSingleStep(100)
        self.control_layout.addWidget(self.delay_label, 2, 0)
        self.control_layout.addWidget(self.delay_spin, 2, 1)

        # Hide Delay SpinBox
        self.hide_delay_label = QLabel("Hide Delay (ms):")
        self.hide_delay_spin = QSpinBox()
        self.hide_delay_spin.setRange(0, 10000)
        self.hide_delay_spin.setValue(0)
        self.hide_delay_spin.setSingleStep(500)
        self.control_layout.addWidget(self.hide_delay_label, 3, 0)
        self.control_layout.addWidget(self.hide_delay_spin, 3, 1)

        # Offset X SpinBox
        self.offset_x_label = QLabel("Offset X:")
        self.offset_x_spin = QSpinBox()
        self.offset_x_spin.setRange(-100, 100)
        self.offset_x_spin.setValue(6)
        self.control_layout.addWidget(self.offset_x_label, 0, 2)
        self.control_layout.addWidget(self.offset_x_spin, 0, 3)

        # Offset Y SpinBox
        self.offset_y_label = QLabel("Offset Y:")
        self.offset_y_spin = QSpinBox()
        self.offset_y_spin.setRange(-100, 100)
        self.offset_y_spin.setValue(6)
        self.control_layout.addWidget(self.offset_y_label, 1, 2)
        self.control_layout.addWidget(self.offset_y_spin, 1, 3)

        # Text to display
        self.text_label = QLabel("Text:")
        self.text_edit = QLabel("This is a tooltip.")
        self.text_edit.setWordWrap(True)
        self.control_layout.addWidget(self.text_label, 2, 2)
        self.control_layout.addWidget(self.text_edit, 2, 3, 2, 1) # Span 2 rows

    def _on_target_enter(self, event):
        # 从控件获取当前设置
        position = self.pos_combo.currentData()
        mode = self.mode_combo.currentData()
        show_delay = self.delay_spin.value()
        hide_delay = self.hide_delay_spin.value()
        offset = QPoint(self.offset_x_spin.value(), self.offset_y_spin.value())
        text = self.text_edit.text()

        # 调用 showTip 显示工具提示
        # 使用 QTimer.delay 实现显示延迟
        if show_delay > 0:
            from PySide6.QtCore import QTimer
            QTimer.singleShot(show_delay, lambda: self._show_tooltip_actual(text, position, mode, offset, hide_delay))
        else:
            self._show_tooltip_actual(text, position, mode, offset, hide_delay)

    def _show_tooltip_actual(self, text, position, mode, offset, hide_delay):
        # 检查鼠标是否仍在目标区域内，避免延迟后鼠标已离开却仍显示提示
        if self.target_group.underMouse():
            self._tooltip.showTip(
                text=text,
                target=self.target_group,
                mode=mode,
                position=position,
                offset=offset,
                hide_delay=hide_delay
            )

    def _on_target_leave(self, event):
        # 鼠标离开，立即隐藏工具提示
        self._tooltip.hideTip()
