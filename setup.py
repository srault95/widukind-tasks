#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

from widukind_tasks import version

setup(name='widukind-tasks',
	version=version.version_str(),
    description='Celery tasks for dlstats project',
    author='Widukind team',
    url='https://github.com/srault95/widukind-tasks', 
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
		'nose>=1.0',
		'coverage',
		'flake8'
	],
	test_suite='nose.collector',		
)

        
