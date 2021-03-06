from click import group,version_option,option,echo
from InquirerPy import prompt

import click_completion

from .function import Create_Project
from .prompt import PROMPT

click_completion.init()

@group()
@version_option("0.2.1", help="Show version") 
def create_flask_app():
    """ 
    create-flask-app is a command line tools to generate simple flask project template
    version : 0.2.1
    """
    pass

@create_flask_app.command()
@option("-o","--output",default=".",help="output dir",metavar="<dir>")
def new(output: str):
    """
    generate minimal project template with minimal plugin
    """
    
    project = Create_Project(
        name=output,
        database="sqlite",
        plugins=["flask-sqlalchemy"],
        css="bootstrap-5",auth="none",output_dir=output,additional=[])
    project.create_project()

@create_flask_app.command()
def create():
    """
    generate new project template with prompt and select the additional plugin
    """
    
    result = prompt(PROMPT,vi_mode=True)
    name = result["name"]
    
    if not result["confirmation"]:
        echo("project creation canceled")
        quit()

    project = Create_Project(
                name,
                plugins=result["additional_plugin"],
                database=result["database"],
                output_dir=name,
                css=result["css"],
                additional=result["add"],
                auth=result["auth"]
            )    
    project.create_project()