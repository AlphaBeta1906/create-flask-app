from setuptools import setup,find_packages

setup(
    name="create-flask-app",
    version="0.0.1",
    description="a simple cli tools to generate template for flask app",
    license="MIT",
    author="fariz",
    packages=find_packages(),
    include_package_data=True,
    author_email="farizi1906@gmail.com",
    py_modules=["main"],
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
    install_requires=["Click","requests"],
    keywords="automation,tools ,cli,project,template,flask,development,web,api",    
    python_requires=">=3.7",
)