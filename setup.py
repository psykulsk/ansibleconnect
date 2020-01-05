import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()


def requirements(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
    return lines


setup(
    name='ansibleconnect',
    version='1.0.0',
    description='Connect to all hosts from the ansible inventory with one command',
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/psykulsk/ansibleconnect",
    author='Piotr Sykulski',
    author_email='pitersk@gmail.com',
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Topic :: Utilities',
        'Topic :: System :: Systems Administration'
    ],
    install_requires=requirements('requirements.txt'),
    packages=['ansibleconnect'],
    entry_points='''
    [console_scripts]
    ansibleconnect=ansibleconnect.main:main
    '''
)
