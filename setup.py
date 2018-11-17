from setuptools import setup
import re
import os.path


with open('tenmactl/__init__.py') as f:
    version = re.search(r'__version__\s+=\s+\'(.*)\'', f.read()).group(1)


desc_path = os.path.join(os.path.dirname(__file__), 'README.rst')
with open(desc_path) as desc_file:
    long_description = desc_file.read()


setup(
    name='tenmactl',
    version=version,
    url='https://bitbucket.org/teslabs/tenmactl',
    author='Gerard Marull-Paretas',
    author_email='gerard@teslabs.com',
    packages=['tenmactl'],
    license='MIT',
    description='Tenma power supplies control utility.',
    long_description=long_description,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3 :: Only'
    ],
    install_requires=['pyserial']
)
