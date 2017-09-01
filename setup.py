from setuptools import setup
import io
import sys
from fakr import version, repo_url, download_url, package_name, author, author_email

with io.open('README.rst', 'r', encoding='utf-8') as readme_file:
    readme = readme_file.read()

if sys.argv[-1] == 'readme':
    print(readme)
    sys.exit()

requirements = [
    'unidecode',
    'jinja2'
]

setup(
    name=package_name,
    version=version,
    description='Random data generator for the command line',
    long_description=readme,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3 :: Only',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Topic :: Software Development',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Testing :: Traffic Generation',
    ],
    keywords='fake template random list data generator Jinja2 ' + package_name,
    url=repo_url,
    author=author,
    author_email=author_email,
    license='MIT',
    install_requires=open('requirements.txt').read().lstrip().rstrip().split('\n'),
    tests_require=['nose2', 'cov-core'],
    test_suite='nose2.collector.collector',
    entry_points={
        'console_scripts': [
            '{n}={n}.cli:main'.format(n=package_name),
            '{n}-builder={n}.vocabulary_builder:main'.format(n=package_name),
        ],
    },
    include_package_data=True,
    zip_safe=False,
    packages=[package_name],
    package_dir={package_name: package_name + '/'},
    package_data={package_name: ['vocabularies/*.fakr']},
    download_url=download_url
)
