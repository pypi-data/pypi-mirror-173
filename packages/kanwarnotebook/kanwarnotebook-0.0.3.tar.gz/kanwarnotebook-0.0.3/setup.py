from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='kanwarnotebook',
  version='0.0.3',
  description='A very basic notebook',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Kanwar Adnan',
  author_email='kanwaradnanrajput@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='notebook', 
  packages=find_packages(),
  install_requires=[''] 
)