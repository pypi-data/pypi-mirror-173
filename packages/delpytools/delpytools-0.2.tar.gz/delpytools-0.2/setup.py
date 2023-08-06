from setuptools import setup, find_packages


setup(
    name='delpytools',
    version='0.2',
    license='MIT',
    author="Alex Malainic",
    description = "Implementation of scripts to automate a data science project",
    author_email='amalainic@deloittece.com',
    packages=find_packages('init'),
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
