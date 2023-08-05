from distutils.core import setup
import os.path

def get_file(*paths):
    path = os.path.join(*paths)
    try:
        with open(path, 'rb') as f:
            return f.read().decode('utf8')
    except IOError:
        pass

def get_readme():
    return get_file(os.path.dirname(__file__), 'README.rst')



setup(
  name = 'pigDetection',         # How you named your package folder (MyLib)
  packages = ['pigDetection'],   # Chose the same as "name"
  version = '0.0.1.4',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Show Loong Pom Name Jaaa',   # Give a short description about your library
  long_description='plese read in: https://github.com/UncleEngineer/loongpom',
  author = 'Bas Tatsana',                   # Type in your name
  author_email = 'tatsanasrisawang2@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/UncleEngineer/loongpom',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/TNPKpenguin',    # I explain this later on
  keywords = ['PigDetection', 'Pig', 'Detection', 'Pig classification'],   # Keywords that define your package best
  install_requires=[],

)
