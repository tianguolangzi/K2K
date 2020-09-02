from setuptools import setup

__version__='1.0'
setup(name='K2K',
      version=str(__version__),
      description='Combine multiple files based on the same key consisting of one or more columns',
      long_description=open('README.rst').read(),
      author='Kun Zhang',
      license='MIT',
      author_email='tianguolangzi@gmail.com',
      url='https://github.com/tianguolangzi/K2K',
      packages=['K2K'],
      classifiers=[
          'Development Status :: 1 - Stable',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
          'Programming Language :: Python :: 3',
          'Topic :: Terminals'
          ],
      python_requires='>=3',
      scripts = ["bin/K2K"]
      )

if __name__ == '__main__':
    f = open("K2K/__init__.py",'w')
    f.write("__version__ = \'"+__version__+"\'"+"\n")
    f.close()