from setuptools import setup
from setuptools import find_packages


try:
    from pypandoc import convert

    def get_long_description(file_name):
        return convert(file_name, 'rst', 'md')

except ImportError:

    def get_long_description(file_name):
        with open(file_name) as f:
            return f.read()


setup(
    name='dotplot',
    packages=find_packages(),
    version='0.4.4',
    license='LGPL-3.0',
    description='Small bioinformatic package for dotplot\'s generation (in command line and in GUI)',
    long_description=get_long_description('README.md'),
    author='kn_bibs',
    author_email='bibs.kn@uw.edu.pl',
    url='https://github.com/kn-bibs/dotplot',
    download_url='https://github.com/kn-bibs/dotplot/tarball/v0.4.4-alpha',
    keywords=['dotplot', 'bioinformatic', 'gui'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Utilities',
        'Environment :: X11 Applications :: Qt',
        'Environment :: Console',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'PyQt5',
        'matplotlib',
        'requests'
    ],
    scripts=['bin/dotplot'],
    package_data={
        'dotplot': ['matrices/*.txt']
    }
)
