# 编写完包源码后，python setup.py sdist生成pip压缩包
# 解压压缩包，python setup.py install  安装自己的包，就可以引用了


from distutils.core import setup
from setuptools import find_packages

setup(name='beihaitool',  # 包名
      version='2022.10.27',  # 版本号
      description='',
      long_description='',
      author='beihai',
      author_email='leileiliu_email@163.com',
      packages=find_packages(),
      long_description_content_type="text/markdown",
      license="GPLv3",
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
          "Operating System :: OS Independent",
      ],
      )
