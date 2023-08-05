# import pathlib
# from setuptools import find_packages, setup, find_namespace_packages


# here = pathlib.Path(__file__).parent.resolve()
# install_requires = (here / 'requirements.txt').read_text(encoding='utf-8').splitlines()

# VERSION='0.0.12'
# DESCRIPTION = 'Auto sorting tool to allow you organise any file or folder in a directory using the file extensions'

# with open("README.md", "r") as fh:
#     long_description=fh.read()

# setup(
#     #name="sortmyfolder",
#     version=VERSION,
#     description=DESCRIPTION,
#     #package_dir={'':'auto_group'},
#     long_description=long_description,
#     long_description_content_type="text/markdown",
#     packages=find_namespace_packages(
#         where=['auto_group', 'auto_group.*']
#     ),
#     include_package_data=True,
#     install_requires=install_requires,
#     keywords=['python', 'automation', 'sorting'],
#     classifiers=[
#         "Development Status :: 1 - Planning",
#         "Intended Audience :: Developers",
#         "Operating System :: Unix",
#         "Operating System :: MacOS :: MacOS X",
#         "Operating System :: Microsoft :: Windows",
#     ],
#     entry_points={
#         'console_scripts': [
#             'sortmyfolder=auto_group.determine_location:main',
#         ],
#     },
# )


from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.16'
DESCRIPTION = 'folder sorting python code'
LONG_DESCRIPTION = 'A package that allows to build simple streams of video, audio and camera data.'

# Setting up
setup(
    name="sortmyfolder",
    version=VERSION,
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages('auto-group'),
    install_requires=['opencv-python', 'pyautogui', 'pyaudio', "shutil"],
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)