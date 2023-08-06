import io
import re

from setuptools import setup

with io.open("README.md", "rt", encoding="utf8") as f:
    readme = f.read()

with io.open("kube_bench_report_converter/__init__.py", "rt", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read(), re.M).group(1)

setup(name='kube-bench-report-converter',
      version=version,
      description='Converts kube-bench checks console output to CSV.',
      long_description=readme,
      long_description_content_type="text/markdown",
      keywords='kube-bench report convert csv',
      url='https://github.com/build-failure/kube-bench-report-converter',
      project_urls={
          "Code": "https://github.com/build-failure/kube-bench-report-converter",
          "Issue tracker": "https://github.com/build-failure/kube-bench-report-converter/issues",
      },
      author='Michael Lewkowski',
      author_email='michael@lewkowski.de',
      maintainer="Michael Lewkowski",
      maintainer_email="michael@lewkowski.de",
      license='MIT',
      packages=['kube_bench_report_converter'],
      python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*,!=3.5.*',
      install_requires=[],
      classifiers=[
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Programming Language :: Python :: 3.8",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      zip_safe=False,
      entry_points={
          'console_scripts': ['kube-bench-report-converter=kube_bench_report_converter.command_line:main'],
      }
      )
