from setuptools import setup, find_packages

setup(
    name='property_scraper',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'property_scraper=property_scraper:main'
        ]
    },
    install_requires=[
        'beautifulsoup4',
        'requests'
    ]
)
