# Release Guide 

Right now, the steps to make a release are somewhat manual. As the project matures, we will work to automate some of these steps. 

Currently the folks who have credentials to make releases on [PyPI](https://pypi.org/project/mt-metadata/) and [Conda-Forge](https://anaconda.org/conda-forge/mt-metadata) are:
- [@kkappler](https://github.com/kkappler/)
- [@kujaku11](https://github.com/kujaku11/)
- [@lheagy](https://github.com/lheagy/)

## Updating the version 

This project uses semantic versioning `major.minor.patch`, and you can use the [`bumpversion` package](https://github.com/c4urself/bump2version/#installation) to update the version. From a clean branch state on the `main` branch you can run `bumpversion <major / minor / patch>` to update the package version. Please then push this update. 

## Generate a release on GitHub

Once you have pushed an update to the software version, you can create a tag and associated release notes on GiHub: https://github.com/kujaku11/mt_metadata/releases/new 

## Upload to PyPI 

To upload to PyPI, first make sure you have [`twine`](https://twine.readthedocs.io/en/latest/) installed locally. Next, if you would like to test the release, you can follow the guide from [TestPyPI](https://packaging.python.org/guides/using-testpypi/). Otherwise, if you have the appropriate credentials (if not, contact one of the folks above who have PyPI authority for the project) you can run 

```
python setup.py sdist bdist_wheel
```

to build the distribution, followed by 

```
twine upload --skip-existing dist/*
```

to upload the package to the [PyPI server](https://pypi.org/project/mt-metadata)

## Update on Conda Forge 

We setup conda forge following these [instructions](https://conda-forge.org/docs/maintainer/adding_pkgs.html) and using the [grayskull package](https://github.com/marcelotrevisani/grayskull). At this stage, all that should be needed is to merge pull requests that are made on the [conda-forge feedstock](https://github.com/conda-forge/mt-metadata-feedstock). Note that if there are updates to the project dependencies, these files will need to be manually updated. 
