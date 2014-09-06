import sys
from setuptools import setup, find_packages

sys.path.append('/opt/vag/')

setup(
	name='vag',
	version="0.3",
	description='Varnish Administration GUI',
	author='Carlos Augusto Malucelli',
	author_email='carlos@carlosmalucelli.com',
	url='http://github.com/nopp/vag',
	packages = ['vag'],
	package_dir={'vag': 'vag'},
	package_data={'vag': ['lib/*']},
	data_files=[('/etc/vag/',['vag/config.cfg', 'vag/vag.sql']),
				('/etc/init.d/',['vag/init.d/vag'])],
	include_package_data=True,
	zip_safe=False,
	install_requires=['Flask']
)
