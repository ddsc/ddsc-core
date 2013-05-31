from setuptools import setup

version = '1.0'

long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CREDITS.rst').read(),
    open('CHANGES.rst').read(),
    ])

install_requires = [
    'Django',
    'cassandralib',
    'django-extensions',
    'django-nose',
    'django-treebeard',
    'lizard-security',
    'lizard-ui >= 4.0b5',
    'networkx',
    'pandas',
    'python-magic',
    'pytz',
    'tslib',
    ],

tests_require = [
    ]

setup(name='ddsc-core',
      version=version,
      description="DDSC core library",
      long_description=long_description,
      # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Programming Language :: Python',
                   'Framework :: Django',
                   ],
      keywords=[],
      author='DDSC',
      author_email='ddsc@dijkdata.nl',
      url='git@github.com:ddsc/ddsc-core.git',
      license='MIT',
      packages=['ddsc_core'],
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require={'test': tests_require},
      entry_points={
          'console_scripts': [
          ]},
      )
