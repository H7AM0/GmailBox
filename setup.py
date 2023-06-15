import setuptools

setuptools.setup(
	name= "GmailBox",
	version= "0.0.1",
	author= "Hamo",
    keywords=["gmail","mail","GmailBox"],
    install_requires=['requests','beautifulsoup4'],
    long_description_content_type="text/markdown",
    long_description="With this library, you can create random Gmail and receive messages",
	description= "With this library, you can create random Gmail and receive messages",
	packages=setuptools.find_packages(),
	classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)