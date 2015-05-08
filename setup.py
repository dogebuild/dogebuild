from setuptools import setup, find_packages

setup(
    name='dogebuild',
    version='0.1',
    description="""\

    """,
    author='Kirill Sulim',
    author_email='kirillsulim@gmail.com',
    url='https://github.com/dogebuild/dogebuild',
    packages=find_packages(include=[
        'dogebuild*',
        ]),
    scripts=['doge_script.py'],
    entry_points={
        'console_scripts': ['doge = doge_script:run_doge'],
    },
    test_suite='tests',
)
