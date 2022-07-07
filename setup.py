from setuptools import setup,find_packages

setup(
    name="create-flask-project",
    version="0.1.1",
    description="a simple cli tools to generate template for flask app",
    long_description= open("README.md","r").read(),
    license="MIT",
    author="fariz",
    packages=find_packages(),
    include_package_data=True,
    author_email="farizi1906@gmail.com",
    maintainer="https://github.com/AlphaBeta1906",
    py_modules=["main"],
    url="https://github.com/AlphaBeta1906/create-flask-app",
    download_url="https://github.com/AlphaBeta1906/create-flask-app/archive/refs/tags/v0.1.1.tar.gz",
    entry_points="""
        [console_scripts]
        create-flask-app= cfa.main:create_flask_app
    """,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Framework :: Flask",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
    ],
    install_requires=["Click","InquirerPy","jinja2","click-autocomplete"],
    keywords="automation,tools ,cli,project,template,flask,development,web,api,boilerplate",    
    python_requires=">=3.7",
)