from setuptools import setup, find_packages

setup(
	name='fixedpt',
	version='0.1.1',

	url='https://github.com/UnsignedByte/fixedpt',
	author='Edmund Lam',
	
	package_dir={'':'./'},
	# py_modules=['fixedpt'],
	packages=find_packages(where='./'),
)
