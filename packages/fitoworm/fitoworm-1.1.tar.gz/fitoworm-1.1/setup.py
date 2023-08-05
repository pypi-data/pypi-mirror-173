from distutils.core import  setup
import setuptools
packages = ['fitoworm']# 唯一的包名，自己取名
setup(name='fitoworm',
	version='1.1',
	author='ywz',
    packages=packages,
    package_dir={'requests': 'requests'},)
