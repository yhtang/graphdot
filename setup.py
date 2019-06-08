from setuptools import setup, find_packages
import io
import graphdot


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


long_description = read('README.md')


setup(
    name='graphdot',
    version=graphdot.__version__,
    url='https://gitlab.com/yhtang/graphdot',
    license='TBD',
    author='Yu-Hang Tang',
    # tests_require=['pytest'],
    # install_requires=['Flask>=0.10.1',
    #                 'Flask-SQLAlchemy>=1.0',
    #                 'SQLAlchemy==0.8.2',
    #                 ],
    # cmdclass={'test': PyTest},
    author_email='Tang.Maxin@gmail.com',
    description='GPU-accelerated graph similarity measurement library',
    long_description=long_description,
    packages=['graphdot'],
    # include_package_data=True,
    platforms='any',
    # test_suite='sandman.test.test_sandman',
    classifiers=[
        'Programming Language :: Python',
        # 'Development Status :: 4 - Beta',
        # 'Natural Language :: English',
        # 'Environment :: Web Environment',
        # 'Intended Audience :: Developers',
        # 'License :: OSI Approved :: Apache Software License',
        # 'Operating System :: OS Independent',
        # 'Topic :: Software Development :: Libraries :: Python Modules',
        # 'Topic :: Software Development :: Libraries :: Application Frameworks',
        # 'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    extras_require={
        # 'testing': ['pytest'],
    }
)
