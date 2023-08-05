"""
   File Name：     setup.py
   Description :
   Author :       abhay
   date：          2022/10/24
   University: Chengdu University of Technology.
"""
import setuptools
with open('README.md','r',encoding='utf8') as f:
    long_description = f.read()

setuptools.setup(
    name='PyGeoTimes',
    version='1.1',
    author = 'Abhay He',
    author_email = '1452245133@qq.com',
    description = 'PyGeoTimes extract geological Times from English texts',
    long_description = long_description,
    long_description_content_type="text/markdown",
    packages = setuptools.find_packages(),
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # 依赖模块
    install_requires = [
        'pillow',
    ],
    python_requires = '>=3'


)