import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ec5conn",
    version="0.0.3",
    author="jack.a",
    author_email="jack.a@kakaoent.com",
    description="ec5 conn",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/schooldevops/python-tutorials",
    # project_urls={
    #     "Bug Tracker": "https://github.com/schooldevops/python-tutorials/issues",
    # },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        'six==1.16.0',
        'termcolor==2.0.1',
        'pyfiglet==0.8.post1',
        'pydash==5.1.0',
        'PyInquirer==1.0.3',
        'ping3==4.0.3',
        'mysql-connector-python==8.0.31',
        'pymongo==4.3.2',
    ],
    scripts=['scripts/ec5conn'],
)
