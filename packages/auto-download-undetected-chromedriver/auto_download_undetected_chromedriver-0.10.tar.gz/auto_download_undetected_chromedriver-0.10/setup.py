from setuptools import setup, find_packages
import codecs
import os

#change to dict
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)),'README.md'), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.10'
DESCRIPTION = "Script to automatically download the right undetected chromedriver version"

# Setting up
setup(
    name="auto_download_undetected_chromedriver",
    version=VERSION,
    license='MIT',
    url = 'https://github.com/hansalemaos/auto_download_undetected_chromedriver',
    author="Johannes Fischer",
    author_email="<aulasparticularesdealemaosp@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    #packages=['undetected_chromedriver'],
    keywords=['chromedriver', 'selenium', 'patched', 'bot', 'automation'],
    classifiers=['Development Status :: 4 - Beta', 'Programming Language :: Python :: 3 :: Only', 'Programming Language :: Python :: 3.9', 'Topic :: Scientific/Engineering :: Visualization', 'Topic :: Software Development :: Libraries :: Python Modules', 'Topic :: Text Editors :: Text Processing', 'Topic :: Text Processing :: General', 'Topic :: Text Processing :: Indexing', 'Topic :: Text Processing :: Filters', 'Topic :: Utilities'],
    install_requires=['undetected_chromedriver'],
    include_package_data=True
)
#python setup.py sdist bdist_wheel
#twine upload dist/*