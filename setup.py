import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='django-friendly-captcha',
    version='0.1.11',
    description='Django library for friendly captcha',
    long_description=read('README.rst'),
    long_description_content_type='text/x-rst',
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
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    zip_safe=False,
)
