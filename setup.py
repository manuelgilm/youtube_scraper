from setuptools import setup, find_packages

setup(
    name="youtube_scraper",
    version="0.1",
    description="Useful tools to get information from youtube videos",
    author ="Manuel Gil",
    author_email="manuelgilsitio@gmail.com",
    install_requires=["selenium"],
    packages=find_packages()

)