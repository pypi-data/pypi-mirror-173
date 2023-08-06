from setuptools import setup

with open('README.rst', encoding='utf-8') as f:
	LONG_DESCRIPTION = f.read()

setup(
	name='tlplib',
	version='1.0.2',
	description='k',
	author_email='yd@qq.com',
	author='yz',
	license='MIT',
	packages=['tlplib'],
	long_description=LONG_DESCRIPTION
)