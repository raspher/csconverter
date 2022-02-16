from setuptools import setup, find_packages
import pathlib

long_description = (pathlib.Path(__file__).parent.resolve()/'README.md').read_text(encoding='utf-8')

setup(
    name='csconverter',
    description='ConnectionString Converter library',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/raspher/csconverter',
    version='0.1',
    author="Szymon Scholz",
    classifiers=[  # Optional
            # How mature is this project? Common values are
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 3 - Alpha',

            'Intended Audience :: Developers',
            'Topic :: Database',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Text Processing',
            'License :: OSI Approved :: The Unlicense (Unlicense)',
            'Operating System :: OS Independent',

            'Programming Language :: Python :: 3 :: Only',
        ],
    keywords='ConnectionString Converter connection string',
    py_modules=["csconverter"],
    python_requires='>=3.6, <4',
)
