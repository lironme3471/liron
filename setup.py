from setuptools import setup, find_packages

setup(
    name="evaluation-appeal-system",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "openai>=1.0.0",
        "pydantic>=2.0.0",
        "python-dateutil>=2.8.0",
    ],
    python_requires=">=3.8",
)
