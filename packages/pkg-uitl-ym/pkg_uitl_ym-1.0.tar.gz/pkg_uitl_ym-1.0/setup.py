from distutils.core import  setup
import setuptools

packages = ['pkg_uitl_ym']# 唯一的包名，自己取名
setup(name='pkg_uitl_ym',
	version='1.0',
	author='ym',
    packages=packages, 
    package_dir={'requests': 'requests'},)
