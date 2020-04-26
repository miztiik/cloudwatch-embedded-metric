import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="cloudwatch_embedded_metric",
    version="0.0.1",

    description="cloudwatch_embedded_metric",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="Mystique",

    package_dir={"": "cloudwatch_embedded_metric"},
    packages=setuptools.find_packages(where="cloudwatch_embedded_metric"),

    install_requires=[
        "aws-cdk.core==1.35.0",
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "License :: OSI Approved :: Apache Software License",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)
