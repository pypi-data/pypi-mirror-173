# rayyan-store-py

Python client interface for RayyanStore.

## Publish

1. Increment the version number in `setup.py`
1. Install twine: `pip install twine`. You may need to upgrade pip first: `pip install --upgrade pip`
1. Create the distribution files: `python setup.py sdist bdist_wheel`
1. Optionally upload to [Test PyPi](https://test.pypi.org/) as a dry run: `twine upload -r testpypi dist/*`. You will need a separate account there
1. Upload to [PyPi](https://pypi.org/): `twine upload dist/*`
