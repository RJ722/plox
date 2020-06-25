from setuptools import setup

setup(
    name="plox",
    version="0.1",
    description="Python implementation of the Lox programming language",
    keywords="compiler-design",
    author="Rahul Jha",
    author_email="rj722@protonmail.com",
    url="https://github.com/RJ722/plox",
    packages=["lox"],
    entry_points={
        "console_scripts": ["plox = lox.lox:main"],
    },
)
