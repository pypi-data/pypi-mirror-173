from setuptools import setup, find_packages

classifiers = [
	'Development Status :: 5 - Production/Stable',
	'Intended Audience :: Education',
	'Programming Language :: Python :: 3',
	'License :: OSI Approved :: MIT License',
	'Operating System :: MacOS :: MacOS X',
	'Operating System :: Microsoft :: Windows',
	]
setup(
	name = 'kidofft',
	version = '0.0.1',
	description = 'A basic FFT audio file function',
	# long_description = open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
	url = '',
	author = 'KiDo Ruan',
	author_email = 'lxfamily123@gmail.com',
	license = 'MIT',
	classifiers = classifiers,
	keywords = 'FFT',
	packages = find_packages(),
	install_requires = ['']
)