from setuptools import setup

with open("README.md", "r") as arq:
	readme = arq.read()

setup(name='jmshow',
	version='0.0.1',
	license='MIT License',
	author='Jorge Martins',
	long_description=readme,
	long_description_content_type="text/markdown",
	author_email='jorgemartins72@gmail.com',
	keywords='panda video',
	description=u'Debugger simples',
	packages=['jmshow'],
	install_requires=['colorama'],)
