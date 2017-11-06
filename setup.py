from setuptools import setup, find_packages

setup(
    name='alpheios_nemo_ui',
    version="0.0.1",
    packages=find_packages(exclude=["examples", "tests"]),
    url='https://github.com/alpheios-project/alpheios_nemo_ui',
    license='GNU GPL',
    author='Bridget Almas',
    author_email='balmas@gmail.com',
    description='CapiTainS Alpheios UI for Nemo',
    test_suite="tests",
    install_requires=[
        "flask_nemo>=1.0.0b5",
        "capitains_nautilus>=1.0.0b6"
    ],
    tests_require=[
        "capitains_nautilus>=1.0.0b6"
    ],
    include_package_data=True,
    zip_safe=False
)
