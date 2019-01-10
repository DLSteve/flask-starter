"""
flask-starter
--------------
Flask-starter is a starter flask project with Azure and Kubernetes support. 
Links
`````
* `documentation <#>`_
"""
from setuptools import setup, find_packages

setup(
    name='flask-starter',
    version='0.2.0',
    long_description=__doc__,
    packages=find_packages(exclude=['tests', 'tests.*']),
    url='',
    author='Steve',
    author_email='darksle@gmail.com',
    license='MIT',
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    install_requires=[
        'Flask',
        'Flask-Login',
        'Flask-Migrate',
        'Flask-SQLAlchemy',
        'Flask-WTF',
        'Flask-SSLify',
        'SQLAlchemy',
        'SQLAlchemy-Utils',
        'Flask-Azure-Storage',
        'celery[redis]',
        'WTForms',
        'redis',
        'flask-restplus',
        'python-dateutil',
        'gunicorn',
        'bleach',
        'requests',
        'flask_oauthlib',
        'python-jose',
        'blinker',
        'chardet',
        'pymssql'
    ],
    extras_require={
        'tests': [
            'mock',
            'pytest',
            'pytest-flask',
            'pytest-cov'
        ]
    },
    entry_points={
        'console_scripts': [
            'iamctl=app.cli:main'
        ]
    }
)
