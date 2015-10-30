#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

def strip(s):
	return s.strip("\"'")

def version(filepath):
	import re
	import os	
	re_vers = re.compile(r'VERSION\s*=.*?\((.*?)\)')
	here = os.path.abspath(os.path.dirname(__file__))
	with open(os.path.join(here, filepath)) as fp:
		for line in fp:
			m = re_vers.match(line.strip())
			if m:
				v = list(map(strip, m.groups()[0].split(', ')))
				return "{0}.{1}.{2}".format(*v[0:3])

setup(name='widukind-tasks',
	version=version('widukind_tasks/version.py'),
    description='Celery tasks for dlstats project',
    author='Widukind team',
    url='https://github.com/Widukind/widukind-tasks', 
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
	entry_points={
		'console_scripts': [
			'widukind-tasks = widukind_tasks.celeryapp:main',
			'widukind-tasks-cli = widukind_tasks.client:main',
		],
	},			
	tests_require=[
		'nose>=1.0'
		'coverage',
		'flake8'
	],
	test_suite='nose.collector',		
)

        
