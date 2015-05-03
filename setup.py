from setuptools import setup

setup(
    name='doge-script',
    version='0.1',
    description='Bla',
    author='Me',
    author_email='',
    url='',
    scripts=["doge.py"],
    entry_points={
        'console_scripts': ['rundoge = doge:da'],
    }
)
