from setuptools import setup, find_packages


setup(
    name='example_publish_pypi_rajat',
    version='1.1',
    license='MIT',
    author="Rajat Mehta",
    author_email='rajatmehta1992@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='',
    keywords='example project',
    install_requires=[
          'numpy',
          'scipy'
      ],

)