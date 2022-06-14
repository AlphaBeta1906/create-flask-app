from requests.exceptions import ConnectionError
from click import group,version_option,option,argument,echo
from jinja2 import Template
from InquirerPy import prompt
from InquirerPy.separator import Separator

import click_completion
import requests

from shutil import copytree,ignore_patterns,unpack_archive,rmtree,chown
from distutils.errors import DistutilsError
from pathlib import Path

import os
import zipfile 

from .url import url

PROMPT = [
    {
        "type": "input",
        "message": "What's your project name(empty or '.' means current dir)?",
        "name": "name",
        "default": "."
    },
    {
        "type": "list",
        "message": "select template: ",
        "choices": [name.replace("_","-") for name in url.keys()],
        "name": "template"
    },
    {
      "type"  : "list",
      "message": "choose database: ",
      "choices": [
          "none",
          "sqlite3",
          "mysql",
          "postgresql"
      ],
      "name": "database"
    },
    {
        "type": "checkbox",
        "message": "Select Additional plugin:",
        "choices": [
            Separator(),
            "flask-wtf",
            "flask-marshmallow",
            "flask-debugtoolbar",
            "flask-cors",
            "flask-cache",
        ],
        "name": "additional_plugin"
    },
    {
        "type": "confirm",
        "message": "Are you sure to use this configuration?",
        "default": False,
        "name": "confirmation"
    },        
]

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
    
    create_project(template, output)

@create_flask_app.command()
def create():
    """
    more interactive version of 'new' command
    """
    
    # for now there are no real function for this command
    result = prompt(PROMPT,vi_mode=True)
    name = result["name"]
    template = result["template"]
    
    if not result["confirmation"]:
        echo("project creation canceled")
        quit()
    
    create_project(template, output=name,plugins=result["additional_plugin"],database=result["database"])

@create_flask_app.command()
@option("--local","-l",is_flag=True,default=False,show_default=False)
def list(local: bool):
    """display available templates"""
    
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


@create_flask_app.command()
@argument("template")
def get(template: str):    
    """download new project template"""
    donwload(template, path)    

@create_flask_app.command()
@option("-t","--template",help="template name",metavar="<template>",default="min_api")
def update(template: str):
    """update exisiting template"""
    
    template = template.replace('-','_')
    echo("updating template...")
    rmtree(f"{path}/{template}/")
    donwload(template, f"{path}/{template}/")
    echo(f"succesfully updating template `{template}`")

@create_flask_app.command()
@argument("template",metavar="<template>")
def remove(template: str):
    """remove selected template"""
    template = template.replace('-','_')
    template_path = f"{path}{template}"
    if not os.path.exists(template_path):
         echo(f"template '{template}' not found")
    os.system(f"rm -rf {path}{template}")
    echo(f"succesffully deleting template `{template}`")

def download_file(template: str):
    template = template.replace('-','_')
    echo(f"downloading template '{template}' from {url[template][0]} ")
    repo =  requests.get(url[template][0]) 
    with open(f"{cache_path}{template}.zip","wb") as file:        
        file.write(repo.content)
        file.close()        
    

def error_msg(template: str):
     """
     display error message when template not found
     """
     echo(f"template with name '{template}' not found")
     quit()


def parse_and_overide(dir: str,plugins: list,database: str):
    for file in os.listdir("cfa/additionalFiles/"):
        _file = f"cfa/additionalFiles/{file}"
        print(_file)
        if not os.path.isdir(_file):
            plugin = open(_file,"r").read()
            #print(text)
            template = Template(plugin)
            render = template
            
            rendered = render.render(additional_plugin=plugins,database=database)
            print(plugins)
            
            new_requirements = None
            
            if os.path.splitext(file)[0] in ("config","__init__"):
                new_requirements = open(os.path.join(os.getcwd(),f"{dir}/app/{file}"),"w")
            else:
                new_requirements = open(os.path.join(os.getcwd(),f"{dir}/{file}"),"w")
            new_requirements.write(rendered)
        

def donwload(template: str,path: str,output: str = ".",copy: bool=False,download: bool=False,is_update: bool=False):
    """
    this function is different from :func:`download_file`, 
    because this function will use :func:`download_file` 
    and copy downloaded file to output dir
    """
    if not os.path.exists(path):
        os.makedirs(path)
    
    if not os.path.exists(cache_path):
        os.makedirs(cache_path)
    
    try:
        TEMPLATE_ARCHIVE = f"{cache_path}{template}.zip"
        
        if not os.path.exists(TEMPLATE_ARCHIVE):            
            download_file(template)
        elif is_update:
            if not os.path.exists(f"{path}/{template}/"):
                echo("template not found")
                return 
            rmtree(TEMPLATE_ARCHIVE)
            download_file(template)                    
        else:
             echo("copy template from cache")
            
        zipdata = zipfile.ZipFile(TEMPLATE_ARCHIVE)
        folders_in_archive = zipdata.infolist()
        original_name = folders_in_archive[0].filename
        
        if not os.path.exists(f"{path}/{template}/"):
            unpack_archive(TEMPLATE_ARCHIVE,extract_dir=f"{path}")        
            os.rename(f"{path}/{original_name}/",f"{path}/{template}")
        
        echo(f"downloading template success,you can use this template by running `create-flask-app new -t {template} ` ")
        
        if copy:
            copytree(f"{path}/{template}/",output,ignore=ignore_patterns(".git"), dirs_exist_ok=True)            
    except KeyError:
        error_msg(template)
        return    
    except ConnectionError:
        echo("connection error")
        quit()
        return
    except FileExistsError:
        echo(f"template already exist,you can run `create-flask-app new -t {template} -o .` to start using it ")
        return
    except OSError:
        echo(f"template already exist,you can run `create-flask-app new -t {template} -o .` to start using it ")
        return

def create_project(template: str,output: str,plugins: list,database: str):
    template = template.replace("-", "_")
    try:
        try:
            url[template]
            copytree(f"{path}/{template}/",output,ignore=ignore_patterns(".git"), dirs_exist_ok=True)
        except KeyError:
            error_msg(template)
            quit()
        except FileNotFoundError:
            echo("flask template not found,clone new one from remote...")
        
            # download/clone template
            donwload(template, path,output,copy=True)            
    except DistutilsError:
        echo("flask template not found,clone new one from remote...")
        
        # download/clone template
        donwload(template, path,output,copy=True)
    else:
        echo("flask template exist,copying...")
        echo(f"successfully copying {template} project template ")
        echo(f"run 'cd {output}' to change to project directory")
        echo("\n")
        echo("run 'pip install -r requirements.txt' to install dependencies")
        echo("\n")
        echo("run `python app.py` to start the flask development server")
        echo("\n")
        echo("app will start at http://localhost:5000 (or try http://localhost:5000/api/v1/ if the first one is 404 not found)")
        echo("\n")
        echo("make sure to README.md first to know more about the template")
        parse_and_overide(output,plugins,database)
