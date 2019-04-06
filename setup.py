from setuptools import setup
import Emailer

setup(name='Emailer',
      version=Emailer.__version__,
      description='Helpers to make operations scripting easier.',
      author='Adam Stueckrath',
      author_email='stueckrath.adam@gmail.com',
      url='',
      packages=['Emailer'],
      install_requires=[],
      tests_require=[],
      package_data={},
      python_requires="<3",
)