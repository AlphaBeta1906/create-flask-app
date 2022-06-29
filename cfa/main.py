from click import group,version_option,option,argument,echo
from InquirerPy import prompt

import click_completion

from shutil import rmtree
from pathlib import Path

import os

from .url import URL as url
from .function import Create_Project
from .prompt import PROMPT

path = os.path.join(Path.home(),".create-flask-app/")
cache_path = os.path.join(Path.home(),".create-flask-app-cache/")

click_completion.init()

@group()
@version_option("0.0.1", help="Show version") 
def create_flask_app():
    """ 
    create-flask-app is a command line app to generate simple template flask project 
    version : 0.0.1
    """
    pass

@create_flask_app.command()
@option("-o","--output",default=".",help="output dir",metavar="<dir>")
@option("-t","--template",help="template name",default="min_api",metavar="<template_name>")
def new(output: str,template: str):
    """generate new flask project template"""
    
    project = Create_Project(name=output,template=template,database="sqlite",plugins=[],output_dir=output)
    project.create_project()

@create_flask_app.command()
def create():
    """
    more interactive version of 'new' command
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

"""
#@create_flask_app.command()
#@option("--local","-l",is_flag=True,default=False,show_default=False)
def list(local: bool):
  
    
    if local:
        echo("display local template")
        try:
            dirs = []
            for dir,sub_dirs,file in os.walk(f"{path}"):
                dirs.append(sub_dirs)
            for templates in dirs[0]:
                echo(templates)
        except FileNotFoundError:
            echo("templates folder not founds")
        return
    echo("available templates: \n")
    for k,v in url.items():
        echo(f"» {k} : {v[1]}")
        echo("\n")


#@create_flask_app.command()
#@argument("template")
def get(template: str):    
    
    project = Create_Project(template=template,output_dir=path)
    project.download_file()

#@create_flask_app.command()
#@option("-t","--template",help="template name",metavar="<template>",default="min_api")
def update(template: str):
    
    project = Create_Project(template=template,output_dir=path)
    
    template = template.replace('-','_')
    echo("updating template...")
    rmtree(f"{path}/{template}/")    
    project.download_file()
    echo(f"succesfully updating template `{template}`")

#@create_flask_app.command()
#@argument("template",metavar="<template>")
def remove(template: str):
    
    template = template.replace('-','_')
    template_path = f"{path}{template}"
    if not os.path.exists(template_path):
         echo(f"template '{template}' not found")
    os.system(f"rm -rf {path}{template}")
    echo(f"succesffully deleting template `{template}`")
"""