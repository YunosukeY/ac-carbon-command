.PHONY: test testup testinst

test:
	@python3 setup.py test

testup:
	@rm -rf accarbon.egg-info dist build
	@pandoc --from markdown --to rst README.md -o README.rst
	@python3 setup.py sdist bdist_wheel
	@twine upload --repository testpypi dist/*

testinst:
	@pip3 --no-cache-dir install --upgrade --index-url https://test.pypi.org/simple/ accarbon

exec:
	@python3 -m accarbon_command.main https://atcoder.jp/contests/abc170/submissions/14465204?lang=ja