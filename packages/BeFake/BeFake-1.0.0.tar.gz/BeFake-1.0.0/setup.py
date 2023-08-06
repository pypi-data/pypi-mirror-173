import setuptools

setuptools.setup(
    name='BeFake',
    version='1.0.0',
    description='BeReal Python API wrapper',
    long_description=open('README.md').read(),
    url='https://github.com/notmarek/BeFake',
    author='Marek Veselý',
    license='Unlicense',
    entry_points={'console_scripts': ['befake=BeFake.__main__:cli']},
    packages=setuptools.find_packages(),
    install_requires=["click==8.1.3", "httpx==0.23.0", "pendulum==2.1.2", "pillow==9.2.0"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: The Unlicense (Unlicense)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet',
        'Topic :: Multimedia :: Graphics'
    ],
)