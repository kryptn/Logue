from setuptools import setup

setup(name='Logue',
      packages=['Logue'],
      include_package_data=True,
      test_suite='Logue.tests',
      install_requires=['sanic',
                        'pyjwt',])

