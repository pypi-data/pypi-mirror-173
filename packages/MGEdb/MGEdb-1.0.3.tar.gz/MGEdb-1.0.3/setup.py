from distutils.util import convert_path
from setuptools import find_packages, setup
import pathlib


DATA_DIR = 'data'

# Get the long description from the README file
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(name='MGEdb',
      version='1.0.3',
      description='Mobile Genetic Element database',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://bitbucket.org/mhkj/mgedb/',
      author='Markus Johansson',
      author_email='markus.johansson@me.com',
      license='GPLv3',
      python_requires='>=3.6',
      packages=find_packages(exclude=('tests',)),
      include_package_data=True,
      package_data={
          'mgedb': [
              '%s/*.json' % DATA_DIR,
              '%s/*.yml' % DATA_DIR,
              '%s/sequences.d/*.fna' % DATA_DIR,
              '%s/sequences.d/*.faa' % DATA_DIR,
          ],
      },
      entry_points={'console_scripts': ['mgedb=mgedb.cli:main']},
      tests_require=[
          'pytest', 'pytest-cov', 'mypy', 'flake8-bugbear', 'flake8-commas',
          'flake8-comprehensions', 'flake8-docstrings', 'flake8-isort',
          'flake8-polyfill', 'flake8-quotes', 'flake8-todo', 'flake8',
          'setuptools-markdown', 'pytest-runner',
      ],
      classifiers=[
          'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
      ])
