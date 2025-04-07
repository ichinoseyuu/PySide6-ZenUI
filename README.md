# ZenUI

## How to use

### install

```powershell
pip install pyside6
pip install pywin32
python setup.py sdist
pip install ./dist/zenui-0.1.0.tar.gz
```

### uninstall

```powershell
pip uninstall ZenUI
```

## Documentation

### conmponent

- ZenWidget(QWidget)  
支持改变背景、透明度、锚点移动、大小等动画效果

    ```python
    from ZenUI import *
    widget = ZenWidget()
    ```

- ZenLayer(QWidget)  
用于实现物件表面颜色变化的组件

- ZenTextLabel(QLabel)  
用于显示文本内容，具有根据主题改变文本颜色的动画效果

- ZenImageLabel(QLabel)  
用于显示图片内容

- ZenPushButton(QPushButton)  
按钮组件，具有悬浮动画和点击闪烁动画效果

- ZenTransButton(QPushButton)  
透明按钮组件，具有悬浮动画效果

### core

### gui
