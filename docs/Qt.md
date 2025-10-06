# Qt 枚举类型说明

## 1. TextFlag（文本处理标志）

| 枚举成员 | 十六进制值 | 类别 | 含义 | 效果 | 适用场景 |
|---------|------------|------|------|------|----------|
| `TextSingleLine` | 0x100 | 文本换行和裁剪控制 | 强制文本显示为单行 | 无论文本多长都不会换行，超出部分会被截断或省略 | 标题、标签、按钮文字等需要保持单行的场合 |
| `TextDontClip` | 0x200 | 文本换行和裁剪控制 | 不裁剪文本 | 即使文本超出绘制区域也完整绘制，可能会绘制到边界外 | 需要完整显示文本内容，不在乎是否超出边界的情况 |
| `TextWordWrap` | 0x1000 | 文本换行和裁剪控制 | 按单词边界换行 | 在空格、标点符号等单词分隔符处换行，保持单词完整性 | 英文文档、多行文本显示 |
| `TextWrapAnywhere` | 0x2000 | 文本换行和裁剪控制 | 在任意字符处换行 | 可以在任何字符之间断行，包括单词中间 | 中文文本、需要紧凑显示的长字符串、URL等 |
| `TextExpandTabs` | 0x400 | Tab 和空格处理 | 展开制表符 | 将 `\t` 字符转换为相应数量的空格 | 显示代码、格式化文本 |
| `TextIncludeTrailingSpaces` | 0x8000000 | Tab 和空格处理 | 包含尾随空格 | 在计算文本尺寸时包含行尾的空格 | 精确的文本布局计算 |
| `TextShowMnemonic` | 0x800 | 快捷键和助记符 | 显示助记符 | 显示 `&` 符号标记的快捷键字符（如 `&File` 显示为带下划线的 `F`） | 菜单项、按钮等需要键盘快捷键的界面元素 |
| `TextHideMnemonic` | 0x8000 | 快捷键和助记符 | 隐藏助记符 | 不显示助记符的下划线，但保留快捷键功能 | 当不需要视觉提示助记符时 |
| `TextDontPrint` | 0x4000 | 打印控制 | 不打印此文本 | 在打印时跳过此文本内容 | 屏幕显示专用的提示文字、调试信息等 |
| `TextJustificationForced` | 0x10000 | 文本对齐和方向 | 强制两端对齐 | 通过调整字符间距使文本两端对齐 | 正式文档、报告等需要整齐排版的场合 |
| `TextForceLeftToRight` | 0x20000 | 文本对齐和方向 | 强制从左到右的文本方向 | 无论系统语言设置如何，都按从左到右显示 | 数字、英文标识符等 |
| `TextForceRightToLeft` | 0x40000 | 文本对齐和方向 | 强制从右到左的文本方向 | 按从右到左的方向显示文本 | 阿拉伯语、希伯来语等 |
| `TextLongestVariant` | 0x80000 | 国际化支持 | 使用最长的文本变体 | 在多语言环境中选择最长的翻译版本进行布局计算 | 国际化应用的界面布局 |

### 1.1 常见组合示例

```python
# 单行文本，显示助记符
flags = Qt.TextFlag.TextSingleLine | Qt.TextFlag.TextShowMnemonic

# 多行自动换行，展开Tab
flags = Qt.TextFlag.TextWordWrap | Qt.TextFlag.TextExpandTabs

# 中文文本，任意位置换行
flags = Qt.TextFlag.TextWrapAnywhere

# 不裁剪的单行文本
flags = Qt.TextFlag.TextSingleLine | Qt.TextFlag.TextDontClip
```

## 2. WindowType（窗口类型）

| 枚举成员 | 十六进制值 | 类别 | 含义说明 | 平台差异 |
|---------|------------|------|----------|----------|
| `Widget` | 0x0 | 核心窗口类型 | 基础控件类型，默认无独立窗口特性，需嵌入其他容器才能显示，不具备独立标题栏/边框 | 跨平台一致 |
| `Window` | 0x1 | 核心窗口类型 | 标准独立窗口，具备完整窗口特性（标题栏、边框、最小化/最大化按钮），可独立存在于任务栏 | 跨平台一致 |
| `Dialog` | 0x3 | 核心窗口类型 | 对话框窗口，用于交互（如确认、输入），通常模态（阻塞父窗口），标题栏简化，默认无最大化按钮 | 跨平台一致 |
| `Sheet` | 0x5 | 核心窗口类型 | macOS 专属“表单窗口”，从父窗口顶部滑入（如保存对话框） | 仅在 macOS 生效，Windows/Linux 无效果 |
| `Drawer` | 0x7 | 核心窗口类型 | 抽屉式窗口，从父窗口边缘（通常左侧/右侧）滑出，用于临时展示附加内容 | 跨平台支持有限 |
| `Popup` | 0x9 | 核心窗口类型 | 弹出式窗口，用于临时内容（如菜单、下拉列表），无标题栏，焦点丢失时自动隐藏，不显示在任务栏 | 跨平台一致 |
| `Tool` | 0xb | 核心窗口类型 | 工具窗口（如调色板、辅助面板），标题栏简化，默认始终在父窗口上方，任务栏中可能不单独显示 | 跨平台一致 |
| `ToolTip` | 0xd | 核心窗口类型 | 提示窗口，用于显示控件的简短说明（如鼠标悬停提示），无边框/标题栏，自动显示/隐藏，不接受焦点 | 跨平台一致 |
| `SplashScreen` | 0xf | 核心窗口类型 | 启动屏窗口，用于程序启动时显示加载进度，无边框，通常全屏或居中，加载完成后自动关闭 | 跨平台一致 |
| `Desktop` | 0x11 | 核心窗口类型 | 桌面窗口，用于覆盖整个桌面（如桌面背景、桌面图标容器），优先级极低，不会遮挡其他窗口 | 跨平台一致 |
| `SubWindow` | 0x12 | 核心窗口类型 | 子窗口，必须嵌入父窗口（如 MDI 多文档界面的子窗口），无独立任务栏图标，父窗口关闭时一同关闭 | 跨平台一致 |
| `ForeignWindow` | 0x21 | 核心窗口类型 | 外部窗口包装器，用于将非 Qt 窗口嵌入 Qt 程序中 | 跨平台一致 |
| `CoverWindow` | 0x41 | 核心窗口类型 | 封面窗口，用于设备“封面展示”（如手机锁屏封面、平板待机界面） | 移动平台（如 Qt for Android）更常用 |
| `WindowType_Mask` | 0xff | 核心窗口类型 | 窗口类型“掩码”，用于按位运算提取窗口的“核心类型”，不直接用于设置窗口类型 | 跨平台一致 |
| `MSWindowsFixedSizeDialogHint` | 0x100 | 平台专属窗口提示 | Windows 专属：固定大小对话框，禁用窗口拉伸 | 仅 Windows 生效 |
| `MSWindowsOwnDC` | 0x200 | 平台专属窗口提示 | Windows 专属：为窗口分配独立的设备上下文（DC），用于高效绘制 | 仅 Windows 生效 |
| `MacWindowToolBarButtonHint` | 0x10000000 | 平台专属窗口提示 | macOS 专属：在窗口标题栏添加“工具栏按钮” | 仅 macOS 生效 |
| `BypassWindowManagerHint` / `X11BypassWindowManagerHint` | 0x400 | 窗口行为与样式提示 | 绕过窗口管理器控制，窗口无边框/标题栏，位置和大小完全由程序控制 | X11（Linux）中别名 `X11BypassWindowManagerHint` |
| `FramelessWindowHint` | 0x800 | 窗口行为与样式提示 | 无边框窗口，隐藏系统默认标题栏和边框，需手动实现窗口拖动、关闭等功能 | 跨平台一致 |
| `WindowTitleHint` | 0x1000 | 窗口行为与样式提示 | 强制显示窗口标题栏（即使其他标志隐藏了标题栏） | 跨平台一致 |
| `WindowSystemMenuHint` | 0x2000 | 窗口行为与样式提示 | 显示窗口系统菜单（标题栏右键菜单/左上角图标菜单） | 跨平台一致 |
| `WindowMinimizeButtonHint` | 0x4000 | 窗口行为与样式提示 | 显示窗口最小化按钮，仅当窗口具备标题栏时生效 | 跨平台一致 |
| `WindowMaximizeButtonHint` | 0x8000 | 窗口行为与样式提示 | 显示窗口最大化按钮，仅支持 `Window` 类型 | 跨平台一致 |
| `WindowMinMaxButtonsHint` | 0xc000 | 窗口行为与样式提示 | 同时显示最小化和最大化按钮 | 跨平台一致 |
| `WindowContextHelpButtonHint` | 0x10000 | 窗口行为与样式提示 | 显示“上下文帮助按钮”（标题栏问号按钮） | 跨平台一致 |
| `WindowShadeButtonHint` | 0x20000 | 窗口行为与样式提示 | 显示窗口“折叠按钮” | 部分系统（如 Linux）支持，Windows 无效果 |
| `WindowStaysOnTopHint` | 0x40000 | 窗口行为与样式提示 | 窗口始终置顶，显示在其他非置顶窗口上方 | 跨平台一致 |
| `WindowTransparentForInput` | 0x80000 | 窗口行为与样式提示 | 窗口对输入透明（鼠标点击、键盘事件会穿透），但视觉上仍可见 | 跨平台一致 |
| `WindowOverridesSystemGestures` | 0x100000 | 窗口行为与样式提示 | 覆盖系统手势，程序自行处理手势事件 | 跨平台一致 |
| `WindowDoesNotAcceptFocus` | 0x200000 | 窗口行为与样式提示 | 窗口不接受焦点，键盘事件不会传递到该窗口 | 跨平台一致 |
| `ExpandedClientAreaHint` / `MaximizeUsingFullscreenGeometryHint` | 0x400000 | 窗口行为与样式提示 | 最大化时使用全屏几何（覆盖任务栏） | 部分系统中 `ExpandedClientAreaHint` 为别名 |
| `NoTitleBarBackgroundHint` | 0x800000 | 窗口行为与样式提示 | 隐藏标题栏背景（仅保留标题文字和按钮） | 部分系统支持 |
| `CustomizeWindowHint` | 0x2000000 | 窗口行为与样式提示 | 允许完全自定义窗口样式，禁用系统默认的标题栏、边框绘制 | 跨平台一致 |
| `WindowStaysOnBottomHint` | 0x4000000 | 窗口行为与样式提示 | 窗口始终置底，显示在所有非置底窗口下方 | 跨平台一致 |
| `WindowCloseButtonHint` | 0x8000000 | 窗口行为与样式提示 | 显示窗口关闭按钮，通常无需手动设置 | 跨平台一致 |
| `BypassGraphicsProxyWidget` | 0x20000000 | 窗口行为与样式提示 | 绕过 Qt 图形代理控件，直接渲染原生控件 | 跨平台一致 |
| `NoDropShadowWindowHint` | 0x40000000 | 窗口行为与样式提示 | 禁用窗口默认的阴影效果 | 跨平台一致 |
| `WindowFullscreenButtonHint` | 0x80000000（带符号） | 特殊标志 | 预留的“全屏按钮提示”，用于控制是否显示全屏按钮 | 部分 Qt 版本支持，优先级低于系统默认行为 |

### 2.1 关键使用说明

- **按位组合使用**：枚举类型为 `IntFlag`，支持按位或（`|`）组合多个标志，例如：

```python
# 无边框 + 始终置顶 + 不接受焦点
window.setWindowFlags(WindowType.FramelessWindowHint | WindowType.WindowStaysOnTopHint | WindowType.WindowDoesNotAcceptFocus)
```

- **平台兼容性**：标注“macOS 专属”“Windows 专属”的成员，在其他平台设置后无效果，需根据目标平台适配（如 `Sheet` 仅在 macOS 生效）。

- **核心类型与提示分离**：`WindowType_Mask` 用于提取“核心类型”（如从组合标志中分离出 `Window`/`Dialog`），例如：

```python
# 获取窗口的核心类型（过滤提示标志）
core_type = window.windowFlags() & WindowType.WindowType_Mask
```
