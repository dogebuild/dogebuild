from setuptools import setup

setup(
    name='dogebuild',
    version='0.1',
    description='Some description, IDK, wow!',
    author='Kirill Sulim',
    author_email='kirillsulim@gmail.com',
    url='https://github.com/dogebuild/dogebuild',
    packages=[
        'dogebuild',
        'dogebuild.adapters',
        'dogebuild.loaders',
        'dogebuild.plugin',
        ],
    entry_points={
        'console_scripts': ['doge = doge_script:run_doge'],
    }
)
