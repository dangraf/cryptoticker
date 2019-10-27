from setuptools import setup, find_packages


# https://stackoverflow.com/questions/26528178/right-way-to-set-python-package-with-sub-packages
# https://docs.python.org/3/distutils/examples.html

setup(name='cryptoticker',
      description="Library to fetch crypto currancy data and save to mongodb",
      author="Daniel Grafstrom",
      version='1.0.0',
      license='GPLv3',
      packages=find_packages(exclude=['tests']),
      install_requires=['mongoengine',
                        'pymongo',
                        'pandas',
                        'newspaper3k',
                        'krakenex',
                        'requests',
                        'schedule',
                        'datetime',
                        'pytest',
                        'flask'],
      )
