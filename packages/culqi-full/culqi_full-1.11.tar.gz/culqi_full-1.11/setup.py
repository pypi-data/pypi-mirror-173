import setuptools
from sys import version

if version < '2.2.3':
	from distutils.dist import DistributionMetadata
	DistributionMetadata.classifiers = None
	DistributionMetadata.download_url = None
	
from distutils.core import setup

setuptools.setup(
                    name='culqi_full',
                    version='1.11',
                    author='@rockscripts',
                    author_email='rockscripts@gmail.com',
                    description='CULQI',
                    long_description="CULQI",
                    install_requires=[],
                    include_package_data=True,
                    platforms='any',
                    url='https://instagram.com/rockscripts/',
                    packages=['culqi_full',],
                    python_requires='>=2.7.*',
                )