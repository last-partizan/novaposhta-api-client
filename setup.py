from setuptools import setup, find_packages


setup(
    name="novaposhta-api-client",
    version="0.2.3",
    description="Python client for Nova Poshta company's API",
    # long_description=open("README.md").read(),
    # long_description_content_type="text/markdown",
    author="semolex, fork by partizan",
    author_email="serg.partizan+novaposhta@gmail.com",
    url="https://github.com/last-partizan/novaposhta-api-client",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=["attrs>=19.2", "requests"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Environment :: Console",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
