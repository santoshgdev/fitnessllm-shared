"""Setup script for the fitnessllm_shared package."""
from setuptools import find_packages, setup

setup(
    name="fitnessllm_shared",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "cryptography>=41.0.0",
        "google-cloud-secret-manager>=2.16.0",
        "stravalib>=2.3,<3.0",
        "pydantic>=2.0,<3.0",
    ],
    author="Santosh G",
    author_email="santoshgdev@gmail.com",
    description="Shared utilities and interfaces for FitnessLLM platform",
    long_description=open("README.md").read() if open("README.md").readable() else "",
    long_description_content_type="text/markdown",
    url="https://github.com/santoshgdev/fitnessllm-shared",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
)
