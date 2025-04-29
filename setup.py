from setuptools import setup, find_packages

setup(
    name='ZenUI',
    version='0.1.1',
    description='A UI library based on PySide6',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='ichinoseyuu',
    author_email='kirito1915914448@gmail.com',
    #url='https://github.com/yourusername/your_ui_library',
    packages=find_packages(),  # 自动查找并包含所有包
    # install_requires=[  # 依赖的其他库
    #     'pyside6',
    #     'Pywin32',
    #     'pywin32-ctypes'
    # ],
    # classifiers=[  # PyPi 上的分类信息
    #     'Development Status :: 3 - Alpha',
    #     'Intended Audience :: Developers',
    #     'Programming Language :: Python :: 3',
    #     'Programming Language :: Python :: 3.7',
    #     'Programming Language :: Python :: 3.8',
    #     'Programming Language :: Python :: 3.9',
    #     'Programming Language :: Python :: 3.10',
    #     'License :: OSI Approved :: MIT License',
    #     'Operating System :: OS Independent',
    # ],
)
