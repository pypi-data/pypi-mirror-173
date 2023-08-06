from setuptools import setup, find_packages
 
setup(name='PrintableTree',
      packages=['PrintableTree'],
      version='0.1',
      url='https://github.com/klingerkrieg/pyPrintableTree',
      download_url='https://github.com/klingerkrieg/pyPrintableTree/archive/refs/tags/0.1.tar.gz',
      license='MIT',
      author='Alan Klinger',
      author_email='klingerkrieg@gmail.com',
      description='It has an implementation of a tree in python and methods that print the tree to an image through OpenCV',
      long_description=open('README.md').read(),
      zip_safe=False,
      install_requires=[            # I get to this in a second
          'opencv-python',
          'numpy',
          'matplotlib',
      ])
