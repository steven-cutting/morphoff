from setuptools import setup, find_packages

with open("README.md") as fp:
    THE_LONG_DESCRIPTION = fp.read()


setup(
    name="morphoff",

    # Semantic versioning. MAJOR.MINOR.MAINTENANCE.(dev1|a1|b1)
    version="0.0.0.dev1",


    description="",
    long_description=THE_LONG_DESCRIPTION,

    author='Steven Cutting',
    author_email='steven.e.cutting@gmail.com',

    classifiers=['Topic :: Scientific/Engineering :: Artificial Intelligence',
                 'Topic :: Scientific/Engineering :: Information Analysis',
                 'Topic :: Text Processing :: Linguistic',
                 'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
                 'Intended Audience :: Science/Research',
                 'Operating System :: Unix',
                 'Operating System :: POSIX :: Linux',
                 'Operating System :: MacOS :: MacOS X',
                 'Development Status :: 3 - Alpha',

                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',

                 'Development Status :: 2 - Pre-Alpha',
                 ],
    keywords='nlp text ngram ngrams Hebrew',
    packages=find_packages(exclude=('bin', 'tests', 'docker',
                                    'data', 'notebooks')),
    scripts=['scripts/morphoff'],
    # entry_points='''
    #     [console_scripts]
    #     htopic=scripts.htopic:cli
    # ''',
    install_requires=['toolz>=0.7.4',
                      'text2math>=0.0.8.dev1',
                      'h_topic_model>=0.0.0.dev1',
                      'Morfessor>=2.0.1',
                      'Morfessor_FlatCat',
                      'click>=6.7',
                      'arrow>=0.6.0',
                      ],
    extras_require={
        'fast': ['cytoolz>=0.7.3'],
        'dev': ['cytoolz>=0.7.3'],
        'test': ['pytest-runner>=2.6.2', 'pytest>=2.8.7', 'coverage>=4.3.4'],
    },
    setup_requires=['pytest-runner>=2.6.2'],
    tests_require=['pytest>=2.8.7'],
)
