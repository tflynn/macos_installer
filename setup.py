from setuptools import setup, find_packages

setup(name='macos_installer',
      version='0.1',
      description='macOS installer for any type of macOS packages',
      url='https://github.com/tflynn/macos_installer.git',
      author='Tracy Flynn',
      author_email='tracysflynn@gmail.com',
      license='MIT',
      packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
      install_requires=['standard_logger>=0.3', 'run_command>=0.2'],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)

