import os
from setuptools import setup, find_packages

__version__ = '0.0.4'  # 版本号
requirements = ["setuptools>=61.0","requests","tqdm"]  # 依赖文件

setup(
    name='easyPB',  # 在pip中显示的项目名称
    version=__version__,
    author='newrain',
    author_email='newrain_wang@163.com',
    url='',
    description='A simple download tool',
    # packages=find_packages(exclude=["tests"]),  # 项目中需要拷贝到指定路径的文件夹
    python_requires='>=3.6.5',
    install_requires=requirements  # 安装依赖
)
