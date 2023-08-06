from setuptools import setup, find_packages


setup(
    name='delpytools',
    version='0.1',
    license='MIT',
    author="Alex Malainic",
    author_email='amalainic@deloittece.com',
    packages=find_packages('delpytools'),
    package_dir={'': 'delpytools'},
    url='https://github.com/AMDelo/delpytools',
    keywords='delpytools',
    install_requires=[
          'scikit-learn',
          'scipy', 
          'numpy', 
          'pandas', 
          'matplotlib', 
          'seaborn', 
          'optbinning'
      ],

)
