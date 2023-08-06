from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
  name = 'DataStats',
  packages = ['DataStats'],
  version = '0.3',
  license='MIT',   
  description = 'This library consists of obtaining data from an open database "statsbombpy".',
  author = 'Iñigo Ugarte & Paulo Cagigal',
  author_email = 'inigo.ugarte@alumni.mondragon.edu',
  url = 'https://github.com/pauloo1010/Paulo-Inigo-Progra',
  download_url = 'https://github.com/pauloo1010/Paulo-Inigo-Progra/archive/refs/tags/v_03.tar.gz',
  keywords = ['Dataset', 'Easy-working', 'Open'],
  long_description=long_description,
  long_description_content_type='text/markdown',
  install_requires=[
          'pandas',
          'statsbombpy',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha', 
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.10'
  ],
)


