from setuptools import setup, find_packages

setup(
    name='dogebuild',
    version='0.0.1',
    description='Builder with plugin system',
    author='Kirill Sulim',
    author_email='kirillsulim@gmail.com',
    license='MIT',
    url='https://github.com/dogebuild/dogebuild',
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
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
    ],
    keywords='dogebuild builder',
)
