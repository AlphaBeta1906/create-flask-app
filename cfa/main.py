from requests.exceptions import ConnectionError

import click
import requests

from shutil import copytree,ignore_patterns,unpack_archive,rmtree,chown
from distutils.errors import DistutilsError
from pathlib import Path
import os
import zipfile

from .url import url

path = os.path.join(Path.home(),".create-flask-app/")
cache_path = os.path.join(Path.home(),".create-flask-app-cache/")

@click.group()
@click.version_option("0.0.1", help="Show version") 
def create_flask_app():
    """ 
    create-flask-app is a command line app to generate simple template flask project 
    version : 0.0.1
    """
    pass

@create_flask_app.command()
@click.option("-o","--output",default=".",help="output dir",metavar="<dir>")
@click.option("-t","--template",help="template name",default="min_api",metavar="<template_name>")
def new(output: str,template: str):
    """generate new flask project template"""
    try:
        try:
            url[template]
            copytree(f"{path}/{template}/",output,ignore=ignore_patterns(".git"), dirs_exist_ok=True)
        except KeyError:
            error_msg(template)
            return
    except DistutilsError:
        click.echo("flask template dir not found,clone new one from remote...")
        
        # download/clone template
        donwload(template, path,output,copy=True)
    else:
        click.echo("flask template exist,copying...")
    click.echo(f"successfully copying {template} project template ")
    click.echo("\n")
    click.echo("run 'pip install -r requirements.txt' to install dependencies")
    click.echo("\n")
    click.echo("run `python app.py` to start the flask development server")
    click.echo("\n")
    click.echo("app will start at http://localhost:5000 (or try http://localhost:5000/api/v1/ if the first one is 404 not found)")
    click.echo("\n")
    click.echo("make sure to README.md first to know more about the template")

@create_flask_app.command()
def list():
    """display available templates"""
    
    click.echo("available templates: \n")
    for k,v in url.items():
        click.echo(f"» {k} : {v[1]}")
    click.echo("\n")


@create_flask_app.command()
@click.argument("template")
def get(template: str):    
    """download new project template"""
    donwload(template, path)    

@create_flask_app.command()
@click.option("-t","--template",help="template name",metavar="<template>",default="min_api")
def update(template: str):
    """update exisiting template"""
    click.echo("updating template...")
    rmtree(f"{path}/{template}/")
    donwload(template, f"{path}/{template}/")
    click.echo(f"succesfully updating template `{template}`")

@create_flask_app.command()
@click.argument("template",metavar="<template>")
def remove(template: str):
    """remove selected template"""
    template_path = f"{path}{template}"
    if not os.path.exists(template_path):
        click.echo(f"template '{template}' not found")
    os.system(f"rm -rf {path}{template}")
    click.echo(f"succesffully deleting template `{template}`")


def download_file(template):
    click.echo(f"downloading template '{template}' from {url[template][0]} ")
    repo = requests.get(url[template][0])
    with open(f"{cache_path}{template}.zip","wb") as file:
        file.write(repo.content)
        file.close()        
    

def error_msg(template: str):
    click.echo(f"template with name '{template}' not found")

def donwload(template: str,path: str,output: str = ".",copy: bool=False,download: bool=False,is_update: bool=False):
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
                click.echo("template not found")
                return 
            rmtree(TEMPLATE_ARCHIVE)
            download_file(template)                    
        else:
            click.echo("copy template from cache")
            
        zipdata = zipfile.ZipFile(TEMPLATE_ARCHIVE)
        folders_in_archive = zipdata.infolist()
        original_name = folders_in_archive[0].filename
        
        unpack_archive(TEMPLATE_ARCHIVE,extract_dir=f"{path}")        
        os.rename(f"{path}/{original_name}/",f"{path}/{template}")
        
        click.echo(f"downloading template success,you can use this template by running `create-flask-app new -t {template} ` ")
        
        if copy:
            copytree(f"{path}/{template}/",output,ignore=ignore_patterns(".git"), dirs_exist_ok=True)
    except KeyError:
        error_msg(template)
        return    
    except ConnectionError:
        click.echo("connection error")
        return
    except FileExistsError:
        click.echo(f"template already exist,you can run `create-flask-app new -t {template} -o .` to start using it ")
        return
