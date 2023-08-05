import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flet_like_streamlit",
    version="0.0.5",
    author="Omochi",
    author_email="soffionam@yahoo.co.jp",
    description="Flet working like streamlit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Shogo0607/flet-like-streamlit",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires= ["flet","numpy","pandas"],
)