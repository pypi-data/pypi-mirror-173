from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='Colorings',
    version='1.0.1',
    description='Color text(with hex,rgb...) and move Cursor',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Antech',
    author_email='antjules26@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='colors',
    packages=find_packages(),
    install_requires=['']
)