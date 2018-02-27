import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='drf-secure-token',
    version='1.0.3',
    packages=['drf_secure_token', 'drf_secure_token/migrations'],
    include_package_data=True,
    license='BSD License',
    description='Add secure token to djnago-rest-framework',
    long_description=README,
    url='',
    author='Tima Akulich',
    author_email='tima.akulich@gmail.com',
    install_requires=['djangorestframework', ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',  # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
