import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    install_requires=[
        'PyATEMMax'
    ],
    extras_require={
        'dev': ['check-manifest']
    }
)