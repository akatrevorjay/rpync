from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='rpync',
      version=version,
      description="Backup utility using rsync for the heavy work",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='backup rsync',
      author='Marc G\xc3\xb6ldner',
      author_email='',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points={'console_scripts': ['rpync = rpync.main:main'],},
      )
