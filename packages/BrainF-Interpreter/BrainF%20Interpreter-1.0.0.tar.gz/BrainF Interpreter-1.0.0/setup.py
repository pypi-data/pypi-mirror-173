from setuptools import setup, find_packages


setup(
    name='BrainF Interpreter',
    version='1.0.0',
    license='MIT',
    author="RavenVR",
    author_email='ravenvr@yahoo.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/RavenVR/bf-interpreter',
    keywords='BrainFuck',
)
