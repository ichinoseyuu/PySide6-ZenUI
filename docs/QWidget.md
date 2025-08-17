# QWidget

## 🔧 **构造与析构**

### `__init__()`

- **用途**：初始化 QWidget 对象
- **参数**：包含大量可选参数，可以在创建时设置几乎所有的部件属性
- **示例**：`widget = QWidget(parent=None, geometry=QRect(0,0,200,100))`

### `__repr__()`

- **用途**：返回对象的字符串表示，用于调试
- **返回**：描述对象的字符串

## 📏 **几何与尺寸管理**

### 位置相关

- `pos()` / `x()` / `y()`：获取部件位置
- `move(x, y)` / `move(QPoint)`：移动部件到指定位置
- `geometry()` / `setGeometry()`：获取/设置部件几何信息（位置+尺寸）
- `frameGeometry()`：获取包含边框的几何信息
- `rect()`：获取部件的矩形区域（相对于自身）

### 尺寸相关

- `size()` / `width()` / `height()`：获取当前尺寸
- `resize(w, h)` / `resize(QSize)`：调整部件尺寸
- `sizeHint()` / `minimumSizeHint()`：获取建议尺寸/最小建议尺寸
- `adjustSize()`：根据内容自动调整尺寸

### 尺寸约束

- `minimumSize()` / `setMinimumSize()`：最小尺寸
- `maximumSize()` / `setMaximumSize()`：最大尺寸
- `setFixedSize()` / `setFixedWidth()` / `setFixedHeight()`：固定尺寸
- `sizeIncrement()` / `setSizeIncrement()`：尺寸增量
- `baseSize()` / `setBaseSize()`：基础尺寸

## 🎨 **外观与样式**

### 颜色与绘制

- `palette()` / `setPalette()`：调色板
- `backgroundRole()` / `setBackgroundRole()`：背景角色
- `foregroundRole()` / `setForegroundRole()`：前景角色
- `autoFillBackground()` / `setAutoFillBackground()`：自动填充背景

### 字体

- `font()` / `setFont()`：字体设置
- `fontInfo()` / `fontMetrics()`：字体信息和度量

### 样式

- `style()` / `setStyle()`：样式对象
- `styleSheet()` / `setStyleSheet()`：CSS样式表
- `cursor()` / `setCursor()` / `unsetCursor()`：鼠标光标

### 遮罩与特效

- `mask()` / `setMask()` / `clearMask()`：遮罩设置
- `graphicsEffect()` / `setGraphicsEffect()`：图形特效

## 🔄 **显示与状态管理**

### 可见性

- `isVisible()` / `setVisible()` / `setHidden()`：可见性控制
- `show()` / `hide()`：显示/隐藏
- `showNormal()` / `showMaximized()` / `showMinimized()` / `showFullScreen()`：不同显示模式

### 窗口状态

- `isEnabled()` / `setEnabled()` / `setDisabled()`：启用/禁用
- `isActiveWindow()` / `activateWindow()`：激活状态
- `windowState()` / `setWindowState()`：窗口状态（最大化、最小化等）
- `isWindow()` / `isTopLevel()`：判断是否为顶级窗口

## 🖱️ **事件处理**

### 鼠标事件

- `mousePressEvent()` / `mouseReleaseEvent()`：鼠标按下/释放
- `mouseMoveEvent()` / `mouseDoubleClickEvent()`：鼠标移动/双击
- `enterEvent()` / `leaveEvent()`：鼠标进入/离开
- `wheelEvent()`：鼠标滚轮事件

### 键盘事件

- `keyPressEvent()` / `keyReleaseEvent()`：按键按下/释放
- `focusInEvent()` / `focusOutEvent()`：获得/失去焦点

### 绘制事件

- `paintEvent()`：绘制事件（最重要的绘制方法）
- `repaint()` / `update()`：强制重绘/请求更新

### 其他事件

- `resizeEvent()` / `moveEvent()`：尺寸/位置改变
- `showEvent()` / `hideEvent()`：显示/隐藏事件
- `closeEvent()`：关闭事件
- `changeEvent()`：属性改变事件

## ⌨️ **焦点管理**

- `hasFocus()` / `setFocus()` / `clearFocus()`：焦点状态
- `focusPolicy()` / `setFocusPolicy()`：焦点策略
- `focusWidget()` / `focusProxy()` / `setFocusProxy()`：焦点部件
- `focusNextChild()` / `focusPreviousChild()`：焦点切换
- `nextInFocusChain()` / `previousInFocusChain()`：焦点链

## 🏗️ **布局与层次**

### 父子关系

- `parentWidget()` / `setParent()`：父部件
- `childAt()` / `childrenRect()` / `childrenRegion()`：子部件信息
- `isAncestorOf()`：判断祖先关系

### 布局

- `layout()` / `setLayout()`：布局管理器
- `contentsMargins()` / `setContentsMargins()`：内容边距
- `contentsRect()`：内容矩形区域

### Z顺序

- `raise_()` / `lower()`：提升/降低层次
- `stackUnder()`：堆叠在指定部件下方

## 🎯 **交互功能**

### 动作系统

- `addAction()` / `removeAction()`：添加/移除动作
- `actions()`：获取所有动作
- `insertAction()` / `insertActions()`：插入动作

### 快捷键

- `grabShortcut()` / `releaseShortcut()`：获取/释放快捷键
- `setShortcutEnabled()` / `setShortcutAutoRepeat()`：快捷键设置

### 输入捕获

- `grabMouse()` / `releaseMouse()`：鼠标捕获
- `grabKeyboard()` / `releaseKeyboard()`：键盘捕获

## 📱 **触摸与手势**

- `grabGesture()` / `ungrabGesture()`：手势识别
- `tabletEvent()`：数位板事件
- `hasTabletTracking()` / `setTabletTracking()`：数位板跟踪

## 🗂️ **窗口属性**

### 窗口信息

- `windowTitle()` / `setWindowTitle()`：窗口标题
- `windowIcon()` / `setWindowIcon()`：窗口图标
- `windowFlags()` / `setWindowFlags()`：窗口标志
- `windowModality()` / `setWindowModality()`：模态性

### 窗口文件

- `windowFilePath()` / `setWindowFilePath()`：关联文件路径
- `isWindowModified()` / `setWindowModified()`：修改状态

## 🌐 **国际化**

- `locale()` / `setLocale()`：区域设置
- `layoutDirection()` / `setLayoutDirection()`：布局方向
- `isLeftToRight()` / `isRightToLeft()`：文字方向判断

## 🔧 **辅助功能**

- `accessibleName()` / `setAccessibleName()`：可访问性名称
- `accessibleDescription()` / `setAccessibleDescription()`：可访问性描述
- `toolTip()` / `setToolTip()`：工具提示
- `statusTip()` / `setStatusTip()`：状态提示
- `whatsThis()` / `setWhatsThis()`：帮助文本

## 🖼️ **渲染与绘制**

### 绘制设备

- `paintEngine()`：绘制引擎
- `metric()`：设备度量信息
- `devType()`：设备类型

### 渲染控制

- `render()`：渲染到指定设备
- `grab()`：截取部件图像
- `backingStore()`：后备存储

### 坐标转换

- `mapTo()` / `mapFrom()`：坐标系转换
- `mapToGlobal()` / `mapFromGlobal()`：全局坐标转换
- `mapToParent()` / `mapFromParent()`：父坐标转换

## ⚙️ **系统集成**

### 窗口系统

- `winId()` / `effectiveWinId()`：窗口ID
- `createWinId()` / `internalWinId()`：创建窗口ID
- `windowHandle()`：窗口句柄

### 屏幕管理

- `screen()` / `setScreen()`：屏幕对象

### 几何保存

- `saveGeometry()` / `restoreGeometry()`：保存/恢复几何信息

## 📋 **实用方法**

### 查找与检测

- `find(winId)`：根据窗口ID查找部件（静态方法）
- `underMouse()`：鼠标是否在部件上
- `visibleRegion()`：可见区域

### 更新控制

- `updatesEnabled()` / `setUpdatesEnabled()`：更新启用状态
- `updateGeometry()`：更新几何信息

### 属性设置

- `setAttribute()` / `testAttribute()`：设置/测试部件属性
