from setuptools import setup,find_packages

setup(
    name="jarvis_spider",
    version="0.0.1",
    keywords=["pip","jarvis_spider"],
    description="新的爬虫框架",
    license="MIT Licence",
    
    author="gk",
    author_email='1015295213@qq.com',

    packages=find_packages(),
    include_package_data= True,
    platforms="any",
    install_requires=["requests"],
)