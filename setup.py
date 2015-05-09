from setuptools import setup, find_packages

setup(
    name='dogebuild',
    version='0.1.0.dev2',
    description='Builder with plugin system',
    author='Kirill Sulim',
    author_email='kirillsulim@gmail.com',
    license='MIT',
    url='https://github.com/dogebuild/dogebuild',
    packages=find_packages(include=[
        'dogebuild*',
        ]),
    scripts=[
        'doge_script.py',
        ],
    entry_points={
        'console_scripts': [
            'doge = doge_script:run_doge',
            ],
    },
    test_suite='tests',
    install_requires=[
        'pip',
        'virtualenv',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development',
    ],
    keywords='dogebuild builder',
)
