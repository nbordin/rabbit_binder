import setuptools

with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='rabbit_binder',
    version='0.0.1',
    author='Nicolò Fabio Bordin',
    author_email='nicolofbordin@gmail.com',
    description='Python package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/nbordin/rabbit_binder',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: WTFPL',
        'Operating System :: OS Independent',
    ],
    install_requires=requirements,
)