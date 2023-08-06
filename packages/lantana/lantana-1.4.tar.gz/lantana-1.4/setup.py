from setuptools import setup, find_packages

VERSION = '1.4'

setup(
    name="lantana",
    version=VERSION,
    url='https://lantana.wsoft.ws',
    license='MIT',
    description='The simple mkdocs theme.',
    author='WSOFT',
    author_email='info@wsoft.ws',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['mkdocs>=1.1','mkdocs-material>=7.0','mkdocs-awesome-pages-plugin>=2.6'],
    python_requires='>=3.5',
    entry_points={
        'mkdocs.themes': [
            'lantana = lantana',
        ]
    },
    zip_safe=False
)