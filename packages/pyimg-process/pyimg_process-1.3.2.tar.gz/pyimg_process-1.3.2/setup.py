import pypandoc
from distutils.core import setup
#from pathlib import Path
#this_directory = Path(__file__).parent
#long_description = (this_directory / "README.md").read_text()
long_description = pypandoc.convert_file('README.md', 'rst')

setup(
  name = 'pyimg_process',         # How you named your package folder (MyLib)
  packages = ['pyimg_process'],   # Chose the same as "name"
  version = '1.3.2',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A simple package for image processing',   # Give a short description about your library
  author = 'Mikel Agirrebeitia & Jon Amelibia',                   # Type in your name
  author_email = 'jon.amelibia@alumni.mondragon.edu',      # Type in your E-Mail
  url = 'https://github.com/jonamelibia/pyimg-process',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/jonamelibia/pyimg-process/archive/refs/tags/1.3.2.tar.gz',    # I explain this later on
  keywords = ['SOME', 'MEANINGFULL', 'KEYWORDS'],   # Keywords that define your package best
  long_description_content_type="text/markdown",
  long_description=long_description,
  install_requires=[      
          'pypandoc',# I get to this in a second
          'numpy',
          'matplotlib',
          'opencv-python'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)
