import setuptools
import codecs
import os.path




def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with codecs.open(os.path.join(here, rel_path)) as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    raise RuntimeError("Unable to find version string.")




with open('README.md', 'r') as fh:
    long_description = fh.read()

description = (
    'A package that connects to one or more PostgreSQL databases and allows '
    'you to retrieve a database connection when required. Depends on '
    'psycopg2-binary.'
)

setuptools.setup(
    name='pgsql-connection-handler',
    version=get_version('pg_connection_handler/__init__.py'),
    author='Armandt van Zyl',
    author_email='armandtvz@gmail.com',
    description=description,
    license='GPL-3.0',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/armandtvz/pgsql-connection-handler',
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
    ],
    python_requires=">=3.8, <4",
    install_requires=[
        'psycopg2-binary',
    ],
)
