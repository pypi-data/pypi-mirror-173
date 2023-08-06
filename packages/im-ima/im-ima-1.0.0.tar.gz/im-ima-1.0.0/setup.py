from distutils.core import setup
from setuptools import find_packages

with open("README.rst", "r",encoding='utf-8') as f:
  long_description = f.read()

setup(name='im-ima',  # 包名
      version='1.0.0',  # 版本号
      description='关于Arduino主板的python库',
      long_description=long_description,
      author='iM智慧编程',
      author_email='317393374@qq.com',
      url='',
      install_requires=[],
      license='BSD License',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Topic :: Software Development :: Libraries'
      ],
      )