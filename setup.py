from setuptools import setup

setup(
    name='blog2md',
    version='0.2',
    author='Jihyeok Seo',
    author_email='me@limeburst.net',
    url='https://github.com/limeburst/blog2md',
    description='Exports your blog in Markdown format.',
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
    packages=['blog2md'],
    install_requires=['html2text', 'BeautifulSoup'],
    scripts=['bin/blog2md']
)
