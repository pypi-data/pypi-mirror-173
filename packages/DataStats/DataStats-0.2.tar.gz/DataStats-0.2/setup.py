from distutils.core import setup
setup(
  name = 'DataStats',
  packages = ['DataStats'],
  version = '0.2',
  license='MIT',   
  description = 'This library consists of obtaining data from an open database "statsbombpy".',
  author = 'Iñigo Ugarte & Paulo Cagigal',
  author_email = 'inigo.ugarte@alumni.mondragon.edu',
  url = 'https://github.com/pauloo1010/Paulo-Inigo-Progra',
  download_url = 'https://github.com/pauloo1010/Paulo-Inigo-Progra/archive/refs/tags/v_02.tar.gz',
  keywords = ['Dataset', 'Easy-working', 'Open'],
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