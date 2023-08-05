import setuptools

file = open("README.md")
long_description = file.read()
file.close()

setuptools.setup(
	name="inputer",
	version="0.0.2",
	author="Time-Coder",
	author_email="binghui.wang@foxmail.com",
	description="Print before input",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/Time-Coder/inputer",
	packages=setuptools.find_packages(),
	install_requires=[
		"click"
	],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent"
	],
)