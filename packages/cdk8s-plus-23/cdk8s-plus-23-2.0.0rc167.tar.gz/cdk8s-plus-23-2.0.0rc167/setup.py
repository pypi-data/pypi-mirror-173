import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk8s-plus-23",
    "version": "2.0.0.rc167",
    "description": "cdk8s+ is a software development framework that provides high level abstractions for authoring Kubernetes applications. cdk8s-plus-23 synthesizes Kubernetes manifests for Kubernetes 1.23.0",
    "license": "Apache-2.0",
    "url": "https://github.com/cdk8s-team/cdk8s-plus.git",
    "long_description_content_type": "text/markdown",
    "author": "Amazon Web Services",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cdk8s-team/cdk8s-plus.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk8s_plus_23",
        "cdk8s_plus_23._jsii",
        "cdk8s_plus_23.k8s"
    ],
    "package_data": {
        "cdk8s_plus_23._jsii": [
            "cdk8s-plus-23@2.0.0-rc.167.jsii.tgz"
        ],
        "cdk8s_plus_23": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "cdk8s>=2.5.25, <3.0.0",
        "constructs>=10.1.137, <11.0.0",
        "jsii>=1.70.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
