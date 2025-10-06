# AnimatedClass

## AnimatedColor(QObject)

- property

    | name | type | description |
    | ---- | ---- | ----------- |
    | color | QColor | 颜色值 |
    | animation | QPropertyAnimation| 属性动画 |

- method

    | name | description |
    | ---- | ----------- |
    | getColor |  |
    | setColor |  |
    | setColorTo |  |
    | transparent |  |
    | toTransparent |  |
    | opaque |  |
    | setAlpha |  |
    | setAlphaTo |  |

## AnimatedLinearGradient(QObject)

- property

    | name | type | description |
    | ---- | ---- | ----------- |
    | colorStart | QColor | 渐变开始颜色 |
    | colorEnd | QColor | 渐变结束颜色 |
    | reverse | Bool|  |
    | direction | ZDirection|  |
    | linearPoint | tuple[float, float, float, float]|  |
    | animationStart | QPropertyAnimation |  |
    | animationEnd | QPropertyAnimation |  |

- method

    | name | description |
    | ---- | ----------- |
    | getColorStart |  |
    | setColorStart |  |
    | getColorEnd |  |
    | setColorEnd |  |
    | setColorStartTo |  |
    | setColorEndTo |  |
    | setColors |  |
    | setColorsTo |  |
    | transparent |  |
    | toTransparent |  |
    | opaque |  |
    | toOpaque |  |
