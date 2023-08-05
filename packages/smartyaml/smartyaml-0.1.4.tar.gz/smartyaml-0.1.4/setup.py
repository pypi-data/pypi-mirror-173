from setuptools import find_packages, setup

setup(
  name = 'smartyaml',
  packages = find_packages(include = ['smartyaml']),
  version = '0.1.4',    
  description = 'SMART Yaml library',  
  long_description = 'SMART Yaml library',
  long_description_content_type = 'text/x-rst',
  author = 'Foo, Ji-Haw',
  author_email = 'foojihaw@hotmail.com',
  license = 'BSD 2-Clause',
  install_requires = [],
  setup_requires = ['pytest-runner'],
  tests_require = ['pytest'],
  test_suite = 'tests'
)