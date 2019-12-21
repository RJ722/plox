from distutils.core import setup

setup(name='plox',
      version='0.1',
      packages=['lox'],
      entry_points={
            'console_scripts': ['plox = lox.lox:main'],
      },
)
