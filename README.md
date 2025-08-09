# ZenUI

## How to use

### install

```powershell
pip install pyside6

python setup.py sdist
pip install ./dist/zenui-0.1.1.tar.gz
# or
python setup.py install
```

### uninstall

```powershell
pip uninstall ZenUI
```

### preview

![浅色主题预览](https://cdn.jsdelivr.net/gh/ichinoseyuu/Image/202505121700512.png)

![深色主题预览](https://cdn.jsdelivr.net/gh/ichinoseyuu/Image/202505121700783.png)

### gallery打包

```powershell
nuitka --mingw64 --show-progress --standalone --disable-console --remove-output  ./zenui_gallery/main.py
```
