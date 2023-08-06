import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="yu_twinkle",
    version="0.0.2",
    author="Kevin Yu",
    author_email="wmjx691@gmail.com",
    description="Twinkle project functions.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wmjx691/yu_twinkle",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
