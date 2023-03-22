from setuptools import setup, find_packages

setup(
    name='finny_scraper',
    version='0.2',
    description='A property scraper for MLS entries',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4',
        'requests',
    ],
)