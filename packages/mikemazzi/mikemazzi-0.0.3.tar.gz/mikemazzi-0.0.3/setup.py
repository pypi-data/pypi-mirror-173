import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name="mikemazzi",
    version="0.0.3",
    author="Michele Marcucci, Davide Mazzitelli",
    author_email="test@email.it",
    description="Assignment pipeline",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/mik3sw/2022_assignment1_users_db",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)