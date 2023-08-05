import distutils.spawn
from setuptools import find_packages
from setuptools import setup
import shlex
import subprocess
import sys

install_requires = [
    'PyQt5',
    'openpyxl'
]

if sys.argv[1] == 'release':
    if not distutils.spawn.find_executable('twine'):
        print(
            'Please install twine:\n\n\tpip install twine\n',
            file=sys.stderr,
        )
        sys.exit(1)

    commands = [
        'python setup.py sdist',
        'twine upload dist/zhou_stattool-{:s}.tar.gz'.format('0.0.7'),
    ]
    for cmd in commands:
        subprocess.check_call(shlex.split(cmd))
    sys.exit(0)


def get_long_description():
    with open('README.md', 'r') as f:
        long_description = f.read()
    return long_description


setup(
    name='zhou_stattool',
    version='0.0.7',
    packages=find_packages(),
    description='statistic tool for zhou',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    author='Frederic',
    author_email='fk1010098686@outlook.com',
    install_requires=install_requires,
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
    ],
    package_data={'zhou_stattool': ['icons/*', ]},
    entry_points={
        'console_scripts': [
            'zhou_stattool=zhou_stattool.app:main',
        ],
    },
)
