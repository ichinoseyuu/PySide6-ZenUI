from PySide6.QtCore import QObject, QTimer, Signal
import numpy as np
from concurrent.futures import ThreadPoolExecutor

class AnimationManager(QObject):
    """动画管理器 - 单例模式"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
        
    def __init__(self):
        if not hasattr(self, 'initialized'):
            super().__init__()
            self.initialized = True
            self._animations = []
            self._thread_pool = ThreadPoolExecutor(max_workers=4)
            
            # 使用单个定时器管理所有动画
            self._timer = QTimer()
            self._timer.setInterval(1000/60)  # ~60fps
            self._timer.timeout.connect(self._process_animations)
            
    def add_animation(self, animation):
        """添加动画到管理器"""
        if animation not in self._animations:
            self._animations.append(animation)
            if not self._timer.isActive():
                self._timer.start()
                
    def remove_animation(self, animation):
        """从管理器移除动画"""
        if animation in self._animations:
            self._animations.remove(animation)
            if not self._animations:
                self._timer.stop()
                
    def _process_animations(self):
        """并行处理所有动画"""
        futures = []
        for anim in self._animations[:]:
            if anim.isCompleted():
                self.remove_animation(anim)
                anim.finished.emit(anim.target())
                continue
                
            future = self._thread_pool.submit(anim._calculate_step)
            futures.append((anim, future))
            
        # 处理计算结果
        for anim, future in futures:
            try:
                step = future.result()
                anim.setCurrent(anim.current() + step)
                anim.ticked.emit(anim.current())
            except Exception as e:
                print(f"动画计算错误: {e}")