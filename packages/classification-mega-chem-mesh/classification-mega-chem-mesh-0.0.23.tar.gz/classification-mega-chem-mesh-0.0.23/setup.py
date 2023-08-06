# -*- coding: utf-8 -*-
# @Time : 2021/11/24 17:30
# @Author : EdwardTsai
# @Email : caiweimin@megarobo.tech
# @File : setup.py
# @Project : chem-mesh-notebook
# @Introduction :
import os
import setuptools

# 如果readme文件中有中文，那么这里要指定encoding='utf-8'，否则会出现编码错误
with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as readme:
    README = readme.read()

# 允许setup.py在任何路径下执行
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setuptools.setup(
    name="classification-mega-chem-mesh",  # 库名，需要在pypi中唯一
    version="0.0.23",  # 版本号
    author="Jinrui.Duan & Weimin.Cai",  # 作者
    author_email="caiweimin@megarobo.tech",  # 作者邮箱（方便使用者发现问题后联系我们）
    description="A Compound classification engine",  # 简介
    long_description="This is a private tool for compound classification",  # 详细描述（一般会写在README.md中）
    long_description_content_type="text/markdown",  # README.md中描述的语法（一般为markdown）
    url="https://gitee.com/chenmesh/chem-mesh-notebook",  # 库/项目主页，一般我们把项目托管在GitHub，放该项目的GitHub地址即可
    packages=setuptools.find_packages(),  # 默认值即可，这个是方便以后我们给库拓展新功能的
    classifiers=[  # 指定该库依赖的Python版本、license、操作系统之类的
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'numpy == 1.21.3',
        'rdkit-pypi == 2021.9.2',
    ],
    python_requires='>=3.6',
)
