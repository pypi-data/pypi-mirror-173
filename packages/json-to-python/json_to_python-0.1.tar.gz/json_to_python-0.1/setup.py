import pathlib

from setuptools import setup

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")
setup(name='json_to_python',
      version='0.1',
      description='converts api json responses to python objects',
      url='https://github.com/arokosaki/json_to_python',
      author='kobi kolodner',
      author_email='kobi@commugen.com',
      license='MIT',
      packages=['.'],
      classifiers=[
            'Development Status :: 2 - Pre-Alpha'
      ],
      long_description=long_description,  # Optional
      long_description_content_type="text/markdown",  # Optional (see note above)

)