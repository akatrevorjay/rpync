from setuptools import setup, find_packages
import sys, os

version = '0.1alpha0'

setup(name='rpync',
      version=version,
      description="Backup utility using rsync for the heavy work and ssh for transport",
      long_description="""\
""",
      # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: Unix",
        "Programming Language :: Python :: 2",
        "Topic :: System :: Archiving :: Backup",
      ],
      keywords='backup rsync',
      author='Marc G\xc3\xb6ldner',
      author_email='',
      url='https://github.com/cramren/rpync',
      license='GPL',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points={
        'console_scripts': [
            'rpync = rpync.client.main:main',
            'rpync-agent = rpync.agent.main:main',
            'rpync-server = rpync.server.main:main',
        ],
      },
)
