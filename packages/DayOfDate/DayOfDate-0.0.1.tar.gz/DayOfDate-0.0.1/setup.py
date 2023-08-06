from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='DayOfDate',
    version='0.0.1',
    description='To find day for the given date',
    long_description=open('README.txt').read() + '\n\n' +
    open('CHANGElOG.txt').read(),
    url='',
    author='IndraKumarR',
    author_email='indra0207accs@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='day',
    packages=find_packages(),
    install_requires=['']
)
