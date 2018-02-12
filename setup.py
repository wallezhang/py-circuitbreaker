# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

version = 1.0

install_requires = [
]

test_requires = [
    "pytest>=3.4"
]

setup(name="py-circuitbreaker",
      version=version,
      description="Circuit Breaker for Python",
      keywords="python circuit breaker",
      author="Walle Zhang",
      author_email="doraemon.zh@gmail.com",
      packages=find_packages(exclude=['benchmark', 'docs', 'tests']),
      entry_points={},
      url="https://github.com/wallezhang/py-circuitbreaker",
      license="Apache Software License",
      zip_safe=False,
      install_requires=install_requires,
      tests_require=test_requires,
      python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
      classifiers=[
          "Topic :: Software Development",
          "Development Status :: 4 - Beta",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: Implementation :: CPython",
          "Programming Language :: Python :: Implementation :: PyPy",
      ])
