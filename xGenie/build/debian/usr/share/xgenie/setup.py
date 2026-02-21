from setuptools import setup, find_packages

setup(
    name='xgenie',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'flask>=3.0.0',
        'requests>=2.31.0',
        'dnspython>=2.4.2',
        'python-whois>=0.8.0',
        'beautifulsoup4>=4.12.2',
        'lxml>=4.9.3',
        'cryptography>=41.0.7',
        'pyOpenSSL>=23.3.0',
        'selenium>=4.15.2',
        'aiohttp>=3.9.1',
        'scapy>=2.5.0',
        'python-nmap>=0.7.1',
        'builtwith>=1.3.15',
        'tldextract>=5.1.1',
        'validators>=0.22.0',
        'colorama>=0.4.6',
        'tabulate>=0.9.0',
        'pyyaml>=6.0.1',
        'jinja2>=3.1.2',
    ],
    entry_points={
        'console_scripts': [
            'xgenie=backend.cli:main',
        ],
    },
    author='xGenie Team',
    description='Security Intelligence Platform',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    python_requires='>=3.8',
)
