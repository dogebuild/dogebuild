from setuptools import setup, find_packages
from os import path


project_directory = path.abspath(path.dirname(__file__))
data_files = []


def load_from(file_name):
    data_files.append(file_name)
    with open(path.join(project_directory, file_name), encoding='utf-8') as f:
        return f.read()


setup(
    name='dogebuild',
    version=load_from('dogebuild.version').strip(),
    description='Builder with plugin system',
    url='https://github.com/dogebuild/dogebuild',
    author='Kirill Sulim',
    author_email='kirillsulim@gmail.com',
    license='MIT',
    packages=find_packages(include=[
        'dogebuild',
    ]),
    scripts=[
        'scripts/doge_runner.py',
    ],
    entry_points={
        'console_scripts': [
            'doge = doge_runner:main',
        ],
    },
    test_suite='tests',
    install_requires=[
        'pip',
        'virtualenv',
        'toposort==1.5',
        'colorlog==4.0.2',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
    ],
    keywords='dogebuild builder',
)
