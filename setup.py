from setuptools import setup

setup(
    name='exitnaver',
    version='0.2.2',
    author='Jihyeok Seo',
    author_email='me@limeburst.net',
    url='https://github.com/limeburst/exitnaver',
    description='Exports your Naver blog in Markdown format.',
    long_description=open('README.rst').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    license='GPL',
    packages=['exitnaver'],
    install_requires=['html2text', 'BeautifulSoup', 'python-dateutil'],
    scripts=['bin/exitnaver']
)
