from distutils.core import setup
from setuptools import find_packages

with open("README.rst", "r") as f:
  long_description = f.read()

setup(name='requestTools',  # 包名
      version='1.0.1',  # 版本号
      description='http request tools',
      long_description=long_description,
      author='trimNiu',
      author_email='fahongsun168@sina.com',
      url='',
      install_requires=[
        'requests'
      ],

      license='BSD License',
      packages=find_packages(),
      platforms=["all"],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python :: 3.8',
          'Topic :: Software Development :: Libraries'
      ],
      )