import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='django-friendly-captcha',
    version='0.1.3',
    description='Django library for friendly captcha',
    long_description=read('README.rst'),
    url='https://github.com/christianwgd/django-friendly-captcha',
    download_url='',
    author='Christian Wiegand',
    author_email='christianwgd@gmail.com',
    maintainer='Christian Wiegand',
    maintainer_email='christianwgd@gmail.com',
    license='BSD',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=[
        'django',
        'requests'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    zip_safe=False,
)
