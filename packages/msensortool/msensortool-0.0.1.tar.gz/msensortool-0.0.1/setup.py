import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="msensortool",
    version="0.0.1",
    author="ischoi",
    author_email="ischoi@morai.ai",
    description="MORAI Sensor API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/schooldevops/python-tutorials",
    # project_urls={
        # "Bug Tracker": "https://github.com/schooldevops/python-tutorials/issues",
    # },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)