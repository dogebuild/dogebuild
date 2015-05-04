from setuptools import setup

setup(
    name='doge',
    version='0.1',
    description='Some description, IDK, wow!',
    author='Kirill Sulim',
    author_email='kirillsulim@gmail.com',
    url='https://github.com/dogebuild/dogebuild',
    scripts=["doge_script.py"],
    entry_points={
        'console_scripts': ['doge = doge_script:run_doge'],
    }
)
