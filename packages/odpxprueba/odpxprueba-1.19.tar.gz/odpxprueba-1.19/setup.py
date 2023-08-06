
from distutils.core import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
  name = 'odpxprueba',        
  packages = ['odpxprueba'],   
  version = '1.19',     
  license='MIT',       
  description = 'The fundamental toolkit for outliers search and visualization',   
  author = 'Iker Cumplido',                   
  author_email = 'ikumpli@gmail.com',      
  url = 'https://github.com/ikumpli/odpxprueba/',   
  download_url = 'https://github.com/ikumpli/odpxprueba/archive/refs/tags/1.19.tar.gz',    
  keywords = ['OUTLIERS', 'VISUALIZATION', 'PANDAS'],   
  long_description=long_description,
  long_description_content_type='text/markdown',
  install_requires=[           
          'pandas',
          'numpy',
          'seaborn',
          'scipy',
          'matplotlib',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',    
    'Intended Audience :: Developers',     
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)