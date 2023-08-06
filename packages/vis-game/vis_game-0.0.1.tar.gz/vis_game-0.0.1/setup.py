from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='vis_game',
  version='0.0.1',
  description='a system reinforcement learning',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Ngo Xuan Phong',
  author_email='phong@vis-laboratory.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='vis_game', 
  packages=find_packages(),
  install_requires=[''] 
)