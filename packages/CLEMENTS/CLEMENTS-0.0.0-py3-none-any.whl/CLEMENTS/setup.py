import setuptools


setuptools.setup(
    name             = 'DNACLEMENT',
    version          = '0.0.0',
    description      = 'Genomic decomposition and reconstruction of non-tumor diploid subclones',
    author           = 'Young-soo Chung, M.D.',
    author_email     = 'goldpm1@yuhs.ac',
    url              = 'https://github.com/Yonsei-TGIL/CLEMENT',
    download_url     = 'https://github.com/Yonsei-TGIL/CLEMENT.git',
    install_requires = ['matplotlib>=3.5.2','seaborn>=0.11.2', 'numpy>=1.21.5', 'pandas>=1.3.4', 'scikit-learn>=1.0.2', 'scipy>=1.7.3', 'palettable>=3.3.0' ],
    keywords         = ['CLEMENT', 'genomic decomposition'],
    python_requires  = '>=3.6',
    package_data     =  {"" : "scripts"},
    #packages         = setuptools.find_packages(exclude = ['docs', 'tests*']),
    packages = setuptools.find_packages(where="scripts"),
    classifiers      = [
        'Programming Language :: Python :: 3.6',
        # "License :: Yonsei Univeristy College of Medicine, Republic of Korea",
        # "Operating System :: Linux",
    ]
)