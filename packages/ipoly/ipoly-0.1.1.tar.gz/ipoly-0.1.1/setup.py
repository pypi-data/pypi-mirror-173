from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
      name='ipoly',
      version='0.1.1',
      license='MIT',
      author="Thomas Danguilhen",
      author_email='thomas.danguilhen@estaca.eu',
      packages=['ipoly'],
      url='https://github.com/Danguilhen/ipoly',
      install_requires=[
            'pyarrow',
            'xlrd',
            'pandas',
            'scipy',
            'typeguard',
            'seaborn',
            'pylatex',
            'opencv-python',
		'imageio',
            'openpyxl'
      ],
      long_description=long_description,
      long_description_content_type='text/markdown'
)
