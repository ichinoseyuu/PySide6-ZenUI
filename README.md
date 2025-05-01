# ZenUI

## How to use

### install

```powershell
pip install pyside6
pip install pywin32

python setup.py sdist
pip install ./dist/zenui-0.1.0.tar.gz
# or
python setup.py install
```

### uninstall

```powershell
pip uninstall ZenUI
```

## Documentation

### conmponent

- ZenWidget(QWidget)  
支持改变背景、透明度、锚点移动、大小等动画效果。

- ZenTextLabel(QLabel)  
用于显示文本内容，具有根据主题改变文本颜色的动画效果。

- ZenImageLabel(QLabel)  
用于显示图片内容。

- ZenPushButton(QPushButton)  
按钮组件，具有悬浮动画和点击闪烁动画效果。

- ZenTransButton(QPushButton)  
透明按钮组件，具有悬浮动画效果。

- ZenWindow(Qwidget)  
窗口组件，具有窗口最小化、窗口最大化等动画效果。

- ZenMainWindow(ZenWindow)  
主窗口组件。

- ZenTitlebar(ZenWidget)  
窗口标题栏组件，具有拖动窗口移动、关闭窗口、最小化窗口、最大化窗口、切换主题等功能。

- ZenContainer(ZenWidget)  
容器组件，自带布局。

pushbutton
trans button
ghost button
icon button
radio button
checkboxs
longpressbutton
tab button

### core

- ZenExpAnim(QObject)  
级数动画组件，支持任何可以变化的值。

- ZenEffect  
效果组件，可以快速的设置窗口阴影。

- Zen(Enum)  
枚举类，用于定义主题、窗口状态等。

- ZenGlobal  
全局变量类，如主题切换、窗口引用等。

- ColorTool  
颜色工具类，用于颜色转换。

- ColorConfig  
颜色配置管理类，继承这个类可以实现一套配置，每套配置独立且互不干扰

- ZenColorConfig(ColorConfig)  
颜色配置，定义了一套包含深色主题和浅色主题的颜色配置

- ColorSheet  
每个控件的自己的颜色表，同类型控件之间独立，需要从ColorConfig类的子类中获取相应的颜色表

### gui
