import codecs
import os
import re
import sys

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    # intentionally *not* adding an encoding option to open, See:
    #   https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]",
        version_file,
        re.M,
    )
    if version_match:
        return version_match.group(1)

    raise RuntimeError("Unable to find version string.")


long_description = read('README.rst')

setup(name='TripleAgent',
      version=find_version("triple_agent", "__init__.py"),
      description='SpyParty Timeline Parser',
      long_description=long_description,
      author='Andrew Zwicky',
      author_email='andrew.zwicky@gmail.com',
      license='MIT',
      url='https://github.com/andrewzwicky/TripleAgent',
      package_dir={"": "triple_agent"},
      packages=find_packages(where="src",
                             exclude=["tests*"],),
      package_data={'triple_agent': ['portraits/*.png', 'VERSION'],
                    '': ['LICENSE', 'README.rst']},
      python_requires='>=3.6',
      install_requires=['pyautogui>=0.9.42',
                        'opencv-python>=4.1.0.25',
                        'mss>=4.0.3',
                        'pytesseract>=0.2.6',
                        ],
      setup_requires=["pytest-runner>=4.4"],
      tests_require=["pytest>=4.5.0"],
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: MIT License',
          'Operating System :: Microsoft :: Windows',
          'Topic :: Games/Entertainment :: First Person Shooters',
          'Topic :: Multimedia :: Graphics :: Capture :: Screen Capture',
          'Topic :: Utilities',
          'Programming Language :: Python :: 3 :: Only',
          'Programming Language :: Python :: 3.6',
      ]
)