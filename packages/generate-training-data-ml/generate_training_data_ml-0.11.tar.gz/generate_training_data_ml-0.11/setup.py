from setuptools import setup, find_packages
import codecs
import os

#change to dict
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(os.path.abspath(os.path.dirname(__file__)),'README.md'), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.11'
DESCRIPTION = "Great object detection results without spending a lot of time"

# Setting up
setup(
    name="generate_training_data_ml",
    version=VERSION,
    license='MIT',
    url = 'https://github.com/hansalemaos/generate_training_data_ml',
    author="Johannes Fischer",
    author_email="<aulasparticularesdealemaosp@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    #packages=['a_pandas_ex_less_memory_more_speed', 'imgaug', 'numpy', 'opencv_python', 'pandas', 'pascal_voc_writer', 'PILasOPENCV', 'regex', 'scikit_learn', 'tqdm'],
    keywords=['yolov5', 'yolo', 'training data', 'lazy', 'auto-generated'],
    classifiers=['Development Status :: 4 - Beta', 'Programming Language :: Python :: 3 :: Only', 'Programming Language :: Python :: 3.9', 'Topic :: Scientific/Engineering :: Visualization', 'Topic :: Software Development :: Libraries :: Python Modules', 'Topic :: Text Editors :: Text Processing', 'Topic :: Text Processing :: General', 'Topic :: Text Processing :: Indexing', 'Topic :: Text Processing :: Filters', 'Topic :: Utilities'],
    install_requires=['a_pandas_ex_less_memory_more_speed', 'imgaug', 'numpy', 'opencv_python', 'pandas', 'pascal_voc_writer', 'PILasOPENCV', 'regex', 'scikit_learn', 'tqdm'],
    include_package_data=True
)
#python setup.py sdist bdist_wheel
#twine upload dist/*