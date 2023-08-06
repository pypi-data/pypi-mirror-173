from setuptools import setup,find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='easyVisualize',
  version='0.0.1',
  description='prepared for basic EDA operations',
  long_description_content_type="text/markdown",
  long_description=open('README.txt').read(),
  url='https://github.com/TolgaTANRISEVER/EDA_functions',
  author='Tolga TANRISEVER',
  author_email='tanrisevertolga@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='EDA', 
  packages=find_packages(include=['easyVisualize']),
  install_requires=['pandas' , 'scikit-learn' , 'numpy','plotly'],
)